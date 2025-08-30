from typing import Annotated, Any, TypeAlias

import structlog
from pydantic import BeforeValidator, Field
from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class LoggerProtocol(Protocol):
    def info(self, event: str, **kw: Any) -> None: ...
    def error(self, event: str, **kw: Any) -> None: ...
    def warning(self, event: str, **kw: Any) -> None: ...
    def debug(self, event: str, **kw: Any) -> None: ...


def validate_logger(v: Any) -> Any:
    """Validate that the object is a structlog logger or has logger methods"""
    # If the object is a structlog logger, return it
    if isinstance(
        v,
        structlog.stdlib.BoundLogger | structlog.types.BindableLogger,
    ):
        return v

    # If the object implements the LoggerProtocol, return it
    if isinstance(v, LoggerProtocol):
        return v

    raise ValueError("Invalid logger object")


LoggerType: TypeAlias = Annotated[Any, BeforeValidator(validate_logger)]

# Complete semantic versioning with pre-release and build metadata
# https://semver.org/
SemanticVersionType = Annotated[
    str,
    Field(
        pattern=r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
        description="Full semantic version with optional pre-release and build metadata",
    ),
]

PanVelocityType: TypeAlias = Annotated[
    float,
    Field(ge=-1.0, le=1.0, description="Pan velocity in the range of -1.0 to 1.0"),
]
TiltVelocityType: TypeAlias = Annotated[
    float,
    Field(ge=-1.0, le=1.0, description="Tilt velocity in the range of -1.0 to 1.0"),
]
ZoomVelocityType: TypeAlias = Annotated[
    float,
    Field(ge=-1.0, le=1.0, description="Zoom velocity in the range of -1.0 to 1.0"),
]
