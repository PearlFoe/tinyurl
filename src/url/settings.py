"""Module for project settings models."""
from os import path
from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import networks


class Settings(BaseSettings):
    """Model for .env settings parsing."""

    class _EnvType(StrEnum):
        TEST = "test"
        PROD = "prod"

    env: _EnvType = "test"

    db_dsn: networks.PostgresDsn
    cache_dsn: networks.RedisDsn

    _project_dir: str = path.join(path.dirname(path.realpath(__file__)), "../..")

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_file=path.join(_project_dir, f"secrets/.env.{env}"),
        extra="ignore",
    )
