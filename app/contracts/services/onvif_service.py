from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict

from app.core.config import OnvifSettings
from app.core.types import (
    LoggerType,
    PanVelocityType,
    TiltVelocityType,
    ZoomVelocityType,
)
from onvif import OnvifClient
from pydantic import computed_field
from functools import cached_property


class IOnvifService(ABC, BaseModel):
    """
    Interface for ONVIF service

    This service is responsible for interacting with the ONVIF camera.
    """

    settings: OnvifSettings
    logger: LoggerType

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @computed_field  # type: ignore[misc]
    @cached_property
    def onvif_client(self) -> OnvifClient:
        onvif_client = OnvifClient(
            self.settings.ONVIF_CAMERA_IP_ADDRESS,
            self.settings.ONVIF_CAMERA_PORT,
            self.settings.ONVIF_CAMERA_USER,
            self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value(),
        )
        return onvif_client

    @abstractmethod
    def get_profile_tokens(self) -> list[str]:
        pass

    @abstractmethod
    def get_snapshot_uri(self) -> str:
        pass

    @abstractmethod
    def get_stream_uri(self) -> str:
        pass

    @abstractmethod
    def get_ptz_capabilities(self) -> dict:
        pass

    @abstractmethod
    def move_pan(self, pan_velocity: PanVelocityType):
        pass

    @abstractmethod
    def move_tilt(self, tilt_velocity: TiltVelocityType):
        pass

    @abstractmethod
    def move_zoom(self, zoom_velocity: ZoomVelocityType):
        pass

    @abstractmethod
    def stop_ptz(self):
        pass

    @abstractmethod
    def goto_home_position(self):
        pass
