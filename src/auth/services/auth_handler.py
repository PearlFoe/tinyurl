"""Auth requests data handler."""

import asyncio
import datetime
from functools import partial

import msgspec
from litestar import Request

from .password import Hash
from .token import JWT
from ..models.routers import (
    UserLoginRequest,
    UserRegistrationRequest,
    UserLoginResponse,
    UserRegistrationResponse,
    UserLogoutResponse,
    AuthResponseStatus,
)
from ..models.token import TokenPayload, Token
from ..models.validators import Email, enc_hook
from ..models.users import User
from ..storage.db import UserRepository
from ..storage.cache import UserCacheRepository
from ..errors import AuthError, ExistingLoginError


class AuthHandler:
    """Auth requests data handler."""

    def __init__(
        self,
        hash: Hash,
        jwt: JWT,
        db: UserRepository,
        cache: UserCacheRepository,
        token_ttl_sec: int,
        token_header_name: str,
    ) -> None:
        self._hash = hash
        self._jwt = jwt
        self._db = db
        self._cache = cache
        self._token_ttl_sec = token_ttl_sec
        self._token_header_name = token_header_name

    def _count_expiration_date(
        self, ttl_sec: int, timezone: datetime.timezone = datetime.UTC
    ) -> datetime.datetime:
        assert ttl_sec > 0, "Token ttl can't be negative or equal to zero."
        return datetime.datetime.now(timezone) + datetime.timedelta(seconds=ttl_sec)

    def _auth_token_payload(self, login: Email) -> TokenPayload:
        return TokenPayload(login=login, expiration_data=self._count_expiration_date(self._token_ttl_sec))

    def _get_auth_token(self, request: Request) -> Token:
        """
        Get auth token from auth header.

        :param request: Request object with auth header..
        :return: Token data.
        """
        token_type, token = request.headers[self._token_header_name].split(" ", maxsplit=1)
        payload = self._jwt.validate(token)

        return Token(
            body=token,
            type=token_type,
            payload=payload,
        )

    async def login(self, data: UserLoginRequest) -> UserLoginResponse:
        """
        Login user.

        :param data: User login data.
        :return: Response body with login result.
        """
        user = await self._db.get_user(data.login)
        if not user:
            return UserLoginResponse(
                status=AuthResponseStatus.ERROR,
                error=str(AuthError("Invalid login or password.")),
            )

        chech_pwd_hash = partial(self._hash.verify, data.password, user.password_hash)
        loop = asyncio.get_running_loop()
        valid = await loop.run_in_executor(None, chech_pwd_hash)

        if not valid:
            return UserLoginResponse(
                status=AuthResponseStatus.ERROR,
                error=str(AuthError("Invalid login or password.")),
            )

        payload = self._auth_token_payload(user.login)
        payload = msgspec.to_builtins(payload, enc_hook=enc_hook)
        token = self._jwt.generate(payload)

        return UserLoginResponse(
            status=AuthResponseStatus.SUCCESS,
            auth_token=token,
        )

    async def registration(self, data: UserRegistrationRequest) -> UserRegistrationResponse:
        """
        Register user.

        :param data: User registration data.
        :return: Response body with registration result.
        """
        user = await self._db.get_user(data.login)
        if user:
            return UserRegistrationResponse(
                status=AuthResponseStatus.ERROR, error=str(ExistingLoginError(login=data.login))
            )

        generate_pwd_hash = partial(self._hash.generate, data.password)
        loop = asyncio.get_running_loop()
        hash = await loop.run_in_executor(None, generate_pwd_hash)

        user = User(
            login=data.login,
            password_hash=hash,
        )

        await self._db.create_user(user)

        return UserRegistrationResponse(
            status=AuthResponseStatus.SUCCESS,
        )

    async def logout(self, request: Request) -> UserLogoutResponse:
        """
        Logout user.

        :param request: Request object with auth header.
        :return: Response body with logout result.
        """
        token = self._get_auth_token(request)
        await self._cache.save_invalidated_token(token)
        return UserLogoutResponse(
            status=AuthResponseStatus.SUCCESS,
        )
