from litestar.testing import TestClient
from httpx import Response


class TestShorteningLogic:
    async def test_shorten__success(
            self,
            client: TestClient,
            shoten_url_request_dict: dict,
            shoten_url_response_dict: dict
        ):
        response: Response = await client.post(
            "api/v1/url/shorten",
            json=shoten_url_request_dict,
        )
        assert response.status_code == 201
        assert response.json() == shoten_url_response_dict

    async def test_shorten__bad_request(
            self,
            client: TestClient,
        ):
        response: Response = await client.post(
            "api/v1/url/shorten",
            json={},
        )
        assert response.status_code == 400


class TestResolveLogic:
    ...
