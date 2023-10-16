import asyncio
import dataclasses
import os
import pytest

from urllib.parse import urlparse

# we have to import the pytest plugin fixtures here,
# in case user did not do the `python setup.py develop` yet,
# that installs the pytest plugin into the setuptools registry.
from celery.contrib.pytest import celery_app, celery_session_worker
from celery.contrib.testing.manager import Manager

from .redissrv import RedisServer, RedisSentinelServer, RedisServerCluster

# Tricks flake8 into silencing redefining fixtures warnings.
__all__ = (
    'celery_app',
    'celery_session_worker',
    'get_active_redis_channels',
    'get_redis_connection',
)


class RedisConfig:
    url: str
    port: int
    host: str = 'localhost'
    master: str = None

    @classmethod
    def is_sentinel(cls):
        return cls.url.lower().startswith('sentinel')


@pytest.fixture(scope='session')
def redis_server(request):
    redis_type = request.config.getoption('redis_type')
    print(redis_type)
    if redis_type == 'sentinel':
        redis = RedisSentinelServer()
    elif redis_type == 'cluster':
        redis = RedisServerCluster()
    else:
        redis = RedisServer()
    redis.start()
    yield redis
    redis.stop()


def get_redis_connection():
    host = os.environ.get('REDIS_HOST', RedisConfig.host)
    port = RedisConfig.port

    if RedisConfig.is_sentinel():
        from redis import Sentinel
        return Sentinel([(host, port)]).master_for(RedisConfig.master)
    else:
        from redis import StrictRedis
        return StrictRedis(host=host, port=port)


def get_active_redis_channels(as_string=False):
    raw = get_redis_connection().execute_command('PUBSUB CHANNELS')
    if as_string:
        return [i.decode() for i in raw]
    else:
        return raw


@pytest.fixture(scope='session')
def celery_config(redis_server):
    TEST_BROKER = os.environ.get('TEST_BROKER', redis_server.as_url())
    TEST_BACKEND = os.environ.get('TEST_BACKEND', redis_server.as_url())

    r = urlparse(TEST_BACKEND)

    RedisConfig.url = TEST_BACKEND
    RedisConfig.host = r.hostname
    RedisConfig.port = r.port

    conf = {
        'broker_url': TEST_BROKER,
        'result_backend': TEST_BACKEND,
        'cassandra_servers': ['localhost'],
        'cassandra_keyspace': 'tests',
        'cassandra_table': 'tests',
        'cassandra_read_consistency': 'ONE',
        'cassandra_write_consistency': 'ONE',
        'worker_hijack_root_logger': True
    }

    if RedisConfig.is_sentinel():
        RedisConfig.master = redis_server.master_name
        conf['broker_transport_options'] = \
            conf['result_backend_transport_options'] = \
            {'master_name': redis_server.master_name}
    return conf


@pytest.fixture(scope='session')
def celery_enable_logging():
    return True


@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'prefork'


@pytest.fixture(scope='session')
def celery_includes():
    return {'t.integration.tasks'}


@pytest.fixture
def app(celery_app):
    yield celery_app


@pytest.fixture
def manager(app, celery_session_worker):
    return Manager(app)


@pytest.fixture(autouse=True)
def ZZZZ_set_app_current(app):
    app.set_current()
    app.set_default()


@pytest.fixture(scope='session')
def celery_class_tasks():
    from t.integration.tasks import ClassBasedAutoRetryTask
    return [ClassBasedAutoRetryTask]


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_addoption(parser):
    parser.addoption(
        '--redis',
        dest='redis_type',
        type=str,
        default='default',
        const='default',
        nargs='?',
        help='which mode redis is in'
    )
