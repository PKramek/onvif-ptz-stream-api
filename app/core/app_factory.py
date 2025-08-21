from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.healthcheck import health_router
from app.api.v1.router import v1_router
from app.core.config import Settings, get_settings
from app.core.lifespan import lifespan_factory
from app.core.logging_config import configure_logging
from app.core.middleware import StructlogRequestContextMiddleware


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Application factory function for creating FastAPI instances

    If settings are not provided, the function will use the settings from the environment.
    """
    if settings is None:
        settings = get_settings()

    # Configure logging before app creation
    configure_logging(debug=settings.debug)

    # Create FastAPI app with lifespan
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
        lifespan=lifespan_factory(settings),
    )

    # Add structlog request context middleware
    app.add_middleware(StructlogRequestContextMiddleware)

    # Include API routes
    app.include_router(v1_router)
    app.include_router(health_router)

    # Add security middleware
    if settings.allowed_hosts:
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
