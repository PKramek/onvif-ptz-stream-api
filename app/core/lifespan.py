import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
import structlog

from app.core.config import Settings
from app.services.onvif_service import OnvifService
from app.services.shared_services import SharedServices
from app.services.health_check import HealthCheckService


def lifespan_factory(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.startup_time = time.time()
        app.state.logger = structlog.get_logger()

        services = SharedServices(
            health_check_service=HealthCheckService(logger=app.state.logger),
            onvif_service=OnvifService(
                settings=settings.onvif, logger=app.state.logger
            ),
        )
        app.state.shared_services = services

        # Log the settings, so that its easy to debug
        app.state.logger.info(f"{repr(settings)}")

        await services.initialize()

        try:
            yield  # Run the application
        finally:
            await services.cleanup()

    return lifespan
