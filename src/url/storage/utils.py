"""Module for store connection utils."""
from typing import AsyncIterator

from pydantic import networks
from redis.asyncio import ConnectionPool, Redis
from asyncpg import create_pool, Connection


async def init_cache_connection_pool(dsn: networks.RedisDsn) -> AsyncIterator[Redis]:
    """Create cache connection pool."""
    async with ConnectionPool.from_url(url=str(dsn)) as pool:
        yield Redis(connection_pool=pool)


async def init_db_connection_pool(dsn: networks.PostgresDsn) -> AsyncIterator[Connection]:
    """Create db connection pool."""
    async with create_pool(dsn=str(dsn)) as pool:
        yield await pool.acquire()
