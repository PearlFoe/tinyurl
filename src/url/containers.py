"""Dependency containers for url package."""

from dependency_injector import containers, providers

from .url_handlers import URLHandler
from .storage.db import URLRepository
from .storage.cache import URLCacheRepository
from .storage import utils

class Container(containers.DeclarativeContainer):
    """Handle all dependencies for url processing."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.url.routers",
        ]
    )

    env = providers.Configuration()

    db_pool = providers.Resource(
        utils.init_db_connection_pool,
        dsn=env.db_dsn,
    )

    db_repository = providers.Factory(URLRepository)

    cache_pool = providers.Resource(
        utils.init_cache_connection_pool,
        dsn=env.cache_dsn,
    )

    cache_repository = providers.Factory(URLCacheRepository)

    url_handler = providers.Factory(
        URLHandler,
        db=db_repository,
        cache=cache_repository,
    )
