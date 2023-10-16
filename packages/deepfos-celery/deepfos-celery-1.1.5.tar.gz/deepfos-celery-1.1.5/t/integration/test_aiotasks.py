import asyncio
import time
from asyncio import sleep
from datetime import datetime, timedelta
from time import perf_counter

import pytest

import celery
from celery import group

from .conftest import get_active_redis_channels
from .tasks import (ClassBasedAutoRetryTask, ExpectedException, add,
                    add_ignore_result, add_not_typed, fail, print_unicode,
                    retry, retry_once, retry_once_priority, sleeping)
from t.base import AsyncTest, AsyncFlakyTest, FlakyTest


TIMEOUT = 10


class test_class_based_tasks(FlakyTest):
    def test_class_based_task_retried(self, celery_session_app,
                                      celery_session_worker):
        task = ClassBasedAutoRetryTask()
        celery_session_app.tasks.register(task)
        res = task.delay()
        assert res.get(timeout=TIMEOUT) == 1


async def _concurrent_runner(j, repeat=10):
    expects = [i + j for i in range(repeat)]
    # Tests calling task only with args
    async_results = await asyncio.gather(
        *(
            add.aio.delay(i, j)
            for i in range(repeat)
        )
    )

    results = await asyncio.gather(
        *(
            r.get(timeout=10)
            for r in async_results
        )
    )

    for expected, result, ar in zip(expects, results, async_results):
        assert result == expected
        assert (await ar.status) == 'SUCCESS'
        assert (await ar.ready()) is True
        assert (await ar.successful()) is True


_loop = None

def _producer(j):
    """Single producer helper function"""
    global _loop

    if _loop is None:
        _loop = asyncio.new_event_loop()
    _loop.run_until_complete(_concurrent_runner(j, repeat=20))
    return j


async def assert_task_succeed(result):
    assert (await result.status) == 'SUCCESS'
    assert (await result.ready()) is True
    assert (await result.successful()) is True


