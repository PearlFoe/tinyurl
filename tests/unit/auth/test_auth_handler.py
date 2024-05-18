import pytest
from litestar import Request

from src.auth.services.auth_handler import AuthHandler
from src.auth.models.token import Token
from src.auth.models.routers import UserLoginRequest, UserRegistrationRequest, AuthResponseStatus
from src.auth.models.users import User
from src.auth.errors import AuthError, ExistingLoginError
from src.auth.settings import AuthSettings


class TestAuthHandler:
    @pytest.mark.parametrize(
        "ttl,exception",
        [
            (1, None),
            (0, AssertionError),
            (-1, AssertionError),
        ],
    )
    async def test_count_token_expiration_date(
        self, ttl: int, exception: Exception, auth_handler: AuthHandler
    ):
        if exception is None:
            assert auth_handler._count_expiration_date(ttl)
        else:
            with pytest.raises(exception):
                auth_handler._count_expiration_date(ttl)

    async def test_login(
        self,
        auth_handler: AuthHandler,
        login_request: UserLoginRequest,
        user: User,
    ):
        auth_handler._db.db[user.login] = user

        response_body = await auth_handler.login(login_request)

        assert response_body.status == AuthResponseStatus.SUCCESS
        assert response_body.auth_token is not None
        assert response_body.error is None

    async def test_login__user_doesnt_exists(
        self,
        auth_handler: AuthHandler,
        login_request: UserLoginRequest,
    ):
        auth_handler._db.db.clear()

        response_body = await auth_handler.login(login_request)

        assert response_body.status == AuthResponseStatus.ERROR
        assert response_body.auth_token is None
        assert response_body.error == str(AuthError("Invalid login or password."))

    async def test_login__invalid_password(
        self,
        auth_handler: AuthHandler,
        login_request: UserLoginRequest,
        user: User,
    ):
        user.password_hash = "invalid password hash"
        auth_handler._db.db[user.login] = user

        response_body = await auth_handler.login(login_request)

        assert response_body.status == AuthResponseStatus.ERROR
        assert response_body.auth_token is None
        assert response_body.error == str(AuthError("Invalid login or password."))

    async def test_registration(
        self,
        auth_handler: AuthHandler,
        registration_request: UserRegistrationRequest,
    ):
        auth_handler._db.db.clear()

        response_body = await auth_handler.registration(registration_request)

        assert registration_request.login in auth_handler._db.db
        assert response_body.status == AuthResponseStatus.SUCCESS
        assert response_body.error is None

    async def test_registration__user_already_exists(
        self,
        auth_handler: AuthHandler,
        registration_request: UserRegistrationRequest,
        user: User,
    ):
        auth_handler._db.db[user.login] = user

        response_body = await auth_handler.registration(registration_request)

        assert response_body.status == AuthResponseStatus.ERROR
        assert response_body.error == str(ExistingLoginError(user.login))

    async def test_logout(
        self,
        auth_handler: AuthHandler,
        empty_request: Request,
        auth_settings: AuthSettings,
        auth_token: Token,
    ):
        auth_handler._cache.db.clear()
        empty_request.scope["headers"] = {auth_settings.token_header_name: auth_token.normalize()}

        response_body = await auth_handler.logout(empty_request)

        assert f"invalidated_{auth_token.body}" in auth_handler._cache.db
        assert response_body.status == AuthResponseStatus.SUCCESS
        assert response_body.error is None
