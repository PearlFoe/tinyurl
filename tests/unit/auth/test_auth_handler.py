import pytest

from src.auth.services.auth_handler import AuthHandler
from src.auth.models.routers import UserAuthRequest, UserAuthResponse
from src.auth.models.users import User
from src.auth.errors import AuthError

class TestAuthHandler:
    async def test_login(
            self,
            auth_handler: AuthHandler,
            auth_request: UserAuthRequest,
            user: User,
        ):
        auth_handler._db.db[user.login] = user
        
        response_body = await auth_handler.login(auth_request)
        
        assert response_body.auth_token is not None
        assert response_body.error is None
        
    async def test_login__user_doesnt_exists(
            self,
            auth_handler: AuthHandler,
            auth_request: UserAuthRequest,
        ):
        auth_handler._db.db.clear()
        
        response_body = await auth_handler.login(auth_request)
        
        assert response_body.auth_token is None
        assert response_body.error == str(AuthError("Invalid login or password."))

    async def test_login__invalid_password(
            self,
            auth_handler: AuthHandler,
            auth_request: UserAuthRequest,
            user: User,
        ):
        user.password_hash = "invalid password hash"
        auth_handler._db.db[user.login] = user
        
        response_body = await auth_handler.login(auth_request)
        
        assert response_body.auth_token is None
        assert response_body.error == str(AuthError("Invalid login or password."))

    @pytest.mark.parametrize(
        "ttl,exception",
        [
            (1, None),
            (0, AssertionError),
            (-1, AssertionError),
        ]
    )
    async def test_count_token_expiration_date(self, ttl: int, exception: Exception, auth_handler: AuthHandler):
        if exception is None:
            assert auth_handler._count_expiration_date(ttl)
        else:
            with pytest.raises(exception):
                auth_handler._count_expiration_date(ttl)