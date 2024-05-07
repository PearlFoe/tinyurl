"""Dependency containers for auth package."""

from dependency_injector import containers, providers

from .services.auth_handler import AuthHandler


class AuthContainer(containers.DeclarativeContainer):
    """Handle all dependencies for user auth."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.auth.routers",
        ]
    )

    env = providers.Configuration()

    auth_handler = providers.Factory(
        AuthHandler,
    )
