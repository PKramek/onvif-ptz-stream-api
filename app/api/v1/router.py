from fastapi import APIRouter

from .endpoints import ptz, stream

# We use a pattern, where we have a separate router for each domain, and then we include
# the routers in the main router. Then we only need to include the main router in the app.

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(ptz.router, prefix="/ptz", tags=["ptz"])
v1_router.include_router(stream.router, prefix="/stream", tags=["stream"])
