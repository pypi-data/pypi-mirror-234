import asyncio

import pytest

from celery.aio.result import AsyncResult

from t.base import AsyncFlakyTest
from .tasks import sleeping
from .test_aiotasks import assert_task_succeed


class test_redis(AsyncFlakyTest):
    @pytest.fixture(autouse=True)
    def setup(self, manager):
        pass

    async def test_restart_between_two_tasks(self, redis_server):
        result = await sleeping.aio.delay(1)
        await result.get()
        await assert_task_succeed(result)
        redis_server.restart()
        await asyncio.sleep(2)
        result = await sleeping.aio.delay(1)
        await result.get()
        await assert_task_succeed(result)

    async def test_restart_during_drain_events(self, redis_server):
        result = await sleeping.aio.delay(4)
        task = asyncio.create_task(result.get())
        redis_server.restart()
        await asyncio.sleep(2)
        await task
        await assert_task_succeed(result)

    async def test_conn_closed_between_two_tasks(self, redis_server):
        result = await sleeping.aio.delay(1)
        await result.get()
        await assert_task_succeed(result)
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        result = await sleeping.aio.delay(1)
        await result.get()
        await assert_task_succeed(result)

    async def test_conn_closed_during_drain_events(self, redis_server):
        result = await sleeping.aio.delay(3)
        task = asyncio.create_task(result.get())
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        await task
        await assert_task_succeed(result)

    async def test_get_result_ok(self, redis_server):
        r = await sleeping.aio.delay(1)
        result = AsyncResult(r.id)
        await r.get()
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        await result.get()
        await assert_task_succeed(r)
        await assert_task_succeed(result)

    async def test_concurrent_get_result_ok(self, redis_server):
        result1 = await sleeping.aio.delay(2)
        result2 = AsyncResult(result1.id)
        task1 = asyncio.create_task(result1.get())
        task2 = asyncio.create_task(result2.get())
        await asyncio.sleep(0.5)
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        await task1
        await task2
        await assert_task_succeed(result1)
        await assert_task_succeed(result2)

    async def test_empty_pubsub_after_reconnect(self, redis_server):
        result = await sleeping.aio.delay(1)
        task = asyncio.create_task(result.get())
        await asyncio.sleep(0)
        pubsub_port = (
            result.backend.result_consumer
                ._pubsub.connection
                ._writer.transport
                ._extra['sockname'][1]
        )
        redis_server.pause(1.5)
        redis_server.kill_by_port(pubsub_port)
        await asyncio.sleep(0.5)
        await task
        await assert_task_succeed(result)

    async def test_get_result_on_finished(self, redis_server):
        result = await sleeping.aio.delay(1)
        await asyncio.sleep(1.5)
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        await result.get()
        await assert_task_succeed(result)

    async def test_get_result_on_finished_with_new_result(self, redis_server):
        r = await sleeping.aio.delay(1)
        await r.get()
        task_id = r.id
        del r
        await asyncio.sleep(1.5)
        result = AsyncResult(task_id)
        await result.backend.client.ping()
        redis_server.kill_clients()
        await asyncio.sleep(0.5)
        await result.get()
        await assert_task_succeed(result)
