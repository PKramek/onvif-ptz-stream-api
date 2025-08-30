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
async def move_left(onvif_service: OnvifServiceDep):
    onvif_service.move_left()
    return {"success": True, "message": "Camera moved left"}


@router.post("/right")
async def move_right(onvif_service: OnvifServiceDep):
    onvif_service.move_right()
    return {"success": True, "message": "Camera moved right"}


@router.post("/up")
async def move_up(onvif_service: OnvifServiceDep):
    onvif_service.move_up()
    return {"success": True, "message": "Camera moved up"}


@router.post("/down")
async def move_down(onvif_service: OnvifServiceDep):
    onvif_service.move_down()
    return {"success": True, "message": "Camera moved down"}


@router.post("/zoom_in")
async def zoom_in(onvif_service: OnvifServiceDep):
    onvif_service.zoom_in()
    return {"success": True, "message": "Camera zoomed in"}


@router.post("/zoom_out")
async def zoom_out(onvif_service: OnvifServiceDep):
    onvif_service.zoom_out()
    return {"success": True, "message": "Camera zoomed out"}


@router.post("/home")
async def goto_home(onvif_service: OnvifServiceDep):
    onvif_service.goto_home_position()
    return {"success": True, "message": "Camera moved to home position"}
