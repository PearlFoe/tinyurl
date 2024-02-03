"""Dependency containers for url package."""

from dependency_injector import containers, providers

from .url_handlers import URLHandler

class Container(containers.DeclarativeContainer):
    """Handle all dependencies for url processing."""

    url_handler = providers.Factory(URLHandler)
