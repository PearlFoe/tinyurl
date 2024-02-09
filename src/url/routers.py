"""Routers for url shortening and resolving."""

from typing import Annotated

from litestar import get, post, Request, exceptions
from litestar.response.redirect import Redirect
from litestar.params import Dependency, Parameter
from litestar.status_codes import HTTP_201_CREATED, HTTP_307_TEMPORARY_REDIRECT
from dependency_injector.wiring import inject, Provide

from .models.routers import ShortenUrlRequest, ShortenUrlResponse, URLID, URLID_PATTERN
from .containers import Container
from .url_handlers import URLHandler


@post("/shorten", status_code=HTTP_201_CREATED)
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
    print(id(url_handler))
    url = await url_handler.save_url(data)

    request_url = request.url
    short_url = f"{request_url.scheme}://{request_url.hostname}/{url.short}"

    return ShortenUrlResponse(url=short_url)


@get("/{url_id:str}", status_code=HTTP_307_TEMPORARY_REDIRECT)
@inject
async def resolve(
        url_id: Annotated[URLID, Parameter(pattern=URLID_PATTERN)],
        url_handler: Annotated[URLHandler, Dependency(skip_validation=True)] = Provide[Container.url_handler],
    ) -> Redirect:
    """
    Redirect from short url to long version.

    :param url_id: Short url id.
    :return: Redirects to long url.
    """
    url = await url_handler.get_url(url_id)
    if not url:
        raise exceptions.NotFoundException()
    return Redirect(url.long, status_code=HTTP_307_TEMPORARY_REDIRECT)
