from functools import cached_property

from onvif import ONVIFCamera
from app.contracts.services.onvif_service import IOnvifService
from time import sleep

from app.core.types import PanVelocityType, TiltVelocityType, ZoomVelocityType


class OnvifService(IOnvifService):
    @cached_property
    def camera(self) -> ONVIFCamera:
        return ONVIFCamera(
            self.onvif_settings.onvif_camera_ip_address,
            self.onvif_settings.onvif_camera_port,
            self.onvif_settings.onvif_camera_user,
            self.onvif_settings.onvif_camera_password.get_secret_value(),
        )

    @cached_property
    def ptz(self):
        return self.camera.create_ptz_service()

    @cached_property
    def media(self):
        return self.camera.create_media_service()

    @cached_property
    def media_profile(self):
        return self.media.GetProfiles()[0]

    def get_snapshot_uri(self) -> str:
        uri = self.media.GetSnapshotUri({"ProfileToken": self.media_profile.token})
        self.logger.debug(f"Snapshot URI: {uri.Uri}")
        return uri.Uri

    def get_stream_uri(self) -> str:
        stream = self.media.GetStreamUri(
            {
                "StreamSetup": {
                    "Stream": "RTP-Unicast",
                    "Transport": {"Protocol": "RTSP"},
                },
                "ProfileToken": self.media_profile.token,
            }
        )
        self.logger.debug(f"Stream URI: {stream.Uri}")
        return stream.Uri

    def _continuous_move(
        self, pan: float = 0.0, tilt: float = 0.0, zoom: float = 0.0, timeout: float = 1
    ):
        request = self.ptz.create_type("ContinuousMove")
        request.ProfileToken = self.media_profile.token
        request.Velocity = {
            "PanTilt": {
                "x": pan,
                "y": tilt,
                "space": "http://www.onvif.org/ver10/tptz/PanTiltSpaces/VelocityGenericSpace",
            },
            "Zoom": {
                "x": zoom,
                "space": "http://www.onvif.org/ver10/tptz/ZoomSpaces/VelocityGenericSpace",
            },
        }
        self.logger.debug(
            f"ContinuousMove request: pan={pan}, tilt={tilt}, zoom={zoom}"
        )
        self.ptz.ContinuousMove(request)
        sleep(timeout)
        self.ptz.Stop({"ProfileToken": request.ProfileToken})
        self.logger.debug("Stopped continuous move")

    def move_pan(self, pan_velocity: PanVelocityType):
        self._continuous_move(pan=pan_velocity)

    def move_tilt(self, tilt_velocity: TiltVelocityType):
        self._continuous_move(tilt=tilt_velocity)

    def move_zoom(self, zoom_velocity: ZoomVelocityType):
        self._continuous_move(zoom=zoom_velocity)

    def move_left(self):
        self.move_pan(pan_velocity=-self.ptz_settings.pan_velocity)

    def move_right(self):
        self.move_pan(pan_velocity=self.ptz_settings.pan_velocity)

    def move_up(self):
        self.move_tilt(tilt_velocity=self.ptz_settings.tilt_velocity)

    def move_down(self):
        self.move_tilt(tilt_velocity=-self.ptz_settings.tilt_velocity)

    def zoom_in(self):
        self.move_zoom(zoom_velocity=self.ptz_settings.zoom_velocity)

    def zoom_out(self):
        self.move_zoom(zoom_velocity=-self.ptz_settings.zoom_velocity)

    def goto_home_position(self):
        self.logger.debug("Going to home position")
        request = self.ptz.create_type("GotoHomePosition")
        request.ProfileToken = self.media_profile.token
        self.ptz.GotoHomePosition(request)