class test_tasks(AsyncTest):
    async def test_basic_task(self, manager):
        """Tests basic task call"""
        results = []
        # Tests calling task only with args
        for i in range(10):
            results.append([i + i, await add.aio.delay(i, i)])
        for expected, result in results:
            value = await result.get(timeout=10)
            assert value == expected
            await assert_task_succeed(result)

        results = []
        # Tests calling task with args and kwargs
        for i in range(10):
            results.append([3*i, await add.aio.delay(i, i, z=i)])
        for expected, result in results:
            value = await result.get(timeout=10)
            assert value == expected
            await assert_task_succeed(result)

    async def test_concurrent_task_only_args(self, manager):
        """Tests basic task call"""
        await _concurrent_runner(10, repeat=20)

    async def test_concurrent_task_with_kwargs(self, manager):
        """Tests basic task call"""
        expects = [3*i for i in range(20)]
        # Tests calling task only with args
        async_results = await asyncio.gather(*(
            add.aio.delay(i, i, z=i)
            for i in range(10)
        ))

        results = await asyncio.gather(*(
            r.get(timeout=10)
            for r in async_results
        ))

        for expected, result, ar in zip(expects, results, async_results):
            assert result == expected
            await assert_task_succeed(ar)

    def test_multiprocess_producer(self, manager):
        """Testing multiple processes calling tasks."""
        from multiprocessing import Pool
        pool = Pool(20)
        ret = pool.map(_producer, range(120))
        assert list(ret) == list(range(120))

    async def test_ignore_result(self, manager):
        """Testing calling task with ignoring results."""
        result = await add.aio.apply_async((1, 2), ignore_result=True)
        assert (await result.get()) is None

    async def test_timeout(self, manager):
        """Testing timeout of getting results from tasks."""
        result = await sleeping.aio.delay(10)
        with pytest.raises(celery.exceptions.TimeoutError):
            await result.get(timeout=5)

    async def test_expired(self, manager):
        """Testing expiration of task."""
        # Fill the queue with tasks which took > 1 sec to process
        for _ in range(4):
            await sleeping.aio.delay(2)
        # Execute task with expiration = 1 sec
        result = await add.aio.apply_async((1, 1), expires=1)
        with pytest.raises(celery.exceptions.TaskRevokedError):
            await result.get()
        assert (await result.status) == 'REVOKED'
        assert (await result.ready()) is True
        assert (await result.failed()) is False
        assert (await result.successful()) is False

        # Fill the queue with tasks which took > 1 sec to process
        for _ in range(4):
            await sleeping.aio.delay(2)
        # Execute task with expiration at now + 1 sec
        result = await add.aio.apply_async((1, 1), expires=datetime.utcnow() + timedelta(seconds=1))
        with pytest.raises(celery.exceptions.TaskRevokedError):
            await result.get()
        assert (await result.status) == 'REVOKED'
        assert (await result.ready()) is True
        assert (await result.failed()) is False
        assert (await result.successful()) is False

    async def test_eta(self, manager):
        """Tests tasks scheduled at some point in future."""
        start = perf_counter()
        # Schedule task to be executed in 3 seconds
        result = await add.aio.apply_async((1, 1), countdown=3)
        await sleep(1)
        assert (await result.status) == 'PENDING'
        assert (await result.ready()) is False
        assert (await result.get()) == 2
        end = perf_counter()
        assert (await result.status) == 'SUCCESS'
        assert (await result.ready()) is True
        # Difference between calling the task and result must be bigger than 3 secs
        assert (end - start) > 3

        start = perf_counter()
        # Schedule task to be executed at time now + 3 seconds
        result = await add.aio.apply_async((2, 2), eta=datetime.utcnow() + timedelta(seconds=3))
        await sleep(1)
        assert (await result.status) == 'PENDING'
        assert (await result.ready()) is False
        assert (await result.get()) == 4
        end = perf_counter()
        assert (await result.status) == 'SUCCESS'
        assert (await result.ready()) is True
        # Difference between calling the task and result must be bigger than 3 secs
        assert (end - start) > 3

    async def test_fail(self, manager):
        """Tests that the failing task propagates back correct exception."""
        result = await fail.aio.delay()
        with pytest.raises(ExpectedException):
            await result.get(timeout=5)
        assert (await result.status) == 'FAILURE'
        assert (await result.ready()) is True
        assert (await result.failed()) is True
        assert (await result.successful()) is False

    async def test_wrong_arguments(self, manager):
        """Tests that proper exceptions are raised when task is called with wrong arguments."""
        with pytest.raises(TypeError):
            add(5)

        with pytest.raises(TypeError):
            add(5, 5, wrong_arg=5)

        with pytest.raises(TypeError):
            await add.aio.delay(5)

        with pytest.raises(TypeError):
            await add.aio.delay(5, wrong_arg=5)

        # Tasks with typing=False are not checked but execution should fail
        result = await add_not_typed.aio.delay(5)
        with pytest.raises(TypeError):
            await result.get(timeout=5)
        assert (await result.status) == 'FAILURE'

        result = await add_not_typed.aio.delay(5, wrong_arg=5)
        with pytest.raises(TypeError):
            await result.get(timeout=5)
        assert (await result.status) == 'FAILURE'

    async def test_retry(self, manager):
        """Tests retrying of task."""
        # Tests when max. retries is reached
        result = await retry.aio.delay()
        for _ in range(5):
            status = await (result.status)
            if status != 'PENDING':
                break
            await sleep(1)
        assert status == 'RETRY'
        with pytest.raises(ExpectedException):
            await result.get()
        assert (await result.status) == 'FAILURE'

        # Tests when task is retried but after returns correct result
        result = await retry.aio.delay(return_value='bar')
        for _ in range(5):
            status = await (result.status)
            if status != 'PENDING':
                break
            await sleep(1)
        assert status == 'RETRY'
        assert (await result.get()) == 'bar'
        assert (await result.status) == 'SUCCESS'

    async def test_task_accepted(self, manager, sleep=1):
        r1 = await sleeping.aio.delay(sleep)
        await sleeping.aio.delay(sleep)
        manager.assert_accepted([r1.id])

    async def test_task_retried(self):
        res = await retry_once.aio.delay()
        assert (await res.get(timeout=TIMEOUT)) == 1  # retried once

    async def test_task_retried_priority(self):
        res = await retry_once_priority.aio.apply_async(priority=7)
        assert (await res.get(timeout=TIMEOUT)) == 7  # retried once with priority 7

    async def not_yet_test_unicode_task(self, manager):
        manager.join(
            group(print_unicode.s() for _ in range(5))(),
            timeout=TIMEOUT, propagate=True,
        )


class test_task_redis_result_backend(AsyncTest):
    @pytest.fixture(autouse=True)
    def setup(self, redis_server, manager):
        if not manager.app.conf.result_backend.startswith('redis'):
            raise pytest.skip('Requires redis result backend.')
        redis_server.restart()
        time.sleep(1)

    async def test_ignoring_result_no_subscriptions(self):
        assert get_active_redis_channels() == []
        result = await add_ignore_result.aio.delay(1, 2)
        assert result.ignored is True
        assert get_active_redis_channels() == []

    async def test_asyncresult_forget_cancels_subscription(self):
        result = await add.aio.delay(1, 2)
        assert get_active_redis_channels(as_string=True) == [
            f"celery-task-meta-{result.id}"
        ]
        await result.forget()
        assert get_active_redis_channels() == []

    async def test_asyncresult_get_cancels_subscription(self):
        result = await add.aio.delay(1, 2)
        assert get_active_redis_channels(as_string=True) == [
            f"celery-task-meta-{result.id}"
        ]
        assert (await result.get(timeout=3)) == 3
        assert get_active_redis_channels() == []
