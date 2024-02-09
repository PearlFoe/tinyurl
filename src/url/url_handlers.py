"""Handlers for url requests."""
from .models.routers import ShortenUrlRequest, URL, URLID
from .storage.db import URLRepository
from .storage.cache import URLCacheRepository


class URLHandler:
    """Handler for url creatind and resolving logic."""

    def __init__(self, db: URLRepository, cache: URLCacheRepository) -> None:
        self._db = db
        self._cache = cache

    async def _save_url(self, url: URL) -> None:
        await self._db.save_url(url)

    async def _get_url(self, short_url_id: URLID) -> URL | None:
        cached_url = await self._cache.get_url(short_url_id)
        if cached_url:
            return cached_url

        url = await self._db.get_url(short_url_id)
        if url:
            await self._cache.save_url(url)

        return url

    async def save_url(self, request_body: ShortenUrlRequest) -> URL:
        """
        Save url to storage.

        :param request_body: Request body with long url.
        :return: URL object with short id.
        """
        url = URL(long=request_body.url)
        url.generate_short_id()

        await self._save_url(url)

        return url

    async def get_url(self, short_url_id: URLID) -> URL | None:
        """
        Get url from storage.

        Lasy caching implemented. If url is cached
        it would be returned. Otherwise it would be selected
        from db and cached.

        :param short_url_id: Short url id from path.
        :return: URL object with full id.
        """
        return await self._get_url(short_url_id)
