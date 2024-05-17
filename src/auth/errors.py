"""Auth errors."""

from src.errors import BaseError
from .models.validators import Email


class AuthError(BaseError):
    """Base auth error."""


class InvalidTokenError(AuthError):
    """Error for all problems happening while auth token checks."""

    def __init__(self, message: str = "Invalid auth token.") -> None:
        super().__init__(message)


class TokenGenerationError(AuthError):
    """Error for all problems happening while auth token generation."""

    def __init__(self, message: str = "Failed to generate auth token.") -> None:
        super().__init__(message)


class ExistingLoginError(AuthError):
    """Error for login duplicates."""

    def __init__(self, login: Email | str, message: str = "Login {} already exists.") -> None:
        self.login = login
        message = message.format(login) if "{}" in message else message
        super().__init__(message)
