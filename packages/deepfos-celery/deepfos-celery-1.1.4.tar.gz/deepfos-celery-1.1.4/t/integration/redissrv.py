import subprocess
import socket
import os
import tempfile
import time
from contextlib import closing
from tempfile import NamedTemporaryFile


def get_redis_connection(port=None):
    from redis import StrictRedis
    return StrictRedis(
        port=port
    )


class RedisServer:
    def __init__(self, redis_executable=None):
        self._serving = False
        self._proc: subprocess.Popen = None
        self._redis = redis_executable or self.find_executable('redis-server')
        self._port = self.find_available_port()
        self._work_dir = None

    def wait_util_open(self, interval):
        while True:
            with closing(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ) as sock:
                if sock.connect_ex(('localhost', self._port)) == 0:
                    break
                time.sleep(interval)

    def as_url(self):
        return f"redis://:{self.port}"

    @property
    def client(self):
        from redis import StrictRedis
        return StrictRedis(port=self.port)

    @property
    def port(self):
        return self._port

    @staticmethod
    def find_executable(exe):
        try:
            executable = subprocess.check_output(
                f"which {exe}".split(), text=True)
            return executable.strip()
        except subprocess.CalledProcessError:
            raise RuntimeError(f'exe not avaliable.')

    @staticmethod
    def find_available_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", 0))
            return sock.getsockname()[1]

    def get_start_cmd(self):
        return f"nohup {self._redis} --port {self._port}"

    def start(self):
        if self._serving:
            return
        cmd = self.get_start_cmd()
        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self._work_dir,
            shell=True
        )
        self._serving = True

    def stop(self):
        if not self._serving:
            return
        self._proc.terminate()
        self._proc.wait()
        self._proc = None
        self._serving = False

    def restart(self):
        self.stop()
        self.start()

    def kill_clients(self, type='all'):
        if type == 'all':
            types = ['normal', 'pubsub']
        else:
            types = [type.lower()]

        with self.client.pipeline() as pipe:
            for t in types:
                pipe.client_kill_filter(_type=t)
            pipe.execute()

    def kill_by_port(self, port):
        self.client.client_kill(f"127.0.0.1:{port}")

    def pause(self, seconds):
        self.client.client_pause(timeout=int(seconds * 1000))

    def __repr__(self):
        if self._serving:
            return f"Redis | Port: {self._port} | PID: {self._proc.pid}"
        else:
            return f"Redis | Stopped"

    def __del__(self):
        self.stop()


class RedisSentinelServer(RedisServer):
    def __init__(self, master_name: str = 'mymaster', redis_executable=None):
        super().__init__(redis_executable)
        self.master_name = master_name
        self.master = RedisServer()
        self._redis = redis_executable or self.find_executable(
            'redis-sentinel')
        self._conf = None

    def as_url(self):
        return f"sentinel://:{self.port}"

    @property
    def client(self):
        from redis.sentinel import Sentinel
        s = Sentinel([('localhost', self.port)])
        return s.master_for(self.master_name)

    def get_start_cmd(self):
        conf = self.create_configure()
        return f"nohup {self._redis} {conf.name}"

    def create_configure(self):
        configure = "\n".join((
            f"port {self.port}",
            f"sentinel monitor {self.master_name} localhost {self.master.port} 2",
            f"sentinel config-epoch {self.master_name} 0",
            "sentinel deny-scripts-reconfig yes"
        ))
        self._conf = f = NamedTemporaryFile(
            mode='wt', delete=False, encoding='utf8')
        f.writelines(configure)
        f.flush()
        return f

    def start(self):
        if self._serving:
            return
        self.master.start()
        super().start()

    def stop(self):
        if not self._serving:
            return

        super().stop()
        self._conf.close()
        os.unlink(self._conf.name)
        self.master.stop()


class RedisServerCluster(RedisServer):
    def __init__(self, redis_executable=None):
        super().__init__(redis_executable)
        self._cli = self.find_executable('redis-cli')
        self._work_dir = tempfile.mkdtemp(
            prefix='redis-cluster-', suffix='-run')
        self._port -= 5
        self._fresh_start = True

        self._hosts = ""
        for i in range(6):
            self._hosts += f" 127.0.0.1:{self._port + i}"

    def start(self):
        super().start()
        self._proc.communicate()
        if self._fresh_start:
            self.wait_util_open(0.5)
            cmd = (
                "{client} "
                "--cluster create {hosts} "
                "--cluster-replicas 1 "
                "--cluster-yes"
            ).format(client=self._cli, hosts=self._hosts)
            subprocess.check_output(cmd, cwd=self._work_dir, shell=True)
        self._fresh_start = False

    def get_start_cmd(self):
        cmds = []

        for i in range(6):
            port = self.port + i
            cmds.append((
                "{server} "
                "--port {port} "
                "--protected-mode no "
                "--cluster-enabled yes "
                "--cluster-config-file nodes-{port}.conf "
                "--cluster-node-timeout 2000 "
                "--appendonly yes "
                "--appendfilename appendonly-{port}.aof "
                "--dbfilename dump-{port}.rdb "
                "--logfile {port}.log "
                "--daemonize yes"
            ).format(port=port, server=self._redis))

        return " && ".join(cmds)

    def stop(self):
        if self._serving:
            cmds = []
            for i in range(6):
                cmds.append(f"{self._cli} -p {self.port + i} shutdown nosave")
            subprocess.check_output(" && ".join(cmds), shell=True)
        super().stop()

    def as_url(self):
        return f"redis-cluster://:{self.port}"
