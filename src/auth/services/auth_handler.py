"""Auth requests data handler."""
import asyncio
from functools import partial

from .password import Hash
from .token import JWT
from ..models.routers import UserAuthRequest, UserAuthResponse
from ..storage.db import UserRepository
from ..storage.cache import UserCacheRepository
from ..errors import AuthError


class AuthHandler:
    """Auth requests data handler."""

    def __init__(
            self,
            hash: Hash,
            jwt: JWT,
            db: UserRepository,
            cache: UserCacheRepository
        ) -> None:
        self._hash = hash
        self._jwt = jwt
        self._db = db
        self._cache = cache

    async def login(self, data: UserAuthRequest) -> UserAuthResponse:
        """
        Login user.

        :param data: User login data.
        :return: Response body with login result.
        """
        user = await self._db.get_user(data.login)
        if not user:
            return UserAuthResponse(
                auth_token=None,
                error=str(AuthError())
            )

        chech_pwd_hash = partial(
            self._hash.verify,
            data.password,
            user.password_hash
        )
        loop = asyncio.get_running_loop()
        valid = await loop.run_in_executor(None, chech_pwd_hash)

        if not valid:
            return UserAuthResponse(
                auth_token=None,
                error=str(AuthError())
            )

        return UserAuthResponse()

    async def registration(self, _: UserAuthRequest) -> UserAuthResponse:
        """
        Register user.

        :param data: User registration data.
        :return: Response body with registration result.
        """
        return {}


    async def logout(self) -> None:
        """Logout user."""
        return None

