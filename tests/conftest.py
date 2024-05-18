import datetime

import msgspec
import pytest
from litestar import Litestar, Request
from litestar.types.asgi_types import HTTPScope
from litestar.testing import AsyncTestClient

from src.main import get_app

from src.auth.settings import AuthSettings
from src.auth.models.validators import enc_hook
from src.auth.models.users import User
from src.auth.models.token import Token, TokenPayload
from src.auth.models.routers import UserLoginRequest, UserRegistrationRequest
from src.auth.containers import AuthContainer
from src.auth.services.token import JWT

from src.url.settings import URLSettings
from src.url.models.routers import ShortenUrlRequest, ShortenUrlResponse
from src.url.models.urls import URL
from src.url.containers import URLContainer

from .mocks.url_repositories import URLRepositoryMock, URLCacheRepositoryMock
from .mocks.auth_repositories import UserRepositoryMock, UserCacheRepository
from .mocks.password import MockedHash as Hash


@pytest.fixture(scope="function")
def url_settings():
    return URLSettings()


@pytest.fixture(scope="function")
def url_container(url_settings: URLSettings):
    container = URLContainer()

    container.env.from_dict(url_settings.model_dump())
    container.db_repository.override(URLRepositoryMock())
    container.cache_repository.override(URLCacheRepositoryMock())

    return container


@pytest.fixture(scope="function")
def auth_settings():
    return AuthSettings()


@pytest.fixture(scope="function")
def auth_container(auth_settings: AuthSettings):
    container = AuthContainer()

    container.env.from_dict(auth_settings.model_dump())
    container.user_repository.override(UserRepositoryMock())
    container.user_cache_repository.override(UserCacheRepository())
    container.hash.override(Hash())

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
def user():
    return User(
        login="test@gmail.com",
        password_hash=Hash.generate("password"),
        user_id=1,
    )


@pytest.fixture(scope="function")
def auth_token(auth_settings: AuthSettings, auth_container: AuthContainer):
    payload = TokenPayload(
        login="test@gmail.com",
        expiration_data=(
            datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=auth_settings.token_ttl_sec)
        ),
    )
    jwt = auth_container.jwt()
    return Token(
        body=jwt.generate(msgspec.to_builtins(payload, enc_hook=enc_hook)),
        payload=payload,
    )


@pytest.fixture(scope="function")
def empty_request():
    scope = {
        "app": None,
        "asgi": {"spec_version": "2.0", "version": "3.0"},
        "auth": None,
        "type": type,
        "path": "/",
        "raw_path": "/".encode(),
        "root_path": "",
        "scheme": "http",
        "query_string": "".encode(),
        "client": ("testclient", 50000),
        "server": ("testserver", 80),
        "method": "GET",
        "http_version": "1.1",
        "extensions": {"http.response.template": {}},
        "state": {},
        "path_params": {},
        "route_handler": None,
        "user": None,
        "session": None,
        "headers": {},
    }
    return Request(scope=HTTPScope(scope))


@pytest.fixture(scope="function")
def login_request():
    return UserLoginRequest(login="test@gmail.com", password="password")


@pytest.fixture(scope="function")
def login_request_dict(login_request: UserLoginRequest):
    return msgspec.to_builtins(login_request, enc_hook=enc_hook)


@pytest.fixture(scope="function")
def registration_request():
    return UserRegistrationRequest(login="test@gmail.com", password="password")


@pytest.fixture(scope="function")
def registration_request_dict(registration_request: UserRegistrationRequest):
    return msgspec.to_builtins(registration_request, enc_hook=enc_hook)


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
    return ShortenUrlRequest(url=url.long)


@pytest.fixture(scope="function")
def shoten_url_request_dict(shoten_url_request: ShortenUrlRequest):
    return msgspec.to_builtins(shoten_url_request)


@pytest.fixture(scope="function")
def shoten_url_response(short_url: str):
    return ShortenUrlResponse(url=short_url)


@pytest.fixture(scope="function")
def shoten_url_response_dict(shoten_url_response: ShortenUrlResponse):
    return msgspec.to_builtins(shoten_url_response)
