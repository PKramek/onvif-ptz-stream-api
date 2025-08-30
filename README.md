# 🎥 ONVIF PTZ Stream API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1+-green.svg)](https://fastapi.tiangolo.com/)
[![ONVIF](https://img.shields.io/badge/ONVIF-Client-0.0.4+-blue.svg)](https://github.com/quatanium/python-onvif-zeep)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0+-orange.svg)](https://opencv.org/)

> 🚀 **A high-performance FastAPI application providing low-latency video streaming and PTZ (Pan-Tilt-Zoom) control for ONVIF cameras.**

This API enables developers to integrate ONVIF camera functionality into their applications, offering real-time video streaming and precise camera control through a RESTful interface. Built with modern Python tooling and containerized development environment.

## ✨ Features

### 🎥 **ONVIF Camera Integration**
- **Real-time Video Streaming** - Low-latency MJPEG streaming from ONVIF cameras
- **PTZ Control** - Pan, Tilt, and Zoom operations with velocity control
- **Camera Discovery** - Automatic camera profile detection and configuration
- **Authentication Support** - Secure camera access with username/password

### 🏗️ **Modern Architecture**
- **FastAPI Framework** - High-performance async web framework
- **Dependency Injection** - Clean service architecture with interfaces
- **Type Safety** - Comprehensive type hints and Pydantic validation
- **Structured Logging** - Structured logging with structlog

### 🔧 **Developer Experience**
- **DevContainer Ready** - Complete development environment in VS Code
- **UV Package Management** - Fast Python dependency management
- **Code Quality Tools** - Ruff, MyPy, and pre-commit hooks
- **Hot Reload** - Development server with automatic reloading

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture Overview](#-architecture-overview)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Development Setup](#-development-setup)
- [Implementation Details](#-implementation-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## 🚀 Quick Start

### Prerequisites

- **ONVIF Camera** - Any ONVIF-compliant IP camera
- **Network Access** - Camera must be accessible from your network
- **Camera Credentials** - Username and password for camera access

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/onvif-ptz-stream-api.git
   cd onvif-ptz-stream-api
   ```

2. **Configure environment variables**:
   ```bash
   cp .devcontainer/.env.example .devcontainer/.env
   ```

3. **Edit `.env` file with your camera details**:
   ```bash
   ONVIF_CAMERA_IP_ADDRESS=192.168.1.100
   ONVIF_CAMERA_PORT=80
   ONVIF_CAMERA_USER=admin
   ONVIF_CAMERA_PASSWORD=your_password_here
   ```

4. **Open in VS Code DevContainer**:
   ```bash
   code .
   # Select "Reopen in Container" when prompted
   ```

5. **Run the application**:
   ```bash
   uv run main.py
   ```

The API will be available at `http://localhost:8000`

## 🏗️ Architecture Overview

### Project Structure

```
onvif-ptz-stream-api/
├── app/
│   ├── api/                    # API layer
│   │   ├── v1/                # API version 1
│   │   │   ├── endpoints/     # Route handlers
│   │   │   │   ├── ptz.py     # PTZ control endpoints
│   │   │   │   └── stream.py  # Video streaming endpoints
│   │   │   └── router.py      # API router configuration
│   │   ├── dependencies.py    # FastAPI dependencies
│   │   └── healthcheck.py     # Health check endpoint
│   ├── core/                  # Core application logic
│   │   ├── app_factory.py     # FastAPI application factory
│   │   ├── config.py          # Configuration management
│   │   ├── enums.py           # Application enums
│   │   ├── logging_config.py  # Logging configuration
│   │   └── types.py           # Custom type definitions
│   ├── contracts/             # Service interfaces
│   │   └── services/          # Service contracts
│   │       └── onvif_service.py
│   ├── services/              # Service implementations
│   │   ├── onvif_service.py   # ONVIF camera service
│   │   ├── health_check.py    # Health check service
│   │   └── shared_services.py # Shared service utilities
│   ├── schemas/               # Pydantic models
│   └── utils/                 # Utility functions
├── .devcontainer/             # Development container setup
├── pyproject.toml             # Project configuration
└── main.py                    # Application entry point
```

### Design Patterns

#### 1. **Dependency Injection Pattern**
The application uses FastAPI's dependency injection system to manage service instances:

```python
# app/api/dependencies.py
OnvifServiceDep = Annotated[IOnvifService, Depends(get_onvif_service)]

# Usage in endpoints
@router.post("/cameras/{camera_id}/ptz")
async def set_ptz_position(
    camera_id: str,
    command: PTZCommand,
    onvif_service: OnvifServiceDep
):
    # Service is automatically injected
    onvif_service.move_pan(command.pan_velocity)
```

#### 2. **Interface Segregation**
Services are defined through abstract base classes for better testability:

```python
# app/contracts/services/onvif_service.py
class IOnvifService(ABC, BaseModel):
    @abstractmethod
    def move_pan(self, pan_velocity: PanVelocityType):
        pass

    @abstractmethod
    def get_stream_uri(self) -> str:
        pass
```

#### 3. **Factory Pattern**
Application creation is handled through a factory function:

```python
# app/core/app_factory.py
def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        # ... configuration
    )
    # ... setup
    return app
```

## 📡 API Endpoints

### PTZ Control Endpoints

#### Get Camera List
```http
GET /api/v1/cameras
```
Returns a list of available cameras (currently returns empty array).

#### Get Camera Status
```http
GET /api/v1/cameras/{camera_id}
```
Returns camera status information.

#### Control PTZ Movement
```http
POST /api/v1/cameras/{camera_id}/ptz
Content-Type: application/json

{
  "pan_velocity": 0.5,
  "tilt_velocity": -0.3,
  "zoom_velocity": 0.0
}
```

**Velocity Ranges:**
- **Pan**: -1.0 (left) to +1.0 (right)
- **Tilt**: -1.0 (down) to +1.0 (up)  
- **Zoom**: -1.0 (zoom out) to +1.0 (zoom in)

#### Get PTZ Position
```http
GET /api/v1/cameras/{camera_id}/ptz/position
```
Returns current PTZ position (currently returns empty object).

#### Return to Home Position
```http
POST /api/v1/cameras/{camera_id}/ptz/home
```
Moves camera to its home/rest position.

### Video Streaming Endpoints

#### Live Video Stream
```http
GET /api/v1/stream/{camera_id}
```
Returns a live MJPEG stream from the specified camera.

**Stream Format:**
- **Content-Type**: `multipart/x-mixed-replace; boundary=frame`
- **Frame Format**: JPEG-encoded frames
- **Streaming**: Continuous frame delivery for real-time viewing

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ONVIF_CAMERA_IP_ADDRESS` | Camera IP address | ✅ | - |
| `ONVIF_CAMERA_PORT` | Camera port | ❌ | 80 |
| `ONVIF_CAMERA_USER` | Camera username | ✅ | - |
| `ONVIF_CAMERA_PASSWORD` | Camera password | ✅ | - |
| `DEBUG` | Enable debug mode | ❌ | false |
| `LOG_LEVEL` | Logging level | ❌ | INFO |
| `ENVIRONMENT` | Environment type | ❌ | development |

### Configuration Management

The application uses Pydantic Settings for type-safe configuration:

```python
# app/core/config.py
class OnvifSettings(BaseSettings):
    ONVIF_CAMERA_IP_ADDRESS: str = Field(
        ..., description="The IP address of the ONVIF camera"
    )
    ONVIF_CAMERA_PORT: int = Field(
        default=80, description="The port of the ONVIF camera"
    )
    # ... other settings

class Settings(BaseSettings):
    onvif: OnvifSettings = Field(default_factory=lambda: OnvifSettings())

    model_config = SettingsConfigDict(frozen=True)
```

## 🛠️ Development Setup

### Using DevContainer (Recommended)

1. **Install VS Code and Docker Desktop**
2. **Install Dev Containers extension**
3. **Clone and open project**
4. **Select "Reopen in Container"**

### Manual Setup

1. **Install Python 3.12+**
2. **Install UV package manager**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Set environment variables**:
   ```bash
   export ONVIF_CAMERA_IP_ADDRESS=192.168.1.100
   export ONVIF_CAMERA_USER=admin
   export ONVIF_CAMERA_PASSWORD=your_password
   ```

5. **Run the application**:
   ```bash
   uv run main.py
   ```

### Development Tools

```bash
# Code quality checks
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy .

# Security scanning
uv run bandit -r .

# Run pre-commit hooks
uv run pre-commit run --all-files
```

## 🔍 Implementation Details

### ONVIF Service Implementation

#### Camera Connection
The ONVIF client is created using cached properties for efficiency:

```python
# app/contracts/services/onvif_service.py
@computed_field
@cached_property
def onvif_client(self) -> OnvifClient:
    return OnvifClient(
        self.settings.ONVIF_CAMERA_IP_ADDRESS,
        self.settings.ONVIF_CAMERA_PORT,
        self.settings.ONVIF_CAMERA_USER,
        self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value(),
    )
```

#### Stream URI Generation
The service automatically adds authentication credentials to stream URIs:

```python
# app/services/onvif_service.py
def get_stream_uri(self) -> str:
    uri = self.onvif_client.get_streaming_uri(self.get_main_profile_token())
    parsed = urlparse(uri)

    # Add username and password to the netloc part
    netloc_with_auth = f"{self.settings.ONVIF_CAMERA_USER}:{self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value()}@{parsed.hostname}"

    # Build new URL with credentials included
    authorized_uri = urlunparse((
        parsed.scheme,
        netloc_with_auth,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))
    return authorized_uri
```

#### Error Handling
PTZ operations include graceful error handling for unsupported cameras:

```python
def move_pan(self, pan_velocity: PanVelocityType):
    try:
        self.onvif_client.move_pan(
            profile_token=self.get_main_profile_token(),
            velocity=pan_velocity
        )
    except AttributeError as e:
        if "'NoneType' object has no attribute" in str(e):
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return
        raise
```

### Video Streaming Implementation

#### Frame Generation
The streaming endpoint uses OpenCV for frame capture and encoding:

```python
# app/api/v1/endpoints/stream.py
def generate_frames():
    cap = cv2.VideoCapture(stream_uri)
    if not cap.isOpened():
        logger.error(f"Cannot open video stream for {camera_id}")
        return

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            ret, jpeg = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = jpeg.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame_bytes + b"\r\n"
            )
    finally:
        cap.release()
```

#### MJPEG Response
Returns a proper MJPEG multipart response for browser compatibility:

```python
return StreamingResponse(
    generate_frames(),
    media_type="multipart/x-mixed-replace; boundary=frame",
)
```

### Type System

The application uses custom types for PTZ operations:

```python
# app/core/types.py
PanVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
TiltVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
ZoomVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
```

## 🐛 Troubleshooting

### Common Issues

#### Camera Connection Problems

1. **Check network connectivity**:
   ```bash
   ping 192.168.1.100
   telnet 192.168.1.100 80
   ```

2. **Verify ONVIF support**:
   - Ensure camera supports ONVIF protocol
   - Check if ONVIF is enabled in camera settings
   - Verify correct port (usually 80 or 8080)

3. **Authentication issues**:
   - Verify username/password are correct
   - Check if camera requires special characters in credentials
   - Ensure user has PTZ permissions

#### Streaming Issues

1. **Frame drops or lag**:
   - Check network bandwidth
   - Reduce frame quality in camera settings
   - Verify camera supports MJPEG streaming

2. **No video output**:
   - Check if stream URI is accessible
   - Verify camera profile tokens
   - Check browser compatibility (MJPEG support)

#### PTZ Control Issues

1. **Camera doesn't move**:
   - Verify PTZ is enabled in camera settings
   - Check if camera supports requested movement
   - Ensure user has PTZ control permissions

2. **Erratic movement**:
   - Check velocity values (should be between -1.0 and 1.0)
   - Verify camera calibration
   - Test with smaller velocity values

### Debug Mode

Enable debug mode for detailed logging:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Log Analysis

The application uses structured logging. Look for these log patterns:

```bash
# Check for ONVIF connection issues
grep "ONVIF" logs/app.log

# Check for streaming errors
grep "stream" logs/app.log

# Check for PTZ operation failures
grep "PTZ" logs/app.log
```

## 🔧 **Developer Implementation Guide**

This section provides detailed information for developers who need to understand how the API was implemented, extend functionality, or troubleshoot issues.

### **Core Implementation Patterns**

#### **1. ONVIF Client Management**
The ONVIF client is implemented using cached properties to avoid recreating connections:

```python
# app/contracts/services/onvif_service.py
@computed_field
@cached_property
def onvif_client(self) -> OnvifClient:
    return OnvifClient(
        self.settings.ONVIF_CAMERA_IP_ADDRESS,
        self.settings.ONVIF_CAMERA_PORT,
        self.settings.ONVIF_CAMERA_USER,
        self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value(),
    )
```

**Why this approach?** ONVIF connections can be expensive to establish, so we cache the client instance. The `@cached_property` ensures the client is only created once per service instance.

#### **2. Stream URI Authentication**
Stream URIs are automatically modified to include authentication credentials:

```python
# app/services/onvif_service.py
def get_stream_uri(self) -> str:
    uri = self.onvif_client.get_streaming_uri(self.get_main_profile_token())
    parsed = urlparse(uri)

    # Add username and password to the netloc part
    netloc_with_auth = f"{self.settings.ONVIF_CAMERA_USER}:{self.settings.ONVIF_CAMERA_PASSWORD.get_secret_value()}@{parsed.hostname}"

    # Build new URL with credentials included
    authorized_uri = urlunparse((
        parsed.scheme,
        netloc_with_auth,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))
    return authorized_uri
```

**Implementation note:** This approach embeds credentials directly in the URL, which is necessary for some ONVIF cameras that don't support HTTP authentication headers.

#### **3. PTZ Error Handling Strategy**
PTZ operations include graceful fallbacks for unsupported cameras:

```python
def move_pan(self, pan_velocity: PanVelocityType):
    try:
        self.onvif_client.move_pan(
            profile_token=self.get_main_profile_token(),
            velocity=pan_velocity
        )
    except AttributeError as e:
        if "'NoneType' object has no attribute" in str(e):
            self.logger.warning(
                "Camera does not support PTZ operations or PTZ configuration is missing"
            )
            return
        raise
```

**Why this pattern?** Not all ONVIF cameras support PTZ operations. This error handling allows the API to work with cameras that only support streaming.

### **Video Streaming Implementation Details**

#### **Frame Processing Pipeline**
The streaming endpoint uses OpenCV for efficient frame processing:

```python
# app/api/v1/endpoints/stream.py
def generate_frames():
    cap = cv2.VideoCapture(stream_uri)
    if not cap.isOpened():
        logger.error(f"Cannot open video stream for {camera_id}")
        return

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            ret, jpeg = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = jpeg.tobytes()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame_bytes + b"\r\n"
            )
    finally:
        cap.release()
```

**Key implementation decisions:**
- **JPEG encoding**: Chosen for browser compatibility and reasonable compression
- **Generator pattern**: Memory-efficient streaming without buffering all frames
- **Error handling**: Graceful degradation when frames can't be read

#### **MJPEG Response Format**
The API returns proper MJPEG multipart responses:

```python
return StreamingResponse(
    generate_frames(),
    media_type="multipart/x-mixed-replace; boundary=frame",
)
```

**Why MJPEG?** This format is widely supported by browsers and provides low-latency streaming suitable for real-time camera monitoring.

### **Configuration Management Architecture**

#### **Settings Inheritance Pattern**
Configuration uses Pydantic's nested settings for clean organization:

```python
# app/core/config.py
class OnvifSettings(BaseSettings):
    ONVIF_CAMERA_IP_ADDRESS: str = Field(..., description="The IP address of the ONVIF camera")
    ONVIF_CAMERA_PORT: int = Field(default=80, description="The port of the ONVIF camera")
    # ... other settings

class Settings(BaseSettings):
    onvif: OnvifSettings = Field(default_factory=lambda: OnvifSettings())

    model_config = SettingsConfigDict(frozen=True)
```

**Benefits of this approach:**
- **Type safety**: All settings are validated at startup
- **Environment variable mapping**: Automatic mapping from environment variables
- **Immutable settings**: Prevents runtime configuration changes
- **Nested organization**: Groups related settings logically

### **Dependency Injection System**

#### **Service Registration Pattern**
Services are registered using FastAPI's dependency injection:

```python
# app/api/dependencies.py
def get_onvif_service() -> IOnvifService:
    settings = get_settings()
    logger = get_logger()
    return OnvifService(settings=settings.onvif, logger=logger)

OnvifServiceDep = Annotated[IOnvifService, Depends(get_onvif_service)]
```

**Usage in endpoints:**
```python
@router.post("/cameras/{camera_id}/ptz")
async def set_ptz_position(
    camera_id: str,
    command: PTZCommand,
    onvif_service: OnvifServiceDep
):
    # Service is automatically injected and ready to use
    onvif_service.move_pan(command.pan_velocity)
```

### **Type System Design**

#### **Custom Type Definitions**
PTZ operations use constrained numeric types:

```python
# app/core/types.py
PanVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
TiltVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
ZoomVelocityType = Annotated[float, Field(ge=-1.0, le=1.0)]
```

**Why these constraints?** ONVIF cameras expect velocity values in the range [-1.0, 1.0], where:
- **0.0** = no movement
- **Positive values** = movement in primary direction
- **Negative values** = movement in opposite direction

### **Performance Considerations**

#### **Memory Management**
- **Streaming**: Uses generators to avoid buffering entire video streams in memory
- **ONVIF Client**: Cached to prevent connection overhead
- **Frame Processing**: Direct frame-to-JPEG conversion without intermediate storage

#### **Network Optimization**
- **Connection Reuse**: ONVIF client connections are reused
- **Streaming**: Direct camera-to-client streaming without proxy buffering
- **Error Recovery**: Automatic reconnection attempts for failed operations

### **Security Implementation**

#### **Credential Management**
- **Environment Variables**: Credentials stored in environment variables, not in code
- **Secret Types**: Pydantic's `SecretStr` for password fields
- **URL Embedding**: Credentials embedded in stream URLs for camera compatibility

#### **Input Validation**
- **Pydantic Models**: All API inputs validated through Pydantic schemas
- **Type Constraints**: Numeric values constrained to valid ranges
- **Path Parameters**: Camera IDs validated as strings

### **Testing Strategy**

#### **Service Layer Testing**
Services can be tested independently using mock ONVIF clients:

```python
# Example test pattern
def test_onvif_service_move_pan():
    mock_client = MockOnvifClient()
    service = OnvifService(settings=mock_settings, logger=mock_logger)
    service.onvif_client = mock_client

    service.move_pan(0.5)
    mock_client.move_pan.assert_called_once_with(
        profile_token="profile_token",
        velocity=0.5
    )
```

#### **API Testing**
Endpoints can be tested using FastAPI's test client:

```python
from fastapi.testclient import TestClient

def test_ptz_endpoint():
    client = TestClient(app)
    response = client.post(
        "/api/v1/cameras/test-camera/ptz",
        json={"pan_velocity": 0.5, "tilt_velocity": 0.0, "zoom_velocity": 0.0}
    )
    assert response.status_code == 200
```

### **Common Development Scenarios**

#### **Adding New PTZ Commands**
1. **Extend the interface** in `app/contracts/services/onvif_service.py`
2. **Implement the method** in `app/services/onvif_service.py`
3. **Add the endpoint** in `app/api/v1/endpoints/ptz.py`
4. **Update schemas** if new data models are needed

#### **Supporting New Camera Types**
1. **Check ONVIF compliance** - ensure camera follows ONVIF standards
2. **Test profile tokens** - verify camera returns valid profile information
3. **Validate PTZ support** - check if camera supports requested operations
4. **Handle edge cases** - implement fallbacks for unsupported features

#### **Performance Tuning**
1. **Monitor frame rates** - adjust JPEG quality for optimal performance
2. **Network optimization** - ensure sufficient bandwidth for streaming
3. **Memory usage** - monitor for memory leaks in long-running streams
4. **Error recovery** - implement exponential backoff for failed operations

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes** following the existing patterns:
   - Use dependency injection for services
   - Implement interfaces for new services
   - Add comprehensive type hints
   - Include error handling

4. **Run quality checks**:
   ```bash
   uv run pre-commit run --all-files
   ```

5. **Test your changes**:
   ```bash
   # Test with your ONVIF camera
   uv run main.py
   ```

6. **Submit a pull request**

### Code Standards

- **Type Hints**: All functions must include type hints
- **Error Handling**: Graceful error handling for camera operations
- **Logging**: Structured logging for debugging
- **Documentation**: Docstrings for all public methods
- **Testing**: Unit tests for new functionality

### Adding New Features

#### New PTZ Operations
1. **Add method to interface** (`app/contracts/services/onvif_service.py`)
2. **Implement in service** (`app/services/onvif_service.py`)
3. **Add endpoint** (`app/api/v1/endpoints/ptz.py`)
4. **Update schemas** if needed

#### New Camera Features
1. **Extend configuration** (`app/core/config.py`)
2. **Add service methods** following existing patterns
3. **Create new endpoints** in appropriate router
4. **Update dependencies** if needed

## 📚 Resources

### ONVIF Documentation
- [ONVIF Core Specification](https://www.onvif.org/profiles/specifications/)
- [ONVIF Device Service](https://www.onvif.org/profiles/specifications/device/)
- [ONVIF Media Service](https://www.onvif.org/profiles/specifications/media/)
- [ONVIF PTZ Service](https://www.onvif.org/profiles/specifications/ptz/)

### Python Libraries
- [python-onvif-zeep](https://github.com/quatanium/python-onvif-zeep) - ONVIF client library
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html) - Computer vision library
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework documentation

### Development Tools
- [UV Package Manager](https://docs.astral.sh/uv/) - Fast Python package management
- [Ruff](https://docs.astral.sh/ruff/) - Python linter and formatter
- [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) - VS Code container development

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ONVIF Forum** for the camera communication protocol
- **FastAPI Team** for the excellent web framework
- **OpenCV Community** for computer vision capabilities
- **Python Community** for the rich ecosystem of tools

---

<div align="center">

**🎥 Built for ONVIF camera integration with modern Python tooling**

Made with ❤️ for the surveillance and automation community

</div>
