import msgspec
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.app import get_app
from src.url.models.routers import URL, URLID, ShortenUrlRequest, ShortenUrlResponse
from src.url.containers import Container
from src.url.url_handlers import URLHandler
from src.url.storage.db import URLRepository


@pytest.fixture(scope="function")
def url_container(url_handler: URLHandler):
    container = Container()

    container.url_handler.override(url_handler)

    return container


@pytest.fixture(scope="function")
def containers(url_container: Container):
    return (
        url_container,
    )


@pytest.fixture(scope="function")
def app(containers: tuple):
    app = get_app(containers)
    return app


@pytest.fixture(scope="function")
async def client(app: Litestar):
    async with AsyncTestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def url():
    url = URL(
        long="https://google.com",
    )
    url.generate_short_id()
    return url


@pytest.fixture(scope="function")
def url_db_repository_mock():
    class URLRepositoryMock:
        def __init__(self) -> None:
            self._data: dict[URLID, URL] = {}

        async def save_url(self, url: URL) -> None:
            self._data[url.short] = url

        async def get_url(self, short_url_id: URLID) -> URL:
            return self._data[short_url_id]

    return URLRepositoryMock()


@pytest.fixture(scope="function")
def url_handler(url: URL, url_db_repository_mock: URLRepository):
    handler = URLHandler(
        db=url_db_repository_mock
    )

    handler._db._data[url.short] = url

    return handler


@pytest.fixture(scope="function")
def short_url(url: URL):
    return f"http://testserver.local/{url.short}"


@pytest.fixture(scope="function")
def shoten_url_request(url: URL):
    return ShortenUrlRequest(
        url=url.long
    )


@pytest.fixture(scope="function")
def shoten_url_request_dict(shoten_url_request: ShortenUrlRequest):
    return msgspec.to_builtins(shoten_url_request)


@pytest.fixture(scope="function")
def shoten_url_response(short_url: str):
    return ShortenUrlResponse(
        url=short_url
    )


@pytest.fixture(scope="function")
def shoten_url_response_dict(shoten_url_response: ShortenUrlResponse):
    return msgspec.to_builtins(shoten_url_response)
