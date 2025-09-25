#!/bin/bash
set -e

echo "Starting build process..."

# Upgrade pip first
pip install --upgrade pip

# Install dependencies with more lenient constraints
pip install --no-cache-dir --force-reinstall fastapi==0.68.0
pip install --no-cache-dir --force-reinstall uvicorn==0.15.0
pip install --no-cache-dir --force-reinstall pydantic==1.10.12
pip install --no-cache-dir --force-reinstall requests==2.28.1
pip install --no-cache-dir --force-reinstall python-dotenv==0.19.0
pip install --no-cache-dir --force-reinstall yt-dlp==2023.7.6

echo "Build completed successfully!"