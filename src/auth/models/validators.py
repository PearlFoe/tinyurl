"""Module for custom types validators."""

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

    def __str__(self) -> str:  # n
        return self._value.normalized

    def __repr__(self) -> str:
        return self._value.__repr__()
