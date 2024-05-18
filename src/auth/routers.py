"""Routers for user auth and registration."""

from typing import Annotated

from litestar import get, post, Request
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from dependency_injector.wiring import inject, Provide

from .models.routers import (
    UserLoginRequest,
    UserRegistrationRequest,
    UserLoginResponse,
    UserRegistrationResponse,
    UserLogoutResponse,
)
from .containers import AuthContainer
from .services.auth_handler import AuthHandler


@post("/login", status_code=HTTP_200_OK)
@inject
async def login(
    data: UserLoginRequest,
    auth_handler: Annotated[AuthHandler, Dependency(skip_validation=True)] = Provide[
        AuthContainer.auth_handler
    ],
) -> UserLoginResponse:
    """
    Login user.

    :param data: User's credetinals.
    :param auth_handler: Injected auth request handler.
    :return: Session data.
    """
    return await auth_handler.login(data)


@get("/logout", status_code=HTTP_200_OK)
@inject
async def logout(
    request: Request,
    auth_handler: Annotated[AuthHandler, Dependency(skip_validation=True)] = Provide[
        AuthContainer.auth_handler
    ],
) -> UserLogoutResponse:
    """
    Logout user.

    :param auth_handler: Injected auth request handler.
    :return: Logout status.
    """
    return await auth_handler.logout(request)


@post("/regitstration", status_code=HTTP_201_CREATED)
@inject
async def registration(
    data: UserRegistrationRequest,
    auth_handler: Annotated[AuthHandler, Dependency(skip_validation=True)] = Provide[
        AuthContainer.auth_handler
    ],
) -> UserRegistrationResponse:
    """
    Register new user.

    :param data: User's credetials.
    :param auth_handler: Injected auth request handler.
    :return: Registration status.
    """
    return await auth_handler.registration(data)
