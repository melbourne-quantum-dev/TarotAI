#!/bin/bash

# Add pre-flight checks
if ! command -v python3 &> /dev/null; then
    echo "Python 3.12+ is required. Please install it first."
    exit 1
fi

# Add version check
python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$python_version < 3.12" | bc -l) )); then
    echo "Python 3.12+ is required. Current version: $python_version"
    exit 1
fi

# Add cleanup function
function cleanup() {
    echo "Cleaning up..."
    rm -rf .venv/ __pycache__/ .pytest_cache/ .mypy_cache/
    find . -name '*.pyc' -delete
    find . -name '*.pyo' -delete
    find . -name '__pycache__' -delete
}

# Add dependency caching
if [ -d ".venv" ]; then
    echo "Existing virtual environment found. Updating..."
    source .venv/bin/activate
else
    # Create fresh environment
    cleanup
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Install uv if not present
    if ! command -v uv &> /dev/null; then
        python3 -m pip install --upgrade pip
        python3 -m pip install uv
    fi
fi

# Install dependencies
uv pip install -e ".[dev]"

# Create config files if missing
if [ ! -f "assistant_config.yml" ]; then
    echo "Creating assistant_config.yml from template..."
    cp config/assistant_config.example.yml assistant_config.yml
fi

if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please configure your API keys in the .env file"
fi

# Add post-install verification
echo "Verifying installation..."
python3 -c "import tarotai; print('Installation successful!')" || {
    echo "Installation verification failed"
    exit 1
}

echo "Setup complete! To activate the environment:"
echo "  source .venv/bin/activate"
