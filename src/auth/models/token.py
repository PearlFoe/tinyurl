"""Auth token data models."""

import datetime

from msgspec import Struct

from .validators import Email


class TokenPayload(Struct):
    """Model for auth token paylod."""

    login: str
    expiration_data: datetime.datetime

    def __post_init__(self) -> None:
        """Validate fields in after init."""
        self.login = Email(self.login)


class Token(Struct):
    """Model for auth token."""

    body: str
    type: str = "Berear"
    payload: TokenPayload | None = None

    def normalize(self) -> str:
        """Format token to string."""
        return f"{self.type}: {self.body}"
