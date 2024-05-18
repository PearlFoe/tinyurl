from litestar import status_codes
from litestar.testing import TestClient

from src.auth.models.token import Token
from src.auth.settings import AuthSettings


class TestAuthRouters:
    async def test_login(
        self,
        client: TestClient,
        login_request_dict: dict,
    ):
        response = await client.post(url="api/v1/auth/login", json=login_request_dict)
        assert response.status_code == status_codes.HTTP_200_OK

    async def test_login__invalid_request_method(
        self,
        client: TestClient,
    ):
        response = await client.get(url="api/v1/auth/login")
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED

    async def test_login__empty_body(
        self,
        client: TestClient,
    ):
        response = await client.post(url="api/v1/auth/login", json={})
        assert response.status_code == status_codes.HTTP_400_BAD_REQUEST

    async def test_logout(
        self,
        client: TestClient,
        auth_token: Token,
        auth_settings: AuthSettings,
    ):
        response = await client.get(
            url="api/v1/auth/logout", headers={auth_settings.token_header_name: auth_token.normalize()}
        )
        assert response.status_code == status_codes.HTTP_200_OK

    async def test_logout__invalid_request_method(
        self,
        client: TestClient,
    ):
        response = await client.post(url="api/v1/auth/logout")
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED

    async def test_registration(
        self,
        client: TestClient,
        registration_request_dict: dict,
    ):
        response = await client.post(url="api/v1/auth/regitstration", json=registration_request_dict)
        assert response.status_code == status_codes.HTTP_201_CREATED

    async def test_registration__invalid_request_method(
        self,
        client: TestClient,
    ):
        response = await client.get(url="api/v1/auth/regitstration")
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED

    async def test_registration__empty_body(
        self,
        client: TestClient,
    ):
        response = await client.post(url="api/v1/auth/regitstration", json={})
        assert response.status_code == status_codes.HTTP_400_BAD_REQUEST
