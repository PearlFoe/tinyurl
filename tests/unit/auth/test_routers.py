from litestar.testing import TestClient


class TestAuthRouters:
    def test_login(
            self,
            client: TestClient,
        ):
        ...