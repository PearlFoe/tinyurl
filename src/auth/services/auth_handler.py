"""Auth requests data handler."""
import asyncio
import datetime
from functools import partial

import msgspec

from .password import Hash
from .token import JWT
from ..models.routers import UserAuthRequest, UserAuthResponse
from ..models.token import TokenPayload
from ..models.validators import Email, enc_hook
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
            cache: UserCacheRepository,
            token_ttl_sec: int,
        ) -> None:
        self._hash = hash
        self._jwt = jwt
        self._db = db
        self._cache = cache
        self._token_ttl_sec = token_ttl_sec

    def _count_expiration_date(
            self,
            ttl_sec: int,
            timezone: datetime.timezone = datetime.UTC
        ) -> datetime.datetime:
        assert ttl_sec > 0, "Token ttl can't be negative or equal to zero."
        return datetime.datetime.now(timezone) + datetime.timedelta(seconds=ttl_sec)

    def _auth_token_payload(self, login: Email) -> TokenPayload:
        return TokenPayload(
            login=login,
            expiration_data=self._count_expiration_date(self._token_ttl_sec)
        )

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
                error=str(AuthError("Invalid login or password."))
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
                error=str(AuthError("Invalid login or password."))
            )

        payload = self._auth_token_payload(user.login)
        payload = msgspec.to_builtins(payload, enc_hook=enc_hook)
        token = self._jwt.generate(payload)

        return UserAuthResponse(auth_token=token)

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

