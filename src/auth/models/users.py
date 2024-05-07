"""Module for user data models."""

from msgspec import Struct

from .validators import Email


class User(Struct):
    """User data model."""

    login: Email
    password_hash: str
    user_id: int | None = None

    def __post_init__(self) -> None:
        """Validate fields in after init."""
        self.login = Email(self.login)
