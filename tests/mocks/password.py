import hashlib


class MockedHash:
    @staticmethod
    def generate(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(password: str, hash: str) -> bool:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == hash
