from fastapi import APIRouter
from pydantic import BaseModel
from app.api.dependencies import OnvifServiceDep
from app.core.types import PanVelocityType, TiltVelocityType, ZoomVelocityType

router = APIRouter()


@router.get("/cameras")
async def get_cameras():
    return []


@router.get("/cameras/{camera_id}")
async def get_camera_status(camera_id: str):
    return {}


@router.get("/cameras/{camera_id}/ptz/capabilities")
async def get_ptz_capabilities(camera_id: str, onvif_service: OnvifServiceDep):
    """
    Get PTZ capabilities of the camera.
    This endpoint helps diagnose PTZ support issues.
    """
    return onvif_service.get_ptz_capabilities()


class PTZCommand(BaseModel):
    pan_velocity: PanVelocityType
    tilt_velocity: TiltVelocityType
    zoom_velocity: ZoomVelocityType


@router.post("/cameras/{camera_id}/ptz")
async def set_ptz_position(
    camera_id: str, command: PTZCommand, onvif_service: OnvifServiceDep
):
    # Check PTZ capabilities first
    capabilities = onvif_service.get_ptz_capabilities()
    if not capabilities.get("ptz_supported"):
        return {
            "success": False,
            "error": "Camera does not support PTZ operations",
            "capabilities": capabilities,
        }

    # Execute PTZ movements
    try:
        if command.pan_velocity != 0:
            onvif_service.move_pan(command.pan_velocity)
        if command.tilt_velocity != 0:
            onvif_service.move_tilt(command.tilt_velocity)
        if command.zoom_velocity != 0:
            onvif_service.move_zoom(command.zoom_velocity)

        # Stop PTZ movement after a short delay
        onvif_service.stop_ptz()

        return {
            "success": True,
            "message": "PTZ movement executed successfully",
            "capabilities": capabilities,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to execute PTZ movement: {str(e)}",
            "capabilities": capabilities,
        }


@router.get("/cameras/{camera_id}/ptz/position")
async def get_ptz_position(camera_id: str, onvif_service: OnvifServiceDep):
    return {}


@router.post("/cameras/{camera_id}/ptz/home")
async def set_ptz_home(camera_id: str, onvif_service: OnvifServiceDep):
    try:
        onvif_service.goto_home_position()
        return {"success": True, "message": "Camera moved to home position"}
    except Exception as e:
        return {"success": False, "error": f"Failed to move to home position: {str(e)}"}
