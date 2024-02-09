"""Module for caching logic."""
import redis

from ..models.routers import URL, URLID


class URLCacheRepository:
    """Repository for url cache."""

    def __init__(
            self,
            pool: redis.asyncio.ConnectionPool,
            key_prefix: str = "url",
            default_ttl_sec: float = 60*60*24,
        ):
        self._pool = pool
        self._key_prefix = key_prefix
        self._default_ttl_sec = default_ttl_sec

    def _format_key(self, key: str) -> str:
        return f"{self._key_prefix}_{key}"

    async def save_url(self, url: URL, ttl: float = -1) -> None:
        """
        Save url to cache.

        :param url: Full info.
        :param ttl: Time (seconds) url to be stored cache. Default: -1.
                    If nothing is set, configured default value is used.
        """
        async with redis.asyncio.Redis(pool=self._pool) as connection:
            connection.setex(
                name=self._format_key(url.short),
                value=url.long,
                time=self._default_ttl_sec if ttl < 0 else ttl,
            )

    async def get_url(self, short_url_id: URLID) -> URL | None:
        """
        Get cached url.

        :param short_url_id: Short url id.
        :return: Url info from cache.
        """
        async with redis.asyncio.Redis(pool=self._pool) as connection:
            long_url = connection.get(self._format_key(short_url_id))

        if not long_url:
            return None

        return URL(long=long_url, short=short_url_id)

