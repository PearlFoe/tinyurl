"""Module for url processing settings models."""
from src.settings import Settings


class URLSettings(Settings):
    """Model for parsing url shortening settings from .env file."""

    model_config = Settings.model_config
