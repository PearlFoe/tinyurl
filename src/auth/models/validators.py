"""Module for custom types validators."""
from typing import Any
from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from msgspec import ValidationError




class Email(str):
    """Email string validator."""

    __slots__ = "_value"

    def __init__(self, v: str) -> None:
        try:
            self._value: ValidatedEmail = validate_email(v)
        except EmailNotValidError as e:
            raise ValidationError from e

    def __str__(self) -> str:
        return self._value.normalized

    def __repr__(self) -> str:
        return self._value.__repr__()


def enc_hook(v: Any) -> Any:  # noqa
    """
    Encode custom types into supported by msgspec types.

    :param v: Unsupported type value.
    :raise NotImplementedError: Raises error if it's unexpected data type.
    :return: _description_.
    """
    if isinstance(v, Email):
        return str(v)
    else:
        raise NotImplementedError(v)
