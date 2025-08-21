import time
from typing import Annotated

import structlog
from fastapi import Depends, Request

from app.contracts.services.health_check import IHealthCheckService
from app.core.config import Settings
from app.core.types import LoggerType
from app.services.shared_services import SharedServices


def get_settings_dependency(request: Request) -> Settings:
    return request.app.state.settings


def get_logger(request: Request) -> structlog.stdlib.BoundLogger:
    return request.app.state.logger


def get_shared_services(request: Request) -> SharedServices:
    return request.app.state.shared_services


def get_uptime(request: Request) -> float:
    return time.time() - request.app.state.startup_time


def get_health_check_service(request: Request) -> IHealthCheckService:
    return request.app.state.shared_services.health_check_service


# ───────────────────────────────SETTINGS───────────────────────────────
SettingsDep = Annotated[Settings, Depends(get_settings_dependency)]
# ───────────────────────────────SERVICES───────────────────────────────
SharedServicesDep = Annotated[SharedServices, Depends(get_shared_services)]
HealthCheckServiceDep = Annotated[
    IHealthCheckService, Depends(get_health_check_service)
]
# ───────────────────────────────OTHER───────────────────────────────
UptimeDep = Annotated[float, Depends(get_uptime)]
LoggerDep = Annotated[LoggerType, Depends(get_logger)]
