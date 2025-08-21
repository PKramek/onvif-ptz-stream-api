from functools import lru_cache
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment
from app.core.types import SemanticVersionType

DEFAULT_APP_NAME = "onvif-ptz-stream-api"


class Settings(BaseSettings):
    # Application settings
    app_name: Annotated[str, Field(default=DEFAULT_APP_NAME, alias="APP_NAME")]
    version: Annotated[SemanticVersionType, Field(default="1.0.0", alias="VERSION")]
    debug: Annotated[bool, Field(default=False, alias="DEBUG")]
    environment: Annotated[
        Environment, Field(default=Environment.DEVELOPMENT, alias="ENVIRONMENT")
    ]

    # Security settings
    access_token_expire_minutes: Annotated[
        int, Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    ]
    allowed_hosts: Annotated[
        list[str] | None, Field(default=None, alias="ALLOWED_HOSTS")
    ]
    cors_origins: Annotated[list[str], Field(default=["*"], alias="CORS_ORIGINS")]

    # Logging
    log_level: Annotated[
        str,
        Field(
            default="INFO",
            alias="LOG_LEVEL",
            pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        ),
    ]

    # External services - The settings for external services should be grouped together in a separate class

    model_config = SettingsConfigDict(frozen=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance

    We need to ignore the call-arg because the Settings are supposed to be loaded from the
    environment and not from the constructor.
    """
    return Settings()  # type: ignore[call-arg]
