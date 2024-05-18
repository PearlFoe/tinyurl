"""Dependency containers for auth package."""

from dependency_injector import containers, providers

from .services.password import Hash
from .services.token import JWT
from .services.auth_handler import AuthHandler
from .storage.db import UserRepository
from .storage.cache import UserCacheRepository


class AuthContainer(containers.DeclarativeContainer):
    """Handle all dependencies for user auth."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.auth.routers",
        ]
    )

    env = providers.Configuration()

    user_repository = providers.Factory(
        UserRepository,
    )

    user_cache_repository = providers.Factory(
        UserCacheRepository,
    )

    hash = providers.Factory(
        Hash,
    )

    jwt = providers.Factory(
        JWT,
        secret=env.secret,
    )

    auth_handler = providers.Factory(
        AuthHandler,
        hash=hash,
        jwt=jwt,
        db=user_repository,
        cache=user_cache_repository,
        token_ttl_sec=env.token_ttl_sec,
        token_header_name=env.token_header_name,
    )
