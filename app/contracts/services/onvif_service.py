from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict

from app.core.config import OnvifSettings, PTZSettings
from app.core.types import (
    LoggerType,
    PanVelocityType,
    TiltVelocityType,
    ZoomVelocityType,
)


class IOnvifService(ABC, BaseModel):
    """
    Interface for ONVIF service

    This service is responsible for interacting with the ONVIF camera.
    """

    onvif_settings: OnvifSettings
    ptz_settings: PTZSettings
    logger: LoggerType

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    def get_snapshot_uri(self) -> str:
        pass

    @abstractmethod
    def get_stream_uri(self) -> str:
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
    def move_left(self, velocity: PanVelocityType | None = None):
        pass

    @abstractmethod
    def move_right(self, velocity: PanVelocityType | None = None):
        pass

    @abstractmethod
    def move_up(self, velocity: TiltVelocityType | None = None):
        pass

    @abstractmethod
    def move_down(self, velocity: TiltVelocityType | None = None):
        pass

    @abstractmethod
    def zoom_in(self, velocity: ZoomVelocityType | None = None):
        pass

    @abstractmethod
    def zoom_out(self, velocity: ZoomVelocityType | None = None):
        pass

    @abstractmethod
    def set_preset(self, preset_name: str) -> None:
        pass

    @abstractmethod
    def delete_preset(self, preset_name: str) -> None:
        pass

    @abstractmethod
    def list_presets(self) -> list[str]:
        pass

    @abstractmethod
    def goto_preset(self, preset_name: str) -> None:
        pass
