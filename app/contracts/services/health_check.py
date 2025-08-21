from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, NonNegativeFloat

from app.core.config import Settings
from app.core.types import LoggerType
from app.schemas.health import ComponentHealth, HealthResponse


@runtime_checkable
class ServiceWithHealthCheck(Protocol):
    async def check_health(self) -> ComponentHealth:
        pass


class IHealthCheckService(ABC, BaseModel):
    """
    Interface for health check service

    This service is responsible for checking the health of the application.
    """

    logger: LoggerType
    # Use ServiceWithHealthCheck protocol to ensure that the service has a check_health method
    # cache_service: ServiceWithHealthCheck

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    async def check_health(
        self, settings: Settings, uptime: NonNegativeFloat
    ) -> HealthResponse:
        pass
