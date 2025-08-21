from fastapi import APIRouter

router = APIRouter()


@router.get("/cameras")
async def get_cameras():
    return []


@router.get("/cameras/{camera_id}")
async def get_camera_status(camera_id: str):
    return {}


@router.post("/cameras/{camera_id}/ptz")
async def set_ptz_position(camera_id: str, pan: float, tilt: float, zoom: float):
    return {}
