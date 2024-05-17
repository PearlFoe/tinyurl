from src.auth.models.validators import Email
from src.auth.models.routers import UserLoginRequest
from src.auth.models.users import User


class UserRepositoryMock:
    def __init__(self) -> None:
        self.db = {}

    async def create_user(self, user: User) -> None: 
        self.db[user.login] = user

    async def get_user(self, login: Email) -> User | None:
        return self.db.get(login, None)


class UserCacheRepository:
    ...
