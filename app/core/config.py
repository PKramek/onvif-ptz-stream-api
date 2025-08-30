from functools import lru_cache
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import Environment
from app.core.types import SemanticVersionType

DEFAULT_APP_NAME = "onvif-ptz-stream-api"


class OnvifSettings(BaseSettings):
    onvif_camera_ip_address: str = Field(
        ...,
        description="The IP address of the ONVIF camera",
        alias="ONVIF_CAMERA_IP_ADDRESS",
    )

    onvif_camera_port: int = Field(
        default=80,
        description="The port of the ONVIF camera",
        alias="ONVIF_CAMERA_PORT",
    )
    onvif_camera_user: str = Field(
        ..., description="The username for the ONVIF camera", alias="ONVIF_CAMERA_USER"
    )
    onvif_camera_password: SecretStr = Field(
        ...,
        description="The password for the ONVIF camera",
        alias="ONVIF_CAMERA_PASSWORD",
    )

    model_config = SettingsConfigDict(
        frozen=True, arbitrary_types_allowed=True, env_prefix="ONVIF_CAMERA_"
    )


PTZVelocity = Annotated[
    float,
    Field(
        default=0.5,
        ge=0.0,
        le=1.0,
    ),
]


class PTZSettings(BaseSettings):
    pan_velocity: PTZVelocity = Field(
        description="The velocity of the PTZ pan",
        alias="PTZ_PAN_VELOCITY",
    )
    tilt_velocity: PTZVelocity = Field(
        description="The velocity of the PTZ tilt",
    )
    zoom_velocity: PTZVelocity = Field(
        description="The velocity of the PTZ zoom",
        alias="PTZ_ZOOM_VELOCITY",
    )

    model_config = SettingsConfigDict(
        frozen=True, arbitrary_types_allowed=True, env_prefix="PTZ_"
    )


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
    onvif: OnvifSettings = Field(default_factory=lambda: OnvifSettings())  # type: ignore[call-arg]
    ptz: PTZSettings = Field(default_factory=lambda: PTZSettings())  # type: ignore[call-arg]

    model_config = SettingsConfigDict(frozen=True)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance

    We need to ignore the call-arg because the Settings are supposed to be loaded from the
    environment and not from the constructor.
    """
    return Settings()  # type: ignore[call-arg]
