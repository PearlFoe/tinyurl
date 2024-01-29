from litestar import Router

from .routers import shorten, resolve


def get_router() -> Router:
    router = Router(path="/url")
    router.register(shorten)
    return router
