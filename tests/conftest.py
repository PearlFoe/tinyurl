import msgspec
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.main import get_app
from src.url.settings import Settings
from src.url.models.routers import URL, ShortenUrlRequest, ShortenUrlResponse
from src.url.containers import Container
from src.url.url_handlers import URLHandler

from .mocks.url_repositories import URLRepositoryMock, URLCacheRepositoryMock


@pytest.fixture(scope="function")
def url_container(url_handler: URLHandler):
    container = Container()
    settings = Settings()

    container.env.from_dict(settings.model_dump())
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
    return URLRepositoryMock()


@pytest.fixture(scope="function")
def url_cache_repository_mock():
    return URLCacheRepositoryMock()


@pytest.fixture(scope="function")
def url_handler(
        url_db_repository_mock: URLRepositoryMock,
        url_cache_repository_mock: URLCacheRepositoryMock
    ):
    handler = URLHandler(
        db=url_db_repository_mock,
        cache=url_cache_repository_mock,
    )
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
