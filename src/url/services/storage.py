"""URL stoing and accessing logic."""

from ..models.urls import URL, URLID
from ..storage.db import URLRepository
from ..storage.cache import URLCacheRepository


class URLStorage:
    """Handels url storing and accessing logic."""

    def __init__(self, db: URLRepository, cache: URLCacheRepository) -> None:
        self._db = db
        self._cache = cache

    async def save_url(self, url: URL) -> None:
        """
        Save url to storage.

        TODO: add caching on write

        :param url: URL data.
        """
        await self._db.save_url(url)

    async def get_url(self, short_url_id: URLID) -> URL | None:
        """
        Get url data from storage.

        :param short_url_id: short if of a long url.
        :return: URL data or None if it is not longer available.
        """
        cached_url = await self._cache.get_url(short_url_id)
        if cached_url:
            return cached_url

        url = await self._db.get_url(short_url_id)
        if url:
            await self._cache.save_url(url)

        return url
