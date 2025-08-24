from onvif import OnvifClient
from pydantic import computed_field
from functools import cached_property
from app.contracts.services.onvif_service import IOnvifService
from urllib.parse import urlparse, urlunparse


class OnvifService(IOnvifService):
    """
    Service for interacting with the ONVIF camera.
    """

    @computed_field  # type: ignore[misc]
    @cached_property
    def onvif_client(self) -> OnvifClient:
        onvif_client = OnvifClient(
            self.settings.ONVIF_CAMERA_IP_ADDRESS,
            self.settings.ONVIF_CAMERA_PORT,
            self.settings.ONVIF_CAMERA_USER,
            self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value(),
        )
        return onvif_client

    def get_profile_tokens(self) -> list[str]:
        return self.onvif_client.get_profile_tokens()

    def get_snapshot_uri(self) -> str:
        profile_tokens = self.get_profile_tokens()
        main_profile_token = profile_tokens[0]

        return self.onvif_client.get_snapshot_uri(main_profile_token)

    def get_stream_uri(self) -> str:
        profile_tokens = self.get_profile_tokens()
        main_profile_token = profile_tokens[0]

        uri = self.onvif_client.get_streaming_uri(main_profile_token)
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
