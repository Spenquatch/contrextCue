#!/usr/bin/env bash
set -e

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv is not installed! Install it first."
  exit 1
fi

# Create and activate venv if not present
if [ ! -d ".venv" ]; then
  uv venv --python 3.12
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
uv pip install .
uv install --group dev