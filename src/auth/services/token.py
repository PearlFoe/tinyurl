"""Module wiht oken generators."""

from jose import JWTError, jwt

from pydantic import BaseModel

from ..models.token import Token
from ..errors import InvalidTokenError


class JWT:
    """JWT token genreator."""

    def __init__(self, secret: str, algorithm: str = "HS256"):
        self._secret = secret
        self._algorithm = algorithm

    def validate(self, token: str, model: BaseModel) -> Token:
        """
        Validate JWT token and stored payload.

        :param token: JWT token.
        :param model: Model to validate payload.
        :raise InvalidTokenError: Raised if token decoding fails.
        :return: Validated token payload model.
        """
        try:
            data = jwt.decode(
                token=token,
                key=self._secret,
                algorithms=[self._algorithm,],
            )
        except JWTError as e:
            raise InvalidTokenError from e
        else:
            return model.model_validate(data)

    def generate(self, payload: dict[str, str]) -> str:
        """
        Generate JWT token with payload.

        :param payload: Any json serializable dict.
        :return: Genrated token.
        """
        return jwt.encode(
            claims=payload,
            key=self._secret,
            algorithm=self._algorithm,
        )
