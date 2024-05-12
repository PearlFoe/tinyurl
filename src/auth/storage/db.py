"""Module for db repositories."""
from ..models.users import User
from ..models.validators import Email

class UserRepository:
    """Repository for user data storing and querying logic."""

    async def create_user(self, user: User) -> None:
        """
        Create new user in database.

        :param user: User data model.
        """
        ...

    async def get_user(self, login: Email) -> User | None:
        """
        Get user data from database.

        :param login: User's login string.
        :return: User data model or None if user doesn't excist.
        """
        ...
