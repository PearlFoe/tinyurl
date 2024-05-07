from litestar import Router

#  Router "resolve" needs to be imported here to register it in root router separately
from .routers import shorten, resolve  # noqa
from .containers import URLContainer
from .settings import URLSettings


def get_container() -> URLContainer:
    """Dependency container factory."""
    container = URLContainer()
    settings = URLSettings()

    container.env.from_dict(settings.model_dump())

    return container


def get_router() -> Router:
    """Aggregate all routers in /url path."""
    router = Router(path="/url", route_handlers=[shorten,])
    return router
