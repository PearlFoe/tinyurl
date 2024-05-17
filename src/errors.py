"""Module for base project errors."""


class BaseError(Exception):
    """
    Base error class.

    All other prject errors are inherited from it.
    """

    def __init__(self, message: str = "") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"
