"""Module for project settings models."""
from os import path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import networks


class Settings(BaseSettings):
    """Base model for parsing settings from .env file."""

    db_dsn: networks.PostgresDsn
    cache_dsn: networks.RedisDsn

    _project_dir: str = path.join(path.dirname(path.realpath(__file__)), "..")


    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=path.join(_project_dir, "secrets/.env"),
        extra="ignore",
    )
