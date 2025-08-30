from onvif import ONVIFCamera
from time import sleep
from app.core.config import OnvifSettings

onvif_settings = OnvifSettings()

camera = ONVIFCamera(
    onvif_settings.ONVIF_CAMERA_IP_ADDRESS,
    onvif_settings.ONVIF_CAMERA_PORT,
    onvif_settings.ONVIF_CAMERA_USER,
    onvif_settings.ONVIF_CAMERA_PASSWORD.get_secret_value(),
)
ptz = camera.create_ptz_service()
media = camera.create_media_service()
media_profile = media.GetProfiles()[0]


def perform_move(ptz, request, timeout):
    ptz.ContinuousMove(request)
    sleep(timeout)
    ptz.Stop({"ProfileToken": request.ProfileToken})


request = ptz.create_type("ContinuousMove")
request.ProfileToken = media_profile.token

# Directly assign Velocity as a dict matching the expected structure
request.Velocity = {
    "PanTilt": {
        "x": 0.5,
        "y": 0.0,
        "space": "http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace",  # Correct velocity space
    },
    "Zoom": {
        "x": 0.0,
        "space": "http://www.onvif.org/ver10/tptz/ZoomSpaces/VelocityGenericSpace",  # Correct velocity space
    },
}

perform_move(ptz, request, timeout=2)
