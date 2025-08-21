import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class StructlogRequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract request_id from header or generate a new one
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
        )
        try:
            response = await call_next(request)
        finally:
            structlog.contextvars.clear_contextvars()
        return response
