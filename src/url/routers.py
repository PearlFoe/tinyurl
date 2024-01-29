from litestar import get, post
from litestar.response.redirect import Redirect

from .models import ShortenUrlRequest, ShortenUrlResponse, URLID


@post("/shorten")
async def shorten(data: ShortenUrlRequest) -> ShortenUrlResponse:
    ...


@get("/{url_id}")
async def resolve(url_id: URLID) -> None:
    ...
