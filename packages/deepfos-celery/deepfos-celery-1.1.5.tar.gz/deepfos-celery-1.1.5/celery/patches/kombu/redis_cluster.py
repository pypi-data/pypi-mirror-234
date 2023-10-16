from contextlib import contextmanager
from queue import Empty
from typing import NamedTuple, List

from kombu.utils.encoding import bytes_to_str
from kombu.utils.eventio import READ, ERR
from kombu.utils.json import loads

from kombu.transport import virtual
from kombu.transport.redis import (
    Channel as RedisChannel,
    MultiChannelPoller,
    QoS as RedisQoS,
    Transport as RedisTransport,
)

from redis.connection import Connection
from redis.exceptions import MovedError
from redis.cluster import (
    RedisCluster, ClusterPubSub,
)
from redis import cluster

from .redis import ClusterChannleMixin


class QoS(RedisQoS):
    def restore_by_tag(self, tag, client=None, leftmost=False):
        assert isinstance(client, RedisCluster)
        node = client.get_node_from_key(self.unacked_key)
        return super().restore_by_tag(
            tag, client.get_redis_connection(node), leftmost)


class RedisNodeClient(NamedTuple):
    client: RedisCluster
    node: str
    conn: Connection

    def parse_response(self, cmd, **options):
        node = self.client.get_node(node_name=self.node)
        redis_node = node.redis_connection
        return redis_node.parse_response(self.conn, cmd, **options)


class PubSubNodeClient(RedisNodeClient):
    client: ClusterPubSub


class ClusterPoller(MultiChannelPoller):

    def _register(self, channel, client: RedisNodeClient, type):
        ident = (channel, client, type)

        if ident in self._chan_to_sock:
            self._unregister(*ident)

        if client.conn._sock is None:
            client.conn.connect()

        sock = client.conn._sock
        self._fd_to_chan[sock.fileno()] = (channel, client, type)
        self._chan_to_sock[ident] = sock
        self.poller.register(sock, self.eventflags)

    def _unregister(self, channel, client, type):
        sock = self._chan_to_sock[(channel, client, type)]
        self.poller.unregister(sock)

    def _register_BRPOP(self, channel):
        for cli in self._get_clis_for_client(
            channel.client, channel
        ):
            ident = (channel, cli, 'BRPOP')

            if cli.conn._sock is None or ident not in self._chan_to_sock:
                channel._in_poll = False
                self._register(*ident)

        if not channel._in_poll:  # send BRPOP
            channel._brpop_start()

    def _register_LISTEN(self, channel):
        for cli in self._get_clis_for_subclient(
            channel.subclient, channel
        ):
            ident = (channel, cli, 'LISTEN')

            if cli.conn._sock is None or ident not in self._chan_to_sock:
                channel._in_listen = False
                self._register(*ident)

        if not channel._in_listen:  # subscribe
            channel._subscribe()

    def _find_existed_clis(self, target_cls):
        chan_to_sock = [
            item for item in self._chan_to_sock or []
            if item[1].client.__class__ is target_cls
        ]

        if chan_to_sock:
            return [cli for _, cli, _ in chan_to_sock]

    def _get_clis_for_client(
        self,
        client: RedisCluster,
        channel
    ) -> List[RedisNodeClient]:
        if exist_clis := self._find_existed_clis(RedisCluster):
            return exist_clis

        clis = []
        for key in channel.active_queues:
            node = client.get_node_from_key(key)
            redis_conn = client.get_redis_connection(node)
            conn = redis_conn.connection_pool.get_connection('_')
            clis.append(RedisNodeClient(
                client=client, node=node.name, conn=conn))
        return clis

    def _get_clis_for_subclient(
        self,
        client: ClusterPubSub,
        channel
    ) -> List[PubSubNodeClient]:
        if exist_clis := self._find_existed_clis(ClusterPubSub):
            return exist_clis

        clis = []
        for queue in channel.active_fanout_queues:
            key = channel._get_subscribe_topic(queue)
            node = client.cluster.get_node_from_key(key)
            client.set_pubsub_node(client.cluster, node=node)
            redis_conn = client.get_redis_connection()
            conn = redis_conn.connection_pool.get_connection('_')
            clis.append(PubSubNodeClient(
                client=client, node=node.name, conn=conn))
        return clis

    def handle_event(self, fileno, event):
        if event & READ:
            return self.on_readable(fileno), self
        elif event & ERR:
            chan, cli, cmd = self._fd_to_chan[fileno]
            chan._poll_error(cmd, client=cli)

    def on_readable(self, fileno):
        try:
            chan, cli, cmd = self._fd_to_chan[fileno]
        except KeyError:
            return

        if chan.qos.can_consume():
            return chan.handlers[cmd](client=cli)


