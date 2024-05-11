from litestar import status_codes
from litestar.testing import TestClient


class TestAuthRouters:
    async def test_login(
            self,
            client: TestClient,
            auth_request_dict: dict,
        ):
        response = await client.post(url="api/v1/auth/login", json=auth_request_dict)
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
        ):
        response = await client.get(url="api/v1/auth/logout")
        assert response.status_code == status_codes.HTTP_200_OK
        assert response.json() == None

    async def test_logout__invalid_request_method(
            self,
            client: TestClient,
        ):
        response = await client.post(url="api/v1/auth/logout")
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED

    async def test_registration(
            self,
            client: TestClient,
            auth_request_dict: dict,
        ):
        response = await client.post(url="api/v1/auth/regitstration", json=auth_request_dict)
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