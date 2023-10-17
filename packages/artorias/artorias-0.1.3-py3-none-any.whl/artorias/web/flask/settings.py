from __future__ import annotations

from datetime import timedelta
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    UNKNOWN_EXCEPTION_MESSAGE: str = "Server error"
    LOGGER_FORMAT_STRING: str = "[%(asctime)s] [%(levelname)-7s] %(thread)s in [%(module)-30s]: %(message)s"

    # DB
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_DATABASE_URI: str = "sqlite://"

    # CACHE
    CACHE_TYPE: str = "SimpleCache"

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES: int | timedelta = timedelta(hours=1)
    JWT_TOKEN_LOCATION: List[str] = ["headers", "cookies"]
    JWT_REFRESH_COOKIE_TOKEN_AFTER_REQUEST: bool = False
    JWT_REFRESH_COOKIE_TOKEN_BEFORE_EXPIRES: int = timedelta(minutes=10).seconds
