"""Auth errors."""

from src.errors import BaseError


class AuthError(BaseError):
    """Base auth error."""


class InvalidTokenError(AuthError):
    """Error for all problems happening while auth token checks."""


class TokenGenerationError(AuthError):
    """Error for all problems happening while auth token generation."""
