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

    def move_left(self, velocity: PanVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.pan_velocity
        self.move_pan(pan_velocity=-velocity)

    def move_right(self, velocity: PanVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.pan_velocity
        self.move_pan(pan_velocity=velocity)

    def move_up(self, velocity: TiltVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.tilt_velocity
        self.move_tilt(tilt_velocity=velocity)

    def move_down(self, velocity: TiltVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.tilt_velocity
        self.move_tilt(tilt_velocity=-velocity)

    def zoom_in(self, velocity: ZoomVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.zoom_velocity
        self.move_zoom(zoom_velocity=velocity)

    def zoom_out(self, velocity: ZoomVelocityType | None = None):
        if velocity is None:
            velocity = self.ptz_settings.zoom_velocity
        self.move_zoom(zoom_velocity=-velocity)

    def list_presets(self) -> list[str]:
        presets = self.ptz.GetPresets({"ProfileToken": self.media_profile.token})
        return [preset.Name for preset in presets]

    def delete_preset(self, preset_name: str):
        preset_token = self.get_preset_token(preset_name)
        request = self.ptz.create_type("RemovePreset")
        request.ProfileToken = self.media_profile.token
        request.PresetToken = preset_token
        self.ptz.RemovePreset(request)
        self.logger.debug(f"Preset {preset_name} deleted")

    def get_preset_details(self) -> list[dict]:
        """Get detailed information about all presets including name and token."""
        presets = self.ptz.GetPresets({"ProfileToken": self.media_profile.token})
        return [{"name": preset.Name, "token": preset.token} for preset in presets]

    def get_preset_token(self, preset_name: str) -> str:
        """Get the token for a preset by name."""
        presets = self.ptz.GetPresets({"ProfileToken": self.media_profile.token})
        for preset in presets:
            if preset.Name == preset_name:
                return preset.token
        raise ValueError(f"Preset {preset_name} not found")

    def goto_preset(self, preset_name: str):
        preset_token = self.get_preset_token(preset_name)
        request = self.ptz.create_type("GotoPreset")
        request.ProfileToken = self.media_profile.token
        request.PresetToken = preset_token
        self.ptz.GotoPreset(request)

    def set_preset(self, preset_name: str):
        # Check if preset already exists
        if preset_name in self.list_presets():
            raise ValueError(
                f"Preset {preset_name} already exists. Please delete it first."
            )

        # SetPreset requires a PresetToken, which should be None for creating new presets
        self.ptz.SetPreset(
            {
                "ProfileToken": self.media_profile.token,
                "PresetName": preset_name,
                "PresetToken": None,
            }
        )
        self.logger.debug(f"Preset {preset_name} set")
