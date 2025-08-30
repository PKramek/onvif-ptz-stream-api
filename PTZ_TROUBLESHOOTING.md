# 🎮 PTZ Troubleshooting Guide

This guide helps you diagnose and fix PTZ (Pan-Tilt-Zoom) issues with your ONVIF camera.

## 🚨 Common Error: `AttributeError("'NoneType' object has no attribute 'PanTilt'")`

### **What This Error Means**

This error occurs when your ONVIF camera:
1. ✅ **Supports ONVIF protocol** (can get profile tokens, stream URIs)
2. ❌ **Has incomplete PTZ service implementation** (PTZ service is `None`)
3. ❌ **Doesn't support PTZ operations** despite appearing to be ONVIF compliant

### **Why This Happens**

- **Camera Limitations**: Some cameras only implement basic ONVIF features (streaming) but not PTZ
- **Firmware Issues**: Camera firmware may have incomplete ONVIF implementation
- **Configuration Problems**: PTZ may be disabled in camera settings
- **Library Compatibility**: The `onvif-client` library expects certain PTZ service attributes

## 🔍 **Diagnosis Steps**

### **1. Test PTZ Capabilities**

Use the new `/api/v1/cameras/{camera_id}/ptz/capabilities` endpoint:

```bash
curl http://localhost:8000/api/v1/cameras/test-camera/ptz/capabilities
```

**Expected Response for Working PTZ:**
```json
{
  "ptz_supported": true,
  "pan_supported": true,
  "tilt_supported": true,
  "zoom_supported": true,
  "home_position_supported": true,
  "error": null
}
```

**Expected Response for Non-Working PTZ:**
```json
{
  "ptz_supported": false,
  "pan_supported": false,
  "tilt_supported": false,
  "zoom_supported": false,
  "home_position_supported": false,
  "error": "PTZ service not available"
}
```

### **2. Run the Test Script**

Use the diagnostic script to test your camera:

```bash
python test_ptz_capabilities.py
```

This script will:
- Test ONVIF connection
- Check profile tokens
- Verify stream URI access
- Test PTZ capabilities
- Attempt small PTZ movements (if supported)

### **3. Check Camera Settings**

Verify in your camera's web interface:
- [ ] ONVIF is enabled
- [ ] PTZ is enabled
- [ ] User has PTZ permissions
- [ ] PTZ is not locked/disabled

## 🛠️ **Solutions Implemented**

### **1. PTZ Service Validation**

The service now checks if PTZ is available before attempting operations:

```python
def _is_ptz_supported(self) -> bool:
    try:
        # Check if PTZ service exists and is properly initialized
        if not hasattr(self.onvif_client, 'ptz') or self.onvif_client.ptz is None:
            return False

        # Try to get PTZ configurations to verify service is working
        self.onvif_client.ptz.GetConfigurations()
        return True
    except (AttributeError, Exception):
        return False
```

### **2. Graceful Fallbacks**

All PTZ methods now check support before execution:

```python
def move_pan(self, pan_velocity: PanVelocityType):
    if not self._is_ptz_supported():
        self.logger.warning("Camera does not support PTZ operations")
        return

    # ... execute movement
```

### **3. Better Error Reporting**

The API now returns detailed capability information:

```json
{
  "success": false,
  "error": "Camera does not support PTZ operations",
  "capabilities": {
    "ptz_supported": false,
    "pan_supported": false,
    "tilt_supported": false,
    "zoom_supported": false,
    "home_position_supported": false,
    "error": "PTZ service not available"
  }
}
```

## 🔧 **Camera-Specific Fixes**

### **For Dahua Cameras**
- Enable ONVIF in **Configuration → Network → Advanced Settings → Integration Protocol**
- Enable PTZ in **Configuration → PTZ → PTZ**
- Ensure user has PTZ permissions

### **For Hikvision Cameras**
- Enable ONVIF in **Configuration → Network → Advanced Settings → Integration Protocol**
- Enable PTZ in **Configuration → PTZ → PTZ**
- Check **Configuration → PTZ → PTZ → Advanced → Protocol Priority**

### **For Generic ONVIF Cameras**
- Look for ONVIF settings in **Configuration → Network → Advanced**
- Check for PTZ settings in **Configuration → PTZ** or **Configuration → Camera**
- Verify user permissions include PTZ control

## 📊 **Testing Your Fixes**

### **1. Test Basic Connection**
```bash
curl http://localhost:8000/api/v1/cameras/test-camera/ptz/capabilities
```

### **2. Test PTZ Movement**
```bash
curl -X POST http://localhost:8000/api/v1/cameras/test-camera/ptz \
  -H "Content-Type: application/json" \
  -d '{"pan_velocity": 0.1, "tilt_velocity": 0.0, "zoom_velocity": 0.0}'
```

### **3. Test Home Position**
```bash
curl -X POST http://localhost:8000/api/v1/cameras/test-camera/ptz/home
```

## 🚫 **What Won't Work**

- **Cameras without PTZ hardware** (fixed cameras)
- **Cameras with broken ONVIF implementation**
- **Cameras where PTZ is locked by firmware**
- **Cameras requiring proprietary protocols**

## 📚 **Additional Resources**

- [ONVIF PTZ Service Error Discussion](https://community.home-assistant.io/t/onvif-ptz-service-error/181093)
- [ONVIF Client Library Documentation](https://github.com/quatanium/python-onvif-zeep)
- [ONVIF Standard Specifications](https://www.onvif.org/profiles/specifications/)

## 🆘 **Still Having Issues?**

If the problem persists:

1. **Check camera logs** for ONVIF-related errors
2. **Verify network connectivity** to the camera
3. **Test with ONVIF Device Manager** (Windows tool)
4. **Contact camera manufacturer** for ONVIF support
5. **Consider alternative PTZ libraries** if available

---

**Remember**: Not all ONVIF cameras support PTZ operations. The API now gracefully handles this and provides clear feedback about what your camera supports.
