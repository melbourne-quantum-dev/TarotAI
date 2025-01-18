#!/usr/bin/env bash

# Constants
VENV_DIR=".venv"
PYTHON_VERSION="3.12"
MIN_PYTHON_VERSION="3.12.0"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log() {
    echo -e "[SETUP] $1"
}

success() {
    echo -e "[${GREEN}SUCCESS${NC}] $1"
}

error() {
    echo -e "[${RED}ERROR${NC}] $1"
}

warning() {
    echo -e "[${YELLOW}WARNING${NC}] $1"
}

# Check if Python version meets requirements
check_python_version() {
    local current_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
    local min_version=$MIN_PYTHON_VERSION
    
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed"
        exit 1
    fi
    
    if ! python3 -c "import sys; exit(0 if sys.version_info >= tuple(map(int, '${min_version}'.split('.'))) else 1)"; then
        error "Python version must be >= ${min_version} (current: ${current_version})"
        exit 1
    fi
}

# Check and create required directories
setup_directories() {
    log "Checking data directory structure..."
    
    # Create required directories if they don't exist
    mkdir -p data/{raw,processed,embeddings}
    mkdir -p .cache/{.uv_cache,__pycache__}
    mkdir -p config
    mkdir -p logs
    
    success "Data structure validated"
}

# Check Python dependencies
check_dependencies() {
    log "Checking Python dependencies..."
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        error "pip is not installed"
        exit 1
    fi
    
    # Check if uv is installed
    if ! command -v uv &> /dev/null; then
        error "uv is not installed. Please install it with: pip install uv"
        exit 1
    fi
    
    success "All required Python packages installed"
}

# Clean up existing virtual environment
clean_venv() {
    log "Removing existing virtual environment..."
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
    fi
}

# Create and activate virtual environment
create_venv() {
    log "Creating fresh virtual environment..."
    uv venv --python=python3.12 "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
}

# Install pip in the virtual environment
install_pip() {
    log "Installing pip..."
    uv pip install --no-cache-dir pip || {
        error "Failed to install pip"
        exit 1
    }
}

# Install project dependencies
install_dependencies() {
    log "Installing project dependencies with uv..."
    echo
    
    # Install package with modern resolver
    echo "Installing package in editable mode with modern resolver..."
    uv pip install \
        --resolution=highest \
        --no-cache-dir \
        --strict \
        -r requirements.txt \
        -e . || {
        error "Failed to install package"
        echo "Tip: Check if all required build tools are installed"
        exit 1
    }
    echo "✓ Package installed"
}

# Main setup function
main() {
    echo "[SETUP] Starting TarotAI setup for data processing..."
    
    # Run setup steps
    setup_directories
    check_dependencies
    clean_venv
    create_venv
    install_pip
    install_dependencies
    
    echo "✨ Setup complete! You can now use TarotAI."
}

# Run main function
main
