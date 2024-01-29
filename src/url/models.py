from typing import TypeAlias

from msgspec import Struct


URLID: TypeAlias = str


class ShortenUrlRequest(Struct):
    url: str


class ShortenUrlResponse(Struct):
    url: str
