from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict

from app.core.config import OnvifSettings
from app.core.types import LoggerType


class IOnvifService(ABC, BaseModel):
    """
    Interface for ONVIF service

    This service is responsible for interacting with the ONVIF camera.
    """

    settings: OnvifSettings
    logger: LoggerType

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    def get_profile_tokens(self) -> list[str]:
        pass

    @abstractmethod
    def get_snapshot_uri(self) -> str:
        pass

    @abstractmethod
    def get_stream_uri(self) -> str:
        pass
