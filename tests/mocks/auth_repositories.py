from src.auth.models.validators import Email
from src.auth.models.users import User
from src.auth.models.token import Token


class UserRepositoryMock:
    def __init__(self) -> None:
        self.db = {}

    async def create_user(self, user: User) -> None:
        self.db[user.login] = user

    async def get_user(self, login: Email) -> User | None:
        return self.db.get(login, None)


class UserCacheRepository:
    def __init__(self) -> None:
        self.db = {}

    def _get_key(self, token: Token) -> str:
        nt = token.body
        return f"invalidated_{nt}"

    async def save_invalidated_token(self, token: Token) -> None:
        self.db[self._get_key(token)] = token

    async def check_invalidated(self, token: Token) -> bool:
        return self._get_key(token) in self.db
