"""Data models for url package."""

import random
from string import ascii_letters, digits
from typing import TypeAlias

from msgspec import Struct

from .constants import URL_ID_LENGTH


URLID: TypeAlias = str


class ShortenUrlRequest(Struct):
    """Shorten request body model."""

    url: str


class ShortenUrlResponse(Struct):
    """Shorten response body model."""

    url: str


class URL(Struct):
    """URL data model."""

    long: str
    short: URLID | None

    def generate_short_id(self, length: int=URL_ID_LENGTH) -> None:
        """Generate random short url id of porvided length."""
        symbols = random.choices(
            ascii_letters + digits,
            k=length
        )

        self.short = "".join(symbols)
