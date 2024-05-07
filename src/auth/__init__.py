from litestar import Router

from .routers import login, logout, registration
from .containers import AuthContainer
from .settings import AuthSettings


def get_container() -> AuthContainer:
    """Dependency container factory."""
    container = AuthContainer()
    settings = AuthSettings()

    container.env.from_dict(settings.model_dump())

    return container


def get_router() -> Router:
    """Aggregate all routers in /auth path."""
    router = Router(path="/auth", route_handlers=[login, logout, registration])
    return router
