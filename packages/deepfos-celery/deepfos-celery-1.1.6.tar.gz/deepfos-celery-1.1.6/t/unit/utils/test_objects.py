from celery.utils.objects import Bunch
from celery.utils.objects import AsyncFallbackContext
from contextlib import asynccontextmanager
import asyncio

import pytest


class Connection:
    def __init__(self):
        self._connected = False

    async def connect(self):
        self._connected = True

    @property
    def connected(self):
        return self._connected

    async def close(self):
        self._connected = False


@asynccontextmanager
async def create_new_connection():
    conn = Connection()
    await conn.connect()
    try:
        yield conn
    finally:
        await conn.close()


def connection_or_default_connection(connection=None):
    return AsyncFallbackContext(connection, create_new_connection)


@pytest.mark.asyncio
async def test_AsyncFallbackContext_fallback():
    async with connection_or_default_connection() as conn:
        assert conn.connected
    assert not conn.connected


@pytest.mark.asyncio
async def test_AsyncFallbackContext_default():
    connection = Connection()
    async with connection_or_default_connection(connection) as conn:
        assert conn is connection
        assert not conn.connected


class test_Bunch:

    def test(self):
        x = Bunch(foo='foo', bar=2)
        assert x.foo == 'foo'
        assert x.bar == 2
