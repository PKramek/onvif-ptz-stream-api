# 🐍 Python DevContainer Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![UV](https://img.shields.io/badge/uv-package%20manager-green.svg)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![DevContainer](https://img.shields.io/badge/DevContainer-Ready-blue.svg)](https://code.visualstudio.com/docs/devcontainers/containers)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> 🚀 **A modern, production-ready Python development environment using VS Code DevContainers with UV package management and comprehensive code quality tools.**

This template provides a complete, containerized Python development environment that works consistently across different machines and operating systems. Perfect for teams who want to standardize their development setup and onboard new developers quickly.

## ✨ Features

### 🏗️ **Modern Python Development**
- **Python 3.12** - Latest stable Python version
- **UV Package Manager** - Lightning-fast Python package installer and resolver
- **PEP 621 Compliant** - Modern `pyproject.toml` configuration
- **Development Dependencies** - Pre-configured with essential dev tools

### 🐳 **Containerized Development Environment**
- **VS Code DevContainer** - Complete development environment in a container
- **Docker Compose Setup** - Multi-service architecture ready for databases, OTEL collectors, and other services
- **Cross-platform Support** - Works on Intel, AMD, and Apple Silicon
- **Instant Setup** - Zero configuration required for new team members

### 🔧 **Code Quality & Developer Experience**
- **Ruff** - Ultra-fast Python linter and formatter (replaces Black + isort + flake8)
- **MyPy** - Static type checking for better code reliability
- **Pre-commit Hooks** - Automated code quality checks before commits
- **Security Scanning** - Bandit for security vulnerability detection
- **Secret Detection** - Prevent accidental commits of sensitive data

### 🛠️ **VS Code Integration**
- **Rich Extensions** - Python, Ruff, MyPy, GitLens, GitHub Copilot, and more
- **IntelliSense** - Advanced code completion and navigation
- **Debugging Support** - Full debugging capabilities pre-configured
- **Integrated Terminal** - All tools available in the integrated terminal

