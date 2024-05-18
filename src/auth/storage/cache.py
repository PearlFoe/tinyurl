"""Module for cache repositories."""

from ..models.token import Token


class UserCacheRepository:
    """Repository for user data caching logic."""

    def __init__(self, token_key_prefix: str = "invalidated") -> None:
        self._token_key_prefix = token_key_prefix

    async def save_invalidated_token(self, token: Token) -> None:
        """
        Save token into blacklist.

        Gets token chached till moment of it's expiration.

        :param token: Token data to save into db.
        """
        ...

    async def check_invalidated(self, token: Token) -> bool:
        """
        Check if token is presented in blacklist.

        :param token: Token data to be checked.
        :return: True if token was found in blacklist, otherwise False.
        """
        ...
