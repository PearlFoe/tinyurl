from src.auth.services.auth_handler import AuthHandler
from src.auth.models.routers import UserAuthRequest, UserAuthResponse

class TestAuthHandler:
    async def test_login(
            self,
            auth_handler: AuthHandler,
            auth_request: UserAuthRequest,
        ):
        response_body = await auth_handler.login(auth_request)
        assert response_body
