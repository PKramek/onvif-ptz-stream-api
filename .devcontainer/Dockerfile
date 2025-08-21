# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.12

RUN apt-get update \
    && apt-get install -y build-essential git \
    curl \
    bash \
    iputils-ping \
    tree \
    telnet \
    fish \
    vim

# Add vscode user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} --create-home --shell /usr/bin/fish ${USERNAME}

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set UV environment variables
ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Switch to vscode user
USER ${USERNAME}
ARG HOME="/home/${USERNAME}"

# Set PATH to include uv
ENV PATH="${HOME}/.local/bin:$PATH"

# Add PYTHONPATH for local development - without this, the import statements in the code will not work in standalone scripts
ENV PYTHONPATH="/workspaces/fast-api-template:${PYTHONPATH}"

# Set working directory
WORKDIR /workspaces/company-research

# Declare Fish as the default shell for future RUN/CMD/ENTRYPOINT
SHELL ["/usr/bin/fish", "-l", "-c"]

# Ensure interactive sessions use Fish
ENV SHELL=/usr/bin/fish

# Note: Dependencies will be installed via setup.sh or postCreateCommand
