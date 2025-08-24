import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import cv2

from app.api.dependencies import LoggerDep, OnvifServiceDep

router = APIRouter()


@router.get("/stream/{camera_id}", response_class=StreamingResponse)
async def get_stream(
    camera_id: str, onvif_service: OnvifServiceDep, logger: LoggerDep
) -> StreamingResponse:
    try:
        stream_uri = onvif_service.get_stream_uri()
        logger.info(f"Stream URI: {stream_uri}")
    except Exception as e:
        logger.error(f"Failed to get stream URI: {e}")
        raise HTTPException(status_code=404, detail="Camera stream not found")

    def generate_frames():
        cap = cv2.VideoCapture(stream_uri)
        if not cap.isOpened():
            logger.error(f"Cannot open video stream for {camera_id}")
            return  # Stop generator immediately

        try:
            while True:
                success, frame = cap.read()
                if not success:
                    logging.warning(
                        f"Frame read failed for {camera_id}, stopping stream"
                    )
                    break
                ret, jpeg = cv2.imencode(".jpg", frame)
                if not ret:
                    continue
                frame_bytes = jpeg.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )
        finally:
            cap.release()

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


# @router.get("/stream/{camera_id}/frame")
# async def get_stream_frame(camera_id: str):
#     return StreamingResponse(
#         content=b"", media_type="multipart/x-mixed-replace; boundary=frame"
#     )
