# 🎥 ONVIF PTZ Stream API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1+-green.svg)](https://fastapi.tiangolo.com/)
[![ONVIF](https://img.shields.io/badge/ONVIF-Client-0.2.12+-blue.svg)](https://github.com/quatanium/python-onvif-zeep)

> 🚀 **High-performance FastAPI application for ONVIF camera streaming and PTZ control with preset management.**

## ✨ Features

- **🎥 Real-time Video Streaming** - MJPEG streaming with authentication
- **🎮 PTZ Control** - Pan, Tilt, Zoom with velocity control and preset management
- **🔐 Secure Access** - Authentication credentials embedded in stream URIs
- **⚡ FastAPI Framework** - High-performance async web framework
- **🐳 DevContainer Ready** - Complete development environment
- **📦 UV Package Management** - Fast Python dependency management

## 🚀 Quick Start

### Prerequisites
- ONVIF-compliant IP camera
- Network access to camera
- Camera credentials

### Setup
1. **Clone and open in DevContainer**:
   ```bash
   git clone https://github.com/yourusername/onvif-ptz-stream-api.git
   cd onvif-ptz-stream-api
   code .  # Select "Reopen in Container"
   ```

2. **Configure environment**:
   ```bash
   cp .devcontainer/.env.example .devcontainer/.env
   # Edit .env with your camera details
   ```

3. **Run the application**:
   ```bash
   uv run main.py
   ```

API available at `http://localhost:8000`

## 📡 API Endpoints

### PTZ Control (`/api/v1/ptz`)
```http
POST /api/v1/ptz/cameras/ptz          # Complex PTZ movement
POST /api/v1/ptz/left                 # Move left
POST /api/v1/ptz/right                # Move right  
POST /api/v1/ptz/up                   # Move up
POST /api/v1/ptz/down                 # Move down
POST /api/v1/ptz/zoom_in              # Zoom in
POST /api/v1/ptz/zoom_out             # Zoom out
```

### Preset Management
```http
POST /api/v1/ptz/preset               # Create preset
GET  /api/v1/ptz/presets              # List presets
POST /api/v1/ptz/preset/{name}        # Go to preset
DELETE /api/v1/ptz/preset/{name}      # Delete preset
```

### Video Streaming
```http
GET /api/v1/stream/{camera_id}        # Live MJPEG stream
```

### Health Check
```http
GET /health                           # System status
```

## ⚙️ Configuration

### Required Environment Variables
```bash
ONVIF_CAMERA_IP_ADDRESS=192.168.1.100
ONVIF_CAMERA_USER=admin
ONVIF_CAMERA_PASSWORD=your_password
```

### Optional PTZ Settings
```bash
PTZ_PAN_VELOCITY=0.5      # Default pan velocity
PTZ_TILT_VELOCITY=0.5     # Default tilt velocity
PTZ_ZOOM_VELOCITY=0.5     # Default zoom velocity
```

## 🎯 Common Use Cases

### Basic Camera Control
```bash
# Move camera left with default velocity
curl -X POST "http://localhost:8000/api/v1/ptz/left"

# Move camera right with custom velocity
curl -X POST "http://localhost:8000/api/v1/ptz/right?velocity=0.8"
```

### Preset Management
```bash
# Save current position as "home"
curl -X POST "http://localhost:8000/api/v1/ptz/preset?preset_name=home"

# Move to saved preset
curl -X POST "http://localhost:8000/api/v1/ptz/preset/home"
```

### Complex PTZ Movements
```bash
curl -X POST "http://localhost:8000/api/v1/ptz/cameras/ptz" \
  -H "Content-Type: application/json" \
  -d '{
    "pan_velocity": 0.5,
    "tilt_velocity": -0.3,
    "zoom_velocity": 0.2
  }'
```

## 🛠️ Development

### Tools
```bash
# Code quality
uv run ruff check .
uv run mypy .

# Run application
uv run main.py
```

### Dependencies
- **FastAPI 0.116.1+** - Web framework
- **ONVIF-Zeep 0.2.12+** - ONVIF client
- **OpenCV-Python 4.12.0+** - Video processing
- **Pydantic 2.11.7+** - Data validation

## 🐛 Troubleshooting

### Common Issues
1. **Camera Connection**: Verify network access and credentials
2. **PTZ Not Working**: Check if camera supports PTZ operations
3. **Stream Issues**: Verify camera supports MJPEG streaming

### Debug Mode
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## 📚 Resources

- [ONVIF Core Specification](https://www.onvif.org/profiles/specifications/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [UV Package Manager](https://docs.astral.sh/uv/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `uv run pre-commit run --all-files`
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

**🎥 Built for ONVIF camera integration with modern Python tooling**

Made with ❤️ for the surveillance and automation community

</div>
