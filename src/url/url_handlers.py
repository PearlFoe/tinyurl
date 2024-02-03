"""Handlers for url requests."""
from .models import ShortenUrlRequest, URL, URLID


class URLHandler:
    """Handler for url creatind and resolving logic."""

    def __init__(self) -> None:
        ...

    async def _save_url(self, url: URL) -> None:
        ...

    async def _get_url(self, short_url_id: URLID) -> URL:
        ...

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

    async def get_url(self, short_url_id: URLID) -> URL:
        """
        Get url from storage.

        :param short_url_id: Short url id from path.
        :return: URL object with full id.
        """
        return await self._get_url(short_url_id)
