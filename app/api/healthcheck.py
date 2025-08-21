from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from app.api.dependencies import HealthCheckServiceDep, SettingsDep, UptimeDep
from app.core.enums import Status
from app.schemas.health import HealthResponse

health_router = APIRouter(tags=["health"])


@health_router.get("/health", response_model=HealthResponse)
async def health_check(
    uptime: UptimeDep,
    settings: SettingsDep,
    health_check_service: HealthCheckServiceDep,
) -> JSONResponse:
    health = await health_check_service.check_health(settings, uptime)

    if health.status == Status.DOWN:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health.model_dump(),
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=health.model_dump(),
    )
