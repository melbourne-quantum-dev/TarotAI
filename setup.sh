#!/bin/bash

# TarotAI Setup Script for macOS/Linux

# Check Python version
if ! python3 -c 'import sys; assert sys.version_info >= (3,10)' &> /dev/null; then
    echo "Python 3.10 or higher is required. Please install it and try again."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv could not be found. Installing..."
    python3 -m pip install uv || { echo "Failed to install uv"; exit 1; }
fi

# Reset virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Existing virtual environment found. Resetting..."
    rm -rf .venv || { echo "Failed to remove existing virtual environment"; exit 1; }
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv .venv || { echo "Failed to create virtual environment"; exit 1; }

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Ensure pip is installed in the virtual environment
if ! python -m ensurepip --default-pip; then
    echo "Failed to install pip in the virtual environment."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

# Verify installation
echo "Verifying installation..."
python -c "import tarotai; print('TarotAI setup successful!')" || { echo "Setup failed!"; exit 1; }

echo ""
echo "Setup complete! To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "  pytest tests/"
