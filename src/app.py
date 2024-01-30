"""
Main application file.

Stores all logic to setup application.
"""
from litestar import Litestar, Router

from url import resolve, get_router as url_get_router


def _get_api_router() -> Router:
    """Create router with all included api subrouters."""
    router = Router(
        path="/api/v1",
        route_handlers=[
            url_get_router(),
        ]
    )
    return router


def get_app() -> Litestar:
    """Create main app with all routers included."""
    app = Litestar()

    app.register(resolve)  # separate router for short url resolving
    app.register(_get_api_router())

    return app
