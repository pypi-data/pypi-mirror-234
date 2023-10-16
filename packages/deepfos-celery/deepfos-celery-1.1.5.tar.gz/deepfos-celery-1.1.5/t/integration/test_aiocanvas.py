import pytest

from celery.aio.result import GroupResult
from celery.aio.canvas import group
from t.base import AsyncFlakyTest, FlakyMixin

from .tasks import (ExpectedException, add, add_chord_to_chord, add_replaced,
                    add_to_all, add_to_all_to_chord, build_chain_inside_task,
                    chord_error, collect_ids, delayed_sum,
                    delayed_sum_with_soft_guard, fail, identity, ids,
                    print_unicode, raise_error, redis_echo,
                    replace_with_chain, replace_with_chain_which_raises,
                    replace_with_empty_chain, retry_once, return_exception,
                    return_priority, second_order_replace1, tsum)

from .test_canvas import assert_ping, TIMEOUT


class test_group(AsyncFlakyTest):
    async def test_ready_with_exception(self, manager):
        if not manager.app.conf.result_backend.startswith('redis'):
            raise pytest.skip('Requires redis result backend.')

        g = group([add.aio.s(1, 2), raise_error.aio.s()])
        result = await g.apply_async()
        while not await result.ready():
            pass

    async def test_empty_group_result(self, manager):
        if not manager.app.conf.result_backend.startswith('redis'):
            raise pytest.skip('Requires redis result backend.')

        task = group([])
        result = await task.apply_async()

        await GroupResult.save(result)
        task = await GroupResult.restore(result.id)
        assert task.results == []

    async def test_nested_group(self, manager):
        assert_ping(manager)

        c = group(
            add.aio.si(1, 10),
            group(
                add.aio.si(1, 100),
                group(
                    add.aio.si(1, 1000),
                    add.aio.si(1, 2000),
                ),
            ),
        )
        res = await c()

        assert await res.get(timeout=TIMEOUT) == [11, 101, 1001, 2001]

    async def test_large_group(self, manager):
        assert_ping(manager)

        c = group(identity.aio.s(i) for i in range(1000))
        res = await c.delay()

        assert await res.get(timeout=TIMEOUT) == list(range(1000))

    async def test_group_lone(self, manager):
        """
        Test that a simple group completes.
        """
        sig = group(identity.aio.s(42), identity.aio.s(42))     # [42, 42]
        res = await sig.delay()
        assert await res.get(timeout=TIMEOUT) == [42, 42]

    async def test_nested_group_group(self, manager):
        """
        Confirm that groups nested inside groups get unrolled.
        """
        sig = group(
            group(identity.aio.s(42), identity.aio.s(42)),  # [42, 42]
        )                                       # [42, 42] due to unrolling
        res = await sig.delay()
        assert await res.get(timeout=TIMEOUT) == [42, 42]

    async def test_group_restore_fast(self):
        sig = group(
            group(identity.aio.s(42), identity.aio.s(42)),  # [42, 42]
        )
        g = await sig.delay()
        await g.save()
        g_clone = await GroupResult.restore(g.id)
        assert await g_clone.get(timeout=5) == [42, 42]

    async def test_group_restore_slow(self):
        sig = group(
            group(delayed_sum.aio.s([40, 2]), delayed_sum.aio.s([2, 40], 2)),  # [42, 42]
        )
        g = await sig.delay()
        await g.save()
        g_clone = await GroupResult.restore(g.id)
        assert await g_clone.get(timeout=6) == [42, 42]
