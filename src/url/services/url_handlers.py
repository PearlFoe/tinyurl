"""Handlers for url requests."""
from ..models.routers import ShortenUrlRequest
from ..models.urls import URL, URLID
from .storage import URLStorage


class URLHandler:
    """Handler for url creatind and resolving logic."""

    def __init__(self, storage: URLStorage) -> None:
        self._url_storage = storage

    async def save_url(self, request_body: ShortenUrlRequest) -> URL:
        """
        Save url to storage.

        :param request_body: Request body with long url.
        :return: URL object with short id.
        """
        url = URL(long=request_body.url)
        url.generate_short_id()

        await self._url_storage.save_url(url)

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
        return await self._url_storage.get_url(short_url_id)
