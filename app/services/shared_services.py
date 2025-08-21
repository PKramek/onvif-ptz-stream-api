from pydantic import BaseModel, ConfigDict

from app.contracts.services.health_check import IHealthCheckService


class SharedServices(BaseModel):
    """
    Container for shared application services

    This class should be used to share immutable services between API calls.

    If you need to share mutable services, you should use the request object.
    """

    health_check_service: IHealthCheckService

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    async def initialize(self) -> None:
        """Initialize the services"""
        pass

    async def cleanup(self) -> None:
        """Cleanup the services"""
        pass
