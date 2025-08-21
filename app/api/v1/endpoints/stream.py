from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/stream/{camera_id}")
async def get_stream(camera_id: str):
    return StreamingResponse(
        content=b"", media_type="multipart/x-mixed-replace; boundary=frame"
    )


@router.get("/stream/{camera_id}/frame")
async def get_stream_frame(camera_id: str):
    return StreamingResponse(
        content=b"", media_type="multipart/x-mixed-replace; boundary=frame"
    )
