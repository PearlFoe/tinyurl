"""Module for auth request and response models."""

from typing import Annotated

from msgspec import Struct, Meta

from .validators import Email


# TODO: create separate login/logout/registration data models


class UserAuthRequest(Struct):
    """Login and registration request body model."""

    login: str
    password: Annotated[str, Meta(pattern=r".{8,32}$")]

    def __post_init__(self):
        """Validate fields in after init."""
        self.login = Email(self.login)


class UserAuthResponse(Struct):
    """Login and registration response body model."""

    auth_token: str | None = None# TODO: create custom token validator
    error: str | None = None
