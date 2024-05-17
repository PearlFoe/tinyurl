"""Module for auth settings models."""

from src.settings import Settings


class AuthSettings(Settings):
    """Model for parsing auth settings from .env file."""

    secret: str

    token_header_name: str
    token_ttl_sec: int
