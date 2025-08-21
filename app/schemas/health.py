from typing import Any

from pydantic import BaseModel, NonNegativeFloat

from app.core.enums import Environment, Status
from app.core.types import SemanticVersionType


class ComponentHealth(BaseModel):
    status: Status
    details: dict[str, Any] | None = None
    responseTime: NonNegativeFloat | None = None


class HealthResponse(BaseModel):
    status: Status
    uptime: float
    checks: dict[str, ComponentHealth]
    version: SemanticVersionType
    environment: Environment
