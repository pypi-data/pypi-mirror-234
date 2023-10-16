from unittest.mock import Mock, AsyncMock

import pytest

from celery import uuid
from celery.aio import control as aio_control
from celery.app import control
from celery.exceptions import DuplicateNodenameWarning
from celery.utils.collections import LimitedSet

from t.base import AsyncTest


def _info_for_commandclass(type_):
    from celery.worker.control import Panel
    return [
        (name, info)
        for name, info in Panel.meta.items()
        if info.type == type_
    ]


def test_client_implements_all_commands(app):
    commands = _info_for_commandclass('control')
    assert commands
    for name, info in commands:
        assert getattr(app.aio_control, name)


def test_inspect_implements_all_commands(app):
    inspect = app.aio_control.inspect()
    commands = _info_for_commandclass('inspect')
    assert commands
    for name, info in commands:
        if info.type == 'inspect':
            assert getattr(inspect, name)


class test_flatten_reply:

    def test_flatten_reply(self):
        reply = [
            {'foo@example.com': {'hello': 10}},
            {'foo@example.com': {'hello': 20}},
            {'bar@example.com': {'hello': 30}}
        ]
        with pytest.warns(DuplicateNodenameWarning) as w:
            nodes = control.flatten_reply(reply)

        assert 'Received multiple replies from node name: {}.'.format(
            next(iter(reply[0]))) in str(w[0].message.args[0])
        assert 'foo@example.com' in nodes
        assert 'bar@example.com' in nodes


class test_inspect(AsyncTest):

    def setup(self):
        self.app.aio_control.broadcast = AsyncMock(name='broadcast')
        self.app.aio_control.broadcast.return_value = {}
        self.inspect = self.app.aio_control.inspect()

    def test_prepare_reply(self):
        reply = self.inspect._prepare([
            {'w1': {'ok': 1}},
            {'w2': {'ok': 1}},
        ])
        assert reply == {
            'w1': {'ok': 1},
            'w2': {'ok': 1},
        }

        i = self.app.aio_control.inspect(destination='w1')
        assert i._prepare([{'w1': {'ok': 1}}]) == {'ok': 1}

    def assert_broadcast_called(self, command,
                                destination=None,
                                callback=None,
                                connection=None,
                                limit=None,
                                timeout=None,
                                reply=True,
                                pattern=None,
                                matcher=None,
                                **arguments):
        self.app.aio_control.broadcast.assert_called_with(
            command,
            arguments=arguments,
            destination=destination or self.inspect.destination,
            pattern=pattern or self.inspect.pattern,
            matcher=matcher or self.inspect.destination,
            callback=callback or self.inspect.callback,
            connection=connection or self.inspect.connection,
            limit=limit if limit is not None else self.inspect.limit,
            timeout=timeout if timeout is not None else self.inspect.timeout,
            reply=reply,
        )

    async def test_active(self):
        await self.inspect.active()
        self.assert_broadcast_called('active')

    async def test_clock(self):
        await self.inspect.clock()
        self.assert_broadcast_called('clock')

    async def test_conf(self):
        await self.inspect.conf()
        self.assert_broadcast_called('conf', with_defaults=False)

    async def test_conf__with_defaults(self):
        await self.inspect.conf(with_defaults=True)
        self.assert_broadcast_called('conf', with_defaults=True)

    async def test_hello(self):
        await self.inspect.hello('george@vandelay.com')
        self.assert_broadcast_called(
            'hello', from_node='george@vandelay.com', revoked=None)

    async def test_hello__with_revoked(self):
        revoked = LimitedSet(100)
        for i in range(100):
            revoked.add(f'id{i}')
        await self.inspect.hello('george@vandelay.com', revoked=revoked._data)
        self.assert_broadcast_called(
            'hello', from_node='george@vandelay.com', revoked=revoked._data)

    async def test_memsample(self):
        await self.inspect.memsample()
        self.assert_broadcast_called('memsample')

    async def test_memdump(self):
        await self.inspect.memdump()
        self.assert_broadcast_called('memdump', samples=10)

    async def test_memdump__samples_specified(self):
        await self.inspect.memdump(samples=303)
        self.assert_broadcast_called('memdump', samples=303)

    async def test_objgraph(self):
        await self.inspect.objgraph()
        self.assert_broadcast_called(
            'objgraph', num=200, type='Request', max_depth=10)

    async def test_scheduled(self):
        await self.inspect.scheduled()
        self.assert_broadcast_called('scheduled')

    async def test_reserved(self):
        await self.inspect.reserved()
        self.assert_broadcast_called('reserved')

    async def test_stats(self):
        await self.inspect.stats()
        self.assert_broadcast_called('stats')

    async def test_revoked(self):
        await self.inspect.revoked()
        self.assert_broadcast_called('revoked')

    async def test_registered(self):
        await self.inspect.registered()
        self.assert_broadcast_called('registered', taskinfoitems=())

    async def test_registered__taskinfoitems(self):
        await self.inspect.registered('rate_limit', 'time_limit')
        self.assert_broadcast_called(
            'registered',
            taskinfoitems=('rate_limit', 'time_limit'),
        )

    async def test_ping(self):
        await self.inspect.ping()
        self.assert_broadcast_called('ping')

    async def test_ping_matcher_pattern(self):
        orig_inspect = self.inspect
        self.inspect = self.app.aio_control.inspect(pattern=".*", matcher="pcre")
        await self.inspect.ping()
        try:
            self.assert_broadcast_called('ping', pattern=".*", matcher="pcre")
        except AssertionError as e:
            self.inspect = orig_inspect
            raise e

    async def test_active_queues(self):
        await self.inspect.active_queues()
        self.assert_broadcast_called('active_queues')

    async def test_query_task(self):
        await self.inspect.query_task('foo', 'bar')
        self.assert_broadcast_called('query_task', ids=('foo', 'bar'))

    async def test_query_task__compat_single_list_argument(self):
        await self.inspect.query_task(['foo', 'bar'])
        self.assert_broadcast_called('query_task', ids=['foo', 'bar'])

    async def test_query_task__scalar(self):
        await self.inspect.query_task('foo')
        self.assert_broadcast_called('query_task', ids=('foo',))

    async def test_report(self):
        await self.inspect.report()
        self.assert_broadcast_called('report')