class Channel(ClusterChannleMixin, RedisChannel):
    QoS = QoS
    connection_class = Connection

    from_transport_options = RedisChannel.from_transport_options + (
        'namespace',
        'keyprefix_queue',
        'keyprefix_fanout',
    )
    client: cluster.RedisCluster

    def __init__(self, conn, *args, **kwargs):
        options = conn.client.transport_options
        self._patch_options(options)
        super().__init__(conn, *args, **kwargs)
        self.client.info()

    @contextmanager
    def conn_or_acquire(self, client=None):
        if client:
            yield client
        else:
            yield self.client

    def _get_client(self):
        return cluster.RedisCluster

    def _create_client(self, asynchronous=False):
        params = self._connparams(asynchronous=asynchronous)
        params.pop('db', None)
        params.pop('connection_class', None)
        return self.Client(**params)

    def _receive(self, **options):
        self.subclient.connection = options['client'].conn
        return super()._receive()

    def _brpop_start(self, timeout=1):
        queues = self._queue_cycle.consume(len(self.active_queues))
        if not queues:
            return

        self._in_poll = True
        timeout = timeout or 0
        cli = self.client
        node_to_keys = {}

        for key in queues:
            node = cli.get_node_from_key(key)
            node_to_keys.setdefault(node.name, []).append(key)

        for chan, client, cmd in self.connection.cycle._chan_to_sock:
            expected = (self, cli, 'BRPOP')
            keys = node_to_keys.get(client.node)

            if keys and (chan, client.client, cmd) == expected:
                for key in keys:
                    client.conn.send_command('BRPOP', key, timeout)

    def _brpop_read(self, client: RedisNodeClient, **options):
        try:
            conn = client.conn
            cli = client.client

            try:
                resp = client.parse_response('BRPOP', **options)
            except self.connection_errors:
                conn.disconnect()
                raise Empty()
            except MovedError as err:
                # copied from rediscluster/client.py
                cli.reinitialize_counter += 1
                if cli._should_reinitialized():
                    cli.nodes_manager.initialize()
                    # Reset the counter
                    cli.reinitialize_counter = 0
                else:
                    cli.nodes_manager.update_moved_exception(err)
                raise Empty()

            if resp:
                dest, item = resp
                dest = bytes_to_str(dest).rsplit(self.sep, 1)[0]
                self._queue_cycle.rotate(dest)
                self.connection._deliver(loads(bytes_to_str(item)), dest)
                return True
        finally:
            self._in_poll = False

    def _subscribe(self):
        keys = [self._get_subscribe_topic(queue)
                for queue in self.active_fanout_queues]
        if not keys:
            return

        self._in_listen = True
        cli = self.subclient
        node_to_keys = {}

        for key in keys:
            node = cli.cluster.get_node_from_key(key)
            node_to_keys.setdefault(node.name, []).append(key)

        for chan, client, cmd in self.connection.cycle._chan_to_sock:
            expected = (self, cli, 'LISTEN')
            keys = node_to_keys.get(client.node)

            cli.connection = client.conn
            if keys and (chan, client.client, cmd) == expected:
                for key in keys:
                    cli.psubscribe(key)

    def _poll_error(self, cmd, **options):
        cli: RedisNodeClient = options['client']

        if cmd == 'BRPOP':
            cli.parse_response(cmd)


class Transport(RedisTransport):

    Channel = Channel

    driver_type = 'redis-cluster'
    driver_name = driver_type

    implements = virtual.Transport.implements.extend(
        asynchronous=True,
        exchange_type=frozenset(['direct', 'fanout'])
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cycle = ClusterPoller()
