"""Auth errors."""

from src.errors import BaseError


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
