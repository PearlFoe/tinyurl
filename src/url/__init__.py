from litestar import Router

#  Router "resolve" needs to be imported here to register it in root router separately
from .routers import shorten, resolve  # noqa
from .containers import Container

def get_container() -> Container:
    """Dependency container factory."""
    return Container()


def get_router() -> Router:
    """Aggregate all routers in /url path."""
    router = Router(path="/url", route_handlers=[shorten,])
    return router
