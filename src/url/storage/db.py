"""Module for db repositories."""
import asyncpg

from ..models.routers import URL, URLID
from .queries.query_builders import Queries


class URLRepository:
    """Repository for url database."""

    def __init__(self, pool: asyncpg.Pool, queries: Queries):
        self._pool = pool
        self._queries = queries

    async def save_url(self, url: URL) -> None:
        """
        Save url to database.

        :param url: Url info to save.
        """
        async with self._pool.acquire() as connection:
            await self._queries.save_url(
                connection=connection,
                long_url=url.long,
                short_url=url.short,
            )

    async def get_url(self, short_url_id: URLID) -> URL:
        """
        Get url from database.

        :param short_url_id: Short url id.
        :return: Url info from database.
        """
        async with self._pool.acquire() as connection:
            long_url = await self._queries.save_url(
                connection=connection,
                short_url=short_url_id,
            )

        return URL(long=long_url, short=short_url_id)
