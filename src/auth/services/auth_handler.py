"""Auth requests data handler."""

from ..models.routers import UserAuthRequest, UserAuthResponse


class AuthHandler:
    """Auth requests data handler."""

    def __init__(self) -> None:
        pass

    async def login(self, _: UserAuthRequest) -> UserAuthResponse:
        """
        Login user.

        :param data: User login data.
        :return: Response body with login result.
        """
        return {}

    async def registration(self, _: UserAuthRequest) -> UserAuthResponse:
        """
        Register user.

        :param data: User registration data.
        :return: Response body with registration result.
        """
        return {}


    async def logout(self) -> None:
        """Logout user."""
        return None

