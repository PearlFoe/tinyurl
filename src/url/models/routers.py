"""Request and response data models."""

from msgspec import Struct


class ShortenUrlRequest(Struct):
    """Shorten request body model."""

    url: str


class ShortenUrlResponse(Struct):
    """Shorten response body model."""

    url: str
