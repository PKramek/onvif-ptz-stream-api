from fastapi import APIRouter
from pydantic import BaseModel
from app.api.dependencies import OnvifServiceDep
from app.core.types import PanVelocityType, TiltVelocityType, ZoomVelocityType

router = APIRouter()


class PTZCommand(BaseModel):
    pan_velocity: PanVelocityType
    tilt_velocity: TiltVelocityType
    zoom_velocity: ZoomVelocityType


@router.post("/cameras/ptz")
async def set_ptz_position(command: PTZCommand, onvif_service: OnvifServiceDep):
    # Execute PTZ movements
    try:
        if command.pan_velocity != 0:
            onvif_service.move_pan(command.pan_velocity)
        if command.tilt_velocity != 0:
            onvif_service.move_tilt(command.tilt_velocity)
        if command.zoom_velocity != 0:
            onvif_service.move_zoom(command.zoom_velocity)

        return {
            "success": True,
            "message": "PTZ movement executed successfully",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to execute PTZ movement: {str(e)}",
        }


@router.post("/left")
async def move_left(
    onvif_service: OnvifServiceDep, velocity: PanVelocityType | None = None
):
    onvif_service.move_left(velocity)
    return {"success": True, "message": "Camera moved left"}


@router.post("/right")
async def move_right(
    onvif_service: OnvifServiceDep, velocity: PanVelocityType | None = None
):
    onvif_service.move_right(velocity)
    return {"success": True, "message": "Camera moved right"}


@router.post("/up")
async def move_up(
    onvif_service: OnvifServiceDep, velocity: TiltVelocityType | None = None
):
    onvif_service.move_up(velocity)
    return {"success": True, "message": "Camera moved up"}


@router.post("/down")
async def move_down(
    onvif_service: OnvifServiceDep, velocity: TiltVelocityType | None = None
):
    onvif_service.move_down(velocity)
    return {"success": True, "message": "Camera moved down"}


@router.post("/zoom_in")
async def zoom_in(
    onvif_service: OnvifServiceDep, velocity: ZoomVelocityType | None = None
):
    onvif_service.zoom_in(velocity)
    return {"success": True, "message": "Camera zoomed in"}


@router.post("/zoom_out")
async def zoom_out(
    onvif_service: OnvifServiceDep, velocity: ZoomVelocityType | None = None
):
    onvif_service.zoom_out(velocity)
    return {"success": True, "message": "Camera zoomed out"}


@router.post("/preset")
async def set_preset(onvif_service: OnvifServiceDep, preset_name: str):
    onvif_service.set_preset(preset_name)
    return {"success": True, "message": "Camera preset set"}


@router.get("/presets")
async def list_presets(onvif_service: OnvifServiceDep):
    presets = onvif_service.list_presets()
    return {"success": True, "message": "Camera presets listed", "presets": presets}


@router.post("/preset/{preset_name}")
async def goto_preset(onvif_service: OnvifServiceDep, preset_name: str):
    onvif_service.goto_preset(preset_name)
    return {"success": True, "message": "Camera moved to preset"}


@router.delete("/preset/{preset_name}")
async def delete_preset(onvif_service: OnvifServiceDep, preset_name: str):
    onvif_service.delete_preset(preset_name)
    return {"success": True, "message": "Camera preset deleted"}
