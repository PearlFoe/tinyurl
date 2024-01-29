from litestar import Litestar

from url import resolve, get_router as url_get_router


async def get_app() -> Litestar:
    app = Litestar()
    
    app.register(resolve)  # separate router for short url resolving
    app.register(url_get_router())
    
    return app
