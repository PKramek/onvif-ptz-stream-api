#!/usr/bin/env python3
"""
Test script to diagnose ONVIF PTZ capabilities.
Run this script to check if your camera supports PTZ operations.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.core.config import get_settings
from app.services.onvif_service import OnvifService
import structlog


def test_onvif_connection():
    """Test basic ONVIF connection and PTZ capabilities."""
    try:
        # Get settings and create service
        settings = get_settings()
        logger = structlog.get_logger()

        print("🔍 Testing ONVIF connection...")
        print(f"📷 Camera IP: {settings.onvif.ONVIF_CAMERA_IP_ADDRESS}")
        print(f"🔌 Port: {settings.onvif.ONVIF_CAMERA_PORT}")
        print(f"👤 Username: {settings.onvif.ONVIF_CAMERA_USER}")
        print(
            f"🔑 Password: {'*' * len(settings.onvif.ONVIF_CAMERA_PASSWORD.get_secret_value())}"
        )
        print()

        # Create ONVIF service
        service = OnvifService(settings=settings.onvif, logger=logger)

        # Test basic connection
        print("📋 Testing profile tokens...")
        try:
            profile_tokens = service.get_profile_tokens()
            print(f"✅ Profile tokens: {profile_tokens}")
        except Exception as e:
            print(f"❌ Failed to get profile tokens: {e}")
            return False

        # Test stream URI
        print("📺 Testing stream URI...")
        try:
            stream_uri = service.get_stream_uri()
            print(f"✅ Stream URI: {stream_uri}")
        except Exception as e:
            print(f"❌ Failed to get stream URI: {e}")
            return False

        # Test PTZ capabilities
        print("🎮 Testing PTZ capabilities...")
        try:
            capabilities = service.get_ptz_capabilities()
            print("📊 PTZ Capabilities:")
            for key, value in capabilities.items():
                if key == "error" and value:
                    print(f"  ❌ {key}: {value}")
                elif key == "error":
                    print(f"  ✅ {key}: None")
                else:
                    status = "✅" if value else "❌"
                    print(f"  {status} {key}: {value}")
        except Exception as e:
            print(f"❌ Failed to get PTZ capabilities: {e}")
            return False

        # Test PTZ operations if supported
        if capabilities.get("ptz_supported"):
            print("\n🎯 Testing PTZ operations...")

            # Test pan movement
            if capabilities.get("pan_supported"):
                print("  🔄 Testing pan movement...")
                try:
                    service.move_pan(0.1)  # Small movement
                    print("    ✅ Pan movement successful")
                except Exception as e:
                    print(f"    ❌ Pan movement failed: {e}")

            # Test tilt movement
            if capabilities.get("tilt_supported"):
                print("  🔽 Testing tilt movement...")
                try:
                    service.move_tilt(0.1)  # Small movement
                    print("    ✅ Tilt movement successful")
                except Exception as e:
                    print(f"    ❌ Tilt movement failed: {e}")

            # Test stop
            print("  ⏹️ Testing stop...")
            try:
                service.stop_ptz()
                print("    ✅ Stop successful")
            except Exception as e:
                print(f"    ❌ Stop failed: {e}")

        print("\n🎉 ONVIF connection test completed!")
        return True

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def main():
    """Main function to run the test."""
    print("🚀 ONVIF PTZ Capability Test")
    print("=" * 40)

    # Check if environment variables are set
    required_vars = [
        "ONVIF_CAMERA_IP_ADDRESS",
        "ONVIF_CAMERA_USER",
        "ONVIF_CAMERA_PASSWORD",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables before running the test.")
        return 1

    success = test_onvif_connection()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