### 🚀 **Multi-Service Architecture**
- **Docker Compose Ready** - Easily add databases, message queues, OTEL collectors, and other services
- **Service Networking** - Pre-configured backend network for service communication
- **Environment Configuration** - Flexible environment variable management
- **Development Scaling** - Support for complex local development scenarios

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Development Tools](#-development-tools)
- [Code Quality](#-code-quality)
- [Configuration](#-configuration)
- [Adding Services](#-adding-services)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

### Using GitHub Template

1. **Click "Use this template"** button at the top of this repository
2. **Clone your new repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
3. **Open in VS Code** and select "Reopen in Container" when prompted
4. **Start coding!** 🎉

### One-Click Setup with Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/yourusername/python-devcontainer?quickstart=1)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (Latest version)
- **[VS Code](https://code.visualstudio.com/)** (Latest version)
- **[Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)** for VS Code

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 10GB free space minimum
- **Architecture**: x86_64 or ARM64 (Apple Silicon supported)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/python-devcontainer.git
cd python-devcontainer
```

### 2. Open in VS Code

```bash
code .
```

### 3. Reopen in Container

When VS Code opens, you'll see a notification:

> **"Folder contains a Dev Container configuration file. Reopen folder to develop in a container"**

Click **"Reopen in Container"** or:
- Press `F1` → Type "Dev Containers: Reopen in Container"
- Use Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)

### 4. Wait for Container Build

The first time will take a few minutes to:
- Download the base Docker images
- Install Python dependencies
- Configure VS Code extensions
- Set up the development environment

## 📖 Usage

### Running the Sample Application

```bash
# Test the sample application
python main.py

# Expected output:
# Hello from python-devcontainer!
```

### Package Management with UV

```bash
# Install a new package
uv add requests

# Install development dependency
uv add --dev pytest

# Install from lock file
uv sync

# Update dependencies
uv lock --upgrade

# Show installed packages
uv pip list
```

### Code Quality Tools

```bash
# Run linting
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .

# Type checking
mypy main.py

# Run all pre-commit hooks
pre-commit run --all-files

# Security scan
bandit -r .
```

## 📁 Project Structure

```
python-devcontainer/
├── .devcontainer/
│   ├── devcontainer.json      # VS Code DevContainer configuration
│   ├── Dockerfile             # Python development environment
│   ├── docker-compose.yml     # Multi-service setup
│   ├── setup.sh              # Post-creation setup script
│   └── .env.example          # Environment variables template
├── .pre-commit-config.yaml    # Pre-commit hooks configuration
├── pyproject.toml             # Python project configuration
├── uv.lock                   # Dependency lock file
├── main.py                   # Sample Python application
└── README.md                 # This file
```

## 🔧 Development Tools

### Included Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **UV** | Package management | `pyproject.toml` |
| **Ruff** | Linting & formatting | `pyproject.toml` |
| **MyPy** | Type checking | `pyproject.toml` |
| **Bandit** | Security scanning | `pyproject.toml` |
| **PyUpgrade | automatically upgrade syntax | `pyproject.toml` |
| **Pre-commit** | Git hooks | `.pre-commit-config.yaml` |

### VS Code Extensions

Pre-installed extensions for the best development experience:

- **Python** - Python language support
- **Ruff** - Python linting and formatting
- **MyPy Type Checker** - Static type checking
- **Python Typehint** - Enhanced type hint support
- **Python Indent** - Correct Python indentation
- **IntelliCode** - AI-assisted development
- **GitLens** - Enhanced Git capabilities
- **GitHub Copilot** - AI pair programming
- **TODO Tree** - Task management

## ✅ Code Quality

### Automated Quality Checks

This template enforces code quality through multiple layers:

#### Pre-commit Hooks
- **File checks**: Large files, merge conflicts, YAML/TOML syntax
- **Security**: Private key detection, secret scanning
- **Python**: AST validation, debug statement detection
- **Formatting**: Trailing whitespace, end-of-file fixes
- **Code Quality**: Ruff linting and formatting

#### Static Analysis
- **Ruff**: Comprehensive linting (replaces flake8, isort, and more)
- **MyPy**: Static type checking for better code reliability
- **Bandit**: Security vulnerability scanning

#### Configuration

All tools are configured in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true

[tool.bandit]
exclude_dirs = ["tests"]
```

## ⚙️ Configuration

### Environment Variables

The template includes an `.env.example` file for environment variable configuration. Copy and customize it for your needs:

```bash
cp .devcontainer/.env.example .devcontainer/.env
```

Add your environment variables to the `.env` file:

```bash
# Example environment variables
API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:pass@host:port/dbname
DEBUG=true
```

### Customizing the Environment

#### Adding Dependencies

```bash
# Production dependency
uv add package-name

# Development dependency  
uv add --dev package-name

# Optional dependency group
uv add --group group-name package-name
```

#### VS Code Settings

Customize VS Code settings in `.devcontainer/devcontainer.json`:

```json
{
  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      },
      "extensions": [
        "ms-python.python"
      ]
    }
  }
}
```

## 🐳 Adding Services

This template uses Docker Compose, making it easy to add additional services for local development. The setup includes a pre-configured backend network for service communication.

### Example: Adding a Database

Add a PostgreSQL database to your `docker-compose.yml`:

```yaml
services:
  python-devcontainer:
    # ... existing configuration ...
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

volumes:
  postgres_data:
```

### Example: Adding Redis Cache

```yaml
services:
  # ... existing services ...

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - backend
```

### Example: Adding OTEL Collector

```yaml
services:
  # ... existing services ...

  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yml"]
    volumes:
      - ./otel-collector-config.yml:/etc/otel-collector-config.yml
    ports:
      - "8888:8888"   # Prometheus metrics
      - "8889:8889"   # Prometheus exporter metrics
      - "13133:13133" # health_check extension
      - "4317:4317"   # OTLP gRPC receiver
      - "4318:4318"   # OTLP HTTP receiver
    networks:
      - backend
```

### Service Communication

Services can communicate using their service names as hostnames:

```python
# Connect to PostgreSQL from Python container
import psycopg2

conn = psycopg2.connect(
    host="postgres",  # Service name as hostname
    port=5432,
    database="myapp",
    user="postgres",
    password="postgres"
)

# Connect to Redis
import redis

r = redis.Redis(host="redis", port=6379, db=0)
```

## 🐛 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Rebuild container
Ctrl+Shift+P → "Dev Containers: Rebuild Container"

# Or rebuild without cache
Ctrl+Shift+P → "Dev Containers: Rebuild Container Without Cache"
```

#### Python Package Issues
```bash
# Reinstall all packages
uv sync --refresh

# Clear UV cache
uv cache clean
```

#### Service Connection Issues
```bash
# Check all container status
docker ps

# View logs for specific service
docker logs python-devcontainer-<service-name>-1

# Restart specific service
docker restart python-devcontainer-<service-name>-1

# Check network connectivity
docker network ls
docker network inspect python-devcontainer_backend
```

#### Permission Issues (Linux/macOS)
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Performance Tips

- **Enable Docker BuildKit** for faster builds
- **Allocate more memory** to Docker (8GB recommended)
- **Use SSD storage** for better I/O performance
- **Close unnecessary VS Code windows** to save resources
- **Use Docker volumes** for data that needs to persist

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

### Getting Started

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Run** tests and quality checks: `pre-commit run --all-files`
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to the branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### Development Guidelines

- Follow **PEP 8** style guidelines (enforced by Ruff)
- Add **type hints** to all functions
- Write **tests** for new functionality
- Update **documentation** as needed
- Ensure all **quality checks pass**

### Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/) Code of Conduct.

## 📚 Resources

### Documentation
- [VS Code DevContainers](https://code.visualstudio.com/docs/devcontainers/containers)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [Pre-commit Hooks](https://pre-commit.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Learning Materials
- [Python Best Practices](https://realpython.com/python-code-quality/)
- [Docker for Developers](https://docs.docker.com/get-started/)
- [Docker Compose Tutorial](https://docs.docker.com/compose/gettingstarted/)

## 🌟 Why This Template?

### For Individual Developers
- ⚡ **Zero setup time** - Start coding immediately
- 🔧 **Best practices built-in** - Modern tooling pre-configured
- 🛡️ **Quality assurance** - Automated checks prevent issues
- 📚 **Learning opportunity** - Discover modern Python tooling

### For Teams
- 🎯 **Consistent environments** - Same setup for everyone
- 🚀 **Faster onboarding** - New team members productive in minutes
- 👥 **Better collaboration** - Shared tooling and standards
- 🔒 **Security by default** - Built-in security scanning

### For Projects
- 🏗️ **Production-ready** - Follows industry best practices
- 📈 **Scalable foundation** - Easy to extend and customize
- 🧪 **Testing-friendly** - Set up for comprehensive testing
- 📦 **Deployment-ready** - Container-based development to production
- 🐳 **Multi-service ready** - Easy integration with databases, caches, and other services

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **UV Team** for the amazing package manager
- **Astral** for Ruff and the excellent Python tooling
- **Microsoft** for VS Code and DevContainers
- **Docker** for containerization technology
- **Python Community** for the incredible ecosystem

---

<div align="center">

**[⬆ Back to Top](#-python-devcontainer-template)**

Made with ❤️ for the Python community

</div>
