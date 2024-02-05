"""Routers for url shortening and resolving."""

from typing import Annotated

from litestar import get, post, Request
from litestar.response.redirect import Redirect
from litestar.params import Dependency
from dependency_injector.wiring import inject, Provide

from .models import ShortenUrlRequest, ShortenUrlResponse, URLID
from .containers import Container
from .url_handlers import URLHandler


@post("/shorten")
@inject
async def shorten(
        request: Request,
        data: ShortenUrlRequest,
        url_handler: Annotated[URLHandler, Dependency(skip_validation=True)] = Provide[Container.url_handler],
    ) -> ShortenUrlResponse:
    """
    Make short url from long.

    :param data: Request body with long url.
    :return: Response body with short version of long url.
    """
    url = await url_handler.save_url(data)

    request_url = request.url
    short_url = f"{request_url.scheme}://{request_url.hostname}/{url.short}"

    return ShortenUrlResponse(url=short_url)


@get("/{url_id:str}")
@inject
async def resolve(
        url_id: URLID,
        url_handler: Annotated[URLHandler, Dependency(skip_validation=True)] = Provide[Container.url_handler],
    ) -> None:
    """
    Redirect from short url to long version.

    :param url_id: Short url id.
    :return: Redirects to long url.
    """
    url = await url_handler.get_url(url_id)
    return Redirect(url.long)
