"""
Main application file.

Stores all logic to setup application.
"""

from dependency_injector.containers import DeclarativeContainer
from litestar import Litestar, Router

from src.url import resolve, get_container as url_get_container, get_router as url_get_router



class ExtendedLitestar(Litestar):
    """Extended application class for working with DI containers."""

    __slots__ = ("containers", )

    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, *kwargs)
        self.containers: tuple | None = None


def _get_api_router() -> Router:
    """Create router with all included api subrouters."""
    router = Router(
        path="/api/v1",
        route_handlers=[
            url_get_router(),
        ]
    )
    return router


def get_app(containers: tuple[DeclarativeContainer] = ()) -> Litestar:
    """Create main app with all routers included."""
    containers = containers or (
        url_get_container(),
    )
    app = ExtendedLitestar()
    app.containers = containers

    app.register(resolve)  # separate router for short url resolving
    app.register(_get_api_router())

    return app
