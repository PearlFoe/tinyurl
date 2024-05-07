"""Auth errors."""

from src.errors import BaseError


class AuthError(BaseError):
    """Base auth error."""



class TokenGenerationError(AuthError):
    """Error for all problems happening while auth token generation."""
