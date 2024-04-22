"""Dependency containers for url package."""

from dependency_injector import containers, providers

from .services.url_handlers import URLHandler
from .services.storage import URLStorage
from .storage.db import URLRepository
from .storage.cache import URLCacheRepository
from .storage import utils

class URLContainer(containers.DeclarativeContainer):
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

    url_storage = providers.Factory(
        URLStorage,
        db=db_repository,
        cache=cache_repository,
    )

    url_handler = providers.Factory(
        URLHandler,
        storage=url_storage,
    )
