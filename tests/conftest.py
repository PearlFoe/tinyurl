import msgspec
import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.main import get_app

from src.auth.settings import AuthSettings
from src.auth.models.validators import enc_hook
from src.auth.models.routers import UserAuthRequest, UserAuthResponse
from src.auth.containers import AuthContainer

from src.url.settings import URLSettings
from src.url.models.routers import ShortenUrlRequest, ShortenUrlResponse
from src.url.models.urls import URL
from src.url.containers import URLContainer

from .mocks.url_repositories import URLRepositoryMock, URLCacheRepositoryMock
from .mocks.auth_repositories import UserRepositoryMock, UserCacheRepository


@pytest.fixture(scope="function")
def url_container():
    container = URLContainer()
    settings = URLSettings()

    container.env.from_dict(settings.model_dump())
    container.db_repository.override(URLRepositoryMock())
    container.cache_repository.override(URLCacheRepositoryMock())

    return container


@pytest.fixture(scope="function")
def auth_container():
    container = AuthContainer()
    settings = AuthSettings()

    container.env.from_dict(settings.model_dump())
    container.user_repository.override(UserRepositoryMock())
    container.user_cache_repository.override(UserCacheRepository())
    
    return container


@pytest.fixture(scope="function")
def containers(
        auth_container: AuthContainer,
        url_container: URLContainer,
    ):
    return (
        auth_container,
        url_container,
    )


@pytest.fixture(scope="function")
def app(containers: tuple):
    app = get_app(containers)
    app.debug = True
    return app


@pytest.fixture(scope="function")
async def client(app: Litestar):
    async with AsyncTestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def auth_request():
    return UserAuthRequest(
        login="test@gmail.com", 
        password="password"
    )


@pytest.fixture(scope="function")
def auth_request_dict(auth_request: UserAuthRequest):
    return msgspec.to_builtins(auth_request, enc_hook=enc_hook)
    

@pytest.fixture(scope="function")
def auth_handler(auth_container: AuthContainer):
    return auth_container.auth_handler()
    

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
        url_container: URLContainer, 
    ):
    return url_container.url_handler()


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
