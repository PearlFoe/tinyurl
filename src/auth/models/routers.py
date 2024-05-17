"""Module for auth request and response models."""

from enum import StrEnum, auto
from typing import Annotated

from msgspec import Struct, Meta

from .validators import Email


class UserAuthRequest(Struct):
    """Base request body model."""

    login: str
    password: Annotated[str, Meta(pattern=r".{8,32}$")]

    def __post_init__(self):
        """Validate fields in after init."""
        self.login = Email(self.login)


class UserLoginRequest(UserAuthRequest):
    """Login request body model."""


class UserRegistrationRequest(UserAuthRequest):
    """Registration request body model."""


class AuthResponseStatus(StrEnum):
    """Possible auth reponses statuses."""

    SUCCESS = auto()
    ERROR = auto()


class UserAuthReponse(Struct):
    """Base response body model."""

    status: AuthResponseStatus = None
    error: str | None = None


class UserLoginResponse(UserAuthReponse):
    """Login response body model."""

    auth_token: str | None = None  # TODO: create custom token validator


class UserRegistrationResponse(UserAuthReponse):
    """Registration response body model."""


class UserLogoutResponse(UserAuthReponse):
    """Logout response body model."""
