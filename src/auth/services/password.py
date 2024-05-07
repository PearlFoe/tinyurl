"""Module for password hashing logic."""

from passlib.hash import sha512_crypt


class Hash:
    """User passwords hasher."""

    @staticmethod
    def generate(password: str) -> str:
        """
        Generate hash based on user password string.

        :param password: User's password.
        :return: Generated hash.
        """
        return sha512_crypt.hash(password)

    @staticmethod
    def verify(password: str, hash: str) -> bool:
        """
        Chech if inputed password matches with stored hash.

        :param password: Inputed password .
        :param hash: Stored password hash.
        :return: True if password matches the hash, othewise False.
        """
        return sha512_crypt.verify(password, hash)