class test_Control_broadcast(AsyncTest):

    def setup(self):
        self.app.aio_control.mailbox = Mock(
            name='mailbox', return_value=AsyncMock())

    async def test_broadcast(self):
        await self.app.aio_control.broadcast('foobarbaz', arguments={'foo': 2})
        self.app.aio_control.mailbox.assert_called()
        self.app.aio_control.mailbox()._broadcast.assert_called_with(
            'foobarbaz', {'foo': 2}, None, False, 1.0, None, None,
            channel=None,
        )

    async def test_broadcast_limit(self):
        await self.app.aio_control.broadcast(
            'foobarbaz1', arguments=None, limit=None, destination=[1, 2, 3],
        )
        self.app.aio_control.mailbox.assert_called()
        self.app.aio_control.mailbox()._broadcast.assert_called_with(
            'foobarbaz1', {}, [1, 2, 3], False, 1.0, None, None,
            channel=None,
        )


class test_Control(AsyncTest):

    def setup(self):
        self.app.aio_control.broadcast = AsyncMock(name='broadcast')
        self.app.aio_control.broadcast.return_value = {}

        @self.app.task(shared=False, aio_variant=True)
        def mytask():
            pass
        self.mytask = mytask

    def assert_control_called_with_args(self, name, destination=None,
                                        _options=None, **args):
        self.app.aio_control.broadcast.assert_called_with(
            name, destination=destination, arguments=args, **_options or {})

    async def zzz_test_purge(self):
        self.app.amqp.TaskConsumer = Mock(name='TaskConsumer')
        await self.app.aio_control.purge()
        self.app.amqp.TaskConsumer().purge.assert_called_with()

    async def test_rate_limit(self):
        await self.app.aio_control.rate_limit(self.mytask.name, '100/m')
        self.assert_control_called_with_args(
            'rate_limit',
            destination=None,
            task_name=self.mytask.name,
            rate_limit='100/m',
        )

    async def test_rate_limit__with_destination(self):
        await self.app.aio_control.rate_limit(
            self.mytask.name, '100/m', 'a@w.com', limit=100)
        self.assert_control_called_with_args(
            'rate_limit',
            destination='a@w.com',
            task_name=self.mytask.name,
            rate_limit='100/m',
            _options={'limit': 100},
        )

    async def test_time_limit(self):
        await self.app.aio_control.time_limit(self.mytask.name, soft=10, hard=20)
        self.assert_control_called_with_args(
            'time_limit',
            destination=None,
            task_name=self.mytask.name,
            soft=10,
            hard=20,
        )

    async def test_time_limit__with_destination(self):
        await self.app.aio_control.time_limit(
            self.mytask.name, soft=10, hard=20,
            destination='a@q.com', limit=99,
        )
        self.assert_control_called_with_args(
            'time_limit',
            destination='a@q.com',
            task_name=self.mytask.name,
            soft=10,
            hard=20,
            _options={'limit': 99},
        )

    async def test_add_consumer(self):
        await self.app.aio_control.add_consumer('foo')
        self.assert_control_called_with_args(
            'add_consumer',
            destination=None,
            queue='foo',
            exchange=None,
            exchange_type='direct',
            routing_key=None,
        )

    async def test_add_consumer__with_options_and_dest(self):
        await self.app.aio_control.add_consumer(
            'foo', 'ex', 'topic', 'rkey', destination='a@q.com', limit=78)
        self.assert_control_called_with_args(
            'add_consumer',
            destination='a@q.com',
            queue='foo',
            exchange='ex',
            exchange_type='topic',
            routing_key='rkey',
            _options={'limit': 78},
        )

    async def test_cancel_consumer(self):
        await self.app.aio_control.cancel_consumer('foo')
        self.assert_control_called_with_args(
            'cancel_consumer',
            destination=None,
            queue='foo',
        )

    async def test_cancel_consumer__with_destination(self):
        self.app.aio_control.cancel_consumer(
            'foo', destination='w1@q.com', limit=3)
        self.assert_control_called_with_args(
            'cancel_consumer',
            destination='w1@q.com',
            queue='foo',
            _options={'limit': 3},
        )

    async def test_shutdown(self):
        await self.app.aio_control.shutdown()
        self.assert_control_called_with_args('shutdown', destination=None)

    async def test_shutdown__with_destination(self):
        await self.app.aio_control.shutdown(destination='a@q.com', limit=3)
        self.assert_control_called_with_args(
            'shutdown', destination='a@q.com', _options={'limit': 3})

    async def test_heartbeat(self):
        await self.app.aio_control.heartbeat()
        self.assert_control_called_with_args('heartbeat', destination=None)

    async def test_heartbeat__with_destination(self):
        await self.app.aio_control.heartbeat(destination='a@q.com', limit=3)
        self.assert_control_called_with_args(
            'heartbeat', destination='a@q.com', _options={'limit': 3})

    async def test_pool_restart(self):
        await self.app.aio_control.pool_restart()
        self.assert_control_called_with_args(
            'pool_restart',
            destination=None,
            modules=None,
            reload=False,
            reloader=None)

    async def test_terminate(self):
        self.app.aio_control.revoke = AsyncMock(name='revoke')
        await self.app.aio_control.terminate('124')
        self.app.aio_control.revoke.assert_called_with(
            '124', destination=None,
            terminate=True,
            signal=control.TERM_SIGNAME,
        )

    async def test_enable_events(self):
        await self.app.aio_control.enable_events()
        self.assert_control_called_with_args('enable_events', destination=None)

    async def test_enable_events_with_destination(self):
        await self.app.aio_control.enable_events(destination='a@q.com', limit=3)
        self.assert_control_called_with_args(
            'enable_events', destination='a@q.com', _options={'limit': 3})

    async def test_disable_events(self):
        await self.app.aio_control.disable_events()
        self.assert_control_called_with_args(
            'disable_events', destination=None)

    async def test_disable_events_with_destination(self):
        await self.app.aio_control.disable_events(destination='a@q.com', limit=3)
        self.assert_control_called_with_args(
            'disable_events', destination='a@q.com', _options={'limit': 3})

    async def test_ping(self):
        await self.app.aio_control.ping()
        self.assert_control_called_with_args(
            'ping', destination=None,
            _options={'timeout': 1.0, 'reply': True})

    async def test_ping_with_destination(self):
        await self.app.aio_control.ping(destination='a@q.com', limit=3)
        self.assert_control_called_with_args(
            'ping',
            destination='a@q.com',
            _options={
                'limit': 3,
                'timeout': 1.0,
                'reply': True,
            })

    async def test_revoke(self):
        await self.app.aio_control.revoke('foozbaaz')
        self.assert_control_called_with_args(
            'revoke',
            destination=None,
            task_id='foozbaaz',
            signal=control.TERM_SIGNAME,
            terminate=False,
        )

    async def test_revoke__with_options(self):
        await self.app.aio_control.revoke(
            'foozbaaz',
            destination='a@q.com',
            terminate=True,
            signal='KILL',
            limit=404,
        )
        self.assert_control_called_with_args(
            'revoke',
            destination='a@q.com',
            task_id='foozbaaz',
            signal='KILL',
            terminate=True,
            _options={'limit': 404},
        )

    async def test_election(self):
        await self.app.aio_control.election('some_id', 'topic', 'action')
        self.assert_control_called_with_args(
            'election',
            destination=None,
            topic='topic',
            action='action',
            id='some_id',
            _options={'connection': None},
        )

    async def test_autoscale(self):
        await self.app.aio_control.autoscale(300, 10)
        self.assert_control_called_with_args(
            'autoscale', max=300, min=10, destination=None)

    async def test_autoscale__with_options(self):
        await self.app.aio_control.autoscale(300, 10, destination='a@q.com', limit=39)
        self.assert_control_called_with_args(
            'autoscale', max=300, min=10,
            destination='a@q.com',
            _options={'limit': 39}
        )

    async def test_pool_grow(self):
        await self.app.aio_control.pool_grow(2)
        self.assert_control_called_with_args(
            'pool_grow', n=2, destination=None)

    async def test_pool_grow__with_options(self):
        await self.app.aio_control.pool_grow(2, destination='a@q.com', limit=39)
        self.assert_control_called_with_args(
            'pool_grow', n=2,
            destination='a@q.com',
            _options={'limit': 39}
        )

    async def test_pool_shrink(self):
        await self.app.aio_control.pool_shrink(2)
        self.assert_control_called_with_args(
            'pool_shrink', n=2, destination=None)

    async def test_pool_shrink__with_options(self):
        await self.app.aio_control.pool_shrink(2, destination='a@q.com', limit=39)
        self.assert_control_called_with_args(
            'pool_shrink', n=2,
            destination='a@q.com',
            _options={'limit': 39}
        )

    async def test_revoke_from_result(self):
        self.app.aio_control.revoke = AsyncMock(name='revoke')
        await self.app.AioAsyncResult('foozbazzbar').revoke()
        self.app.aio_control.revoke.assert_called_with(
            'foozbazzbar',
            connection=None, reply=False, signal=None,
            terminate=False, timeout=None)

    async def test_revoke_from_resultset(self):
        self.app.aio_control.revoke = AsyncMock(name='revoke')
        uuids = [uuid() for _ in range(10)]
        r = self.app.AioGroupResult(
            uuid(), [self.app.AioAsyncResult(x) for x in uuids])
        await r.revoke()
        self.app.aio_control.revoke.assert_called_with(
            uuids,
            connection=None, reply=False, signal=None,
            terminate=False, timeout=None)

    def test_after_fork_clears_mailbox_pool(self):
        amqp = Mock(name='amqp')
        self.app.aio_amqp = amqp
        closed_pool = Mock(name='closed pool')
        amqp.producer_pool = closed_pool
        assert closed_pool is self.app.aio_control.mailbox.producer_pool
        self.app.aio_control._after_fork()
        new_pool = Mock(name='new pool')
        amqp.producer_pool = new_pool
        assert new_pool is self.app.aio_control.mailbox.producer_pool

    def test_control_exchange__default(self):
        c = aio_control.Control(self.app)
        assert c.mailbox.namespace == 'celery'

    def test_control_exchange__setting(self):
        self.app.conf.control_exchange = 'test_exchange'
        c = aio_control.Control(self.app)
        assert c.mailbox.namespace == 'test_exchange'
