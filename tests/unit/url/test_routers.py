from litestar.testing import TestClient
from litestar import status_codes
from httpx import Response

from src.url.models.routers import URL
from src.url.url_handlers import URLHandler


class TestShorteningLogic:
    async def test_shorten__success(
            self,
            monkeypatch,
            url: URL,
            client: TestClient,
            shoten_url_request_dict: dict,
            shoten_url_response_dict: dict,
        ):
        with monkeypatch.context() as context:
            context.setattr(
                "src.url.models.routers.random.choices",
                lambda _, k: list(url.short)
            )

            response: Response = await client.post(
                "api/v1/url/shorten",
                json=shoten_url_request_dict,
            )
        assert response.status_code == status_codes.HTTP_201_CREATED
        assert response.json() == shoten_url_response_dict

    async def test_shorten__bad_request(
            self,
            client: TestClient,
        ):
        response: Response = await client.post(
            "api/v1/url/shorten",
            json={},
        )
        assert response.status_code == status_codes.HTTP_400_BAD_REQUEST

    async def test_shorten__method_not_allowed(
            self,
            client: TestClient,
        ):
        response: Response = await client.get(
            "api/v1/url/shorten",
        )
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED


class TestResolveLogic:
    async def test_resolve__success(
            self,
            client: TestClient,
            url: URL,
            url_handler: URLHandler,
        ):
        url_handler._db.data[url.short] = url
        response: Response = await client.get(
            str(url.short),
            follow_redirects=False,
        )
        assert response.status_code == status_codes.HTTP_307_TEMPORARY_REDIRECT

    async def test_resolve__url_doesnt_exist(
            self,
            client: TestClient,
            url: URL,
        ):
        response: Response = await client.get(
            str(url.short),
            follow_redirects=False,
        )
        assert response.status_code == status_codes.HTTP_404_NOT_FOUND

    async def test_resolve__bad_request(
            self,
            client: TestClient,
        ):
        response: Response = await client.get(
            "/a*",
            follow_redirects=False,
        )
        assert response.status_code == status_codes.HTTP_400_BAD_REQUEST

    async def test_resolve__method_not_allowed(
            self,
            client: TestClient,
            url: URL,
        ):
        response: Response = await client.post(
            str(url.short),
            follow_redirects=False,
        )
        assert response.status_code == status_codes.HTTP_405_METHOD_NOT_ALLOWED
