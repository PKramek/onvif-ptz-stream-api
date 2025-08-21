#!/bin/bash

# Install project dependencies using UV
echo "Installing dependencies with UV..."
uv sync

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Setup complete!"
