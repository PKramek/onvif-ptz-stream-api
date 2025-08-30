from app.contracts.services.onvif_service import IOnvifService
from urllib.parse import urlparse, urlunparse

from app.core.types import PanVelocityType, TiltVelocityType, ZoomVelocityType


class OnvifService(IOnvifService):
    """
    Service for interacting with the ONVIF camera.
    """

    def get_profile_tokens(self) -> list[str]:
        return self.onvif_client.get_profile_tokens()

    def get_main_profile_token(self) -> str:
        profile_tokens = self.get_profile_tokens()
        return profile_tokens[0]

    def get_snapshot_uri(self) -> str:
        return self.onvif_client.get_snapshot_uri(self.get_main_profile_token())

    def get_stream_uri(self) -> str:
        uri = self.onvif_client.get_streaming_uri(self.get_main_profile_token())
        parsed = urlparse(uri)

        # Add username and password to the netloc part: username:password@host:port
        netloc_with_auth = f"{self.settings.ONVIF_CAMERA_USER}:{self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value()}@{parsed.hostname}"
        if parsed.port:
            netloc_with_auth += f":{parsed.port}"

        # Build new URL with credentials included
        authorized_uri = urlunparse(
            (
                parsed.scheme,
                netloc_with_auth,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment,
            )
        )
        return authorized_uri

    def _is_ptz_supported(self) -> bool:
        """
        Check if the camera supports PTZ operations by validating the PTZ service.
        """
        try:
            # Check if PTZ service exists and is properly initialized
            if not hasattr(self.onvif_client, "ptz") or self.onvif_client.ptz is None:
                return False

            # Try to get PTZ configurations to verify service is working
            self.onvif_client.ptz.GetConfigurations()
            return True
        except (AttributeError, Exception):
            return False

    def get_ptz_capabilities(self) -> dict:
        """
        Get PTZ capabilities of the camera.
        Returns a dictionary with PTZ support information.
        """
        capabilities: dict = {
            "ptz_supported": False,
            "pan_supported": False,
            "tilt_supported": False,
            "zoom_supported": False,
            "home_position_supported": False,
            "error": None,
        }

        try:
            if not self._is_ptz_supported():
                capabilities["error"] = "PTZ service not available"
                return capabilities

            capabilities["ptz_supported"] = True

            # Try to get PTZ configurations to determine specific capabilities
            try:
                configs = self.onvif_client.ptz.GetConfigurations()
                if configs:
                    # Basic PTZ support confirmed
                    capabilities["pan_supported"] = True
                    capabilities["tilt_supported"] = True
                    capabilities["zoom_supported"] = True
                    capabilities["home_position_supported"] = True
            except Exception as e:
                capabilities["error"] = f"Failed to get PTZ configurations: {str(e)}"

        except Exception as e:
            capabilities["error"] = f"Error checking PTZ capabilities: {str(e)}"

        return capabilities

    def move_pan(self, pan_velocity: PanVelocityType):
        if not self._is_ptz_supported():
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return

        try:
            self.onvif_client.move_pan(
                profile_token=self.get_main_profile_token(), velocity=pan_velocity
            )
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                self.logger.warning(
                    "Camera does not support PTZ operations or PTZ configuration is missing"
                )
                return
            raise

    def move_tilt(self, tilt_velocity: TiltVelocityType):
        if not self._is_ptz_supported():
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return

        try:
            self.onvif_client.move_tilt(
                profile_token=self.get_main_profile_token(), velocity=tilt_velocity
            )
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                self.logger.warning(
                    "Camera does not support PTZ operations or PTZ configuration is missing"
                )
                return
            raise

    def move_zoom(self, zoom_velocity: ZoomVelocityType):
        if not self._is_ptz_supported():
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return

        try:
            self.onvif_client.move_zoom(
                profile_token=self.get_main_profile_token(),
                velocity=zoom_velocity,
            )
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                self.logger.warning(
                    "Camera does not support PTZ operations or PTZ configuration is missing"
                )
                return
            raise

    def stop_ptz(self):
        if not self._is_ptz_supported():
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return

        try:
            self.onvif_client.stop_ptz(profile_token=self.get_main_profile_token())
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                self.logger.warning(
                    "Camera does not support PTZ operations or PTZ configuration is missing"
                )
                return
            raise

    def goto_home_position(self):
        if not self._is_ptz_supported():
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return

        try:
            self.onvif_client.goto_home_position(
                profile_token=self.get_main_profile_token()
            )
        except AttributeError as e:
            if "'NoneType' object has no attribute" in str(e):
                self.logger.warning(
                    "Camera does not support PTZ operations or PTZ configuration is missing"
                )
                return
            raise
