"""Routers for user auth and registration."""

from typing import Annotated

from litestar import get, post
from litestar.params import Dependency
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from dependency_injector.wiring import inject, Provide

from .containers import AuthContainer
from .models.routers import UserAuthRequest, UserAuthResponse
from .services.auth_handler import AuthHandler


@post("/login", status_code=HTTP_200_OK)
@inject
async def login(
        data: UserAuthRequest,
        auth_handler: Annotated[
           AuthHandler, Dependency(skip_validation=True)] = Provide[AuthContainer.auth_handler],
    ) -> UserAuthResponse:
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
        auth_handler: Annotated[
            AuthHandler, Dependency(skip_validation=True)] = Provide[AuthContainer.auth_handler],
    ) -> None:
    """
    Logout user.

    :param auth_handler: Injected auth request handler.
    :return: Logout status.
    """
    return await auth_handler.logout()


@post("/regitstration", status_code=HTTP_201_CREATED)
@inject
async def registration(
        data: UserAuthRequest,
        auth_handler: Annotated[
            AuthHandler, Dependency(skip_validation=True)] = Provide[AuthContainer.auth_handler],
    ) -> UserAuthResponse:
    """
    Register new user.

    :param data: User's credetials.
    :param auth_handler: Injected auth request handler.
    :return: Registration status.
    """
    return await auth_handler.registration(data)
