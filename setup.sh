#!/bin/bash

# TarotAI Setup Script for macOS/Linux

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv could not be found. Installing..."
    pip install uv
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Verify installation
echo "Verifying installation..."
python -c "import tarotai; print('TarotAI setup successful!')" || echo "Setup failed!"

echo ""
echo "Setup complete! To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
