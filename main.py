import logging

import uvicorn

from app.core.app_factory import create_app
from app.core.config import get_settings
from app.core.logging_config import configure_logging

settings = get_settings()
configure_logging(settings.debug)
app = create_app(settings)

for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = True

if __name__ == "__main__":
    uvicorn.run(
        "main:app" if settings.debug else app,
        host="0.0.0.0",  # nosec B104
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        log_config=None,  # Prevent Uvicorn from overriding our logging config
    )
