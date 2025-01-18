#!/bin/bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[SETUP]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

check_python_version() {
    local python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    (( $(echo "$python_version < 3.12" | bc -l) )) && error "Python 3.12.x required. Current: $python_version"
    log "Python version $python_version detected"
}

check_uv() {
    if ! command -v uv &> /dev/null; then
        log "Installing UV package manager..."
        python3 -m pip install --quiet --upgrade pip
        python3 -m pip install --quiet uv
        success "UV installed successfully"
    else
        log "UV already installed"
    fi
}

cleanup() {
    log "Cleaning up previous installation..."
    python3 scripts/dev/cleanup.py --verbose
    success "Cleanup completed"
}

setup_environment() {
    if [ -d ".venv" ]; then
        log "Existing virtual environment found"
        source .venv/bin/activate || error "Failed to activate existing environment"
        log "Updating dependencies..."
    else
        log "Creating fresh virtual environment..."
        cleanup
        uv venv .venv || error "Failed to create virtual environment"
        source .venv/bin/activate || error "Failed to activate environment"
    fi
}

install_dependencies() {
    log "Installing project dependencies..."
    uv pip install --quiet -e ".[dev]" || error "Failed to install dependencies"
    success "Dependencies installed successfully"
}

setup_config() {
    if [ ! -f "assistant_config.yml" ]; then
        cp config/assistant_config.example.yml assistant_config.yml || error "Failed to create assistant config"
        log "Created assistant_config.yml"
    else
        log "assistant_config.yml already exists"
    fi

    if [ ! -f ".env" ]; then
        cp .env.example .env || error "Failed to create .env"
        log "Created .env file"
    else
        log ".env already exists"
    fi
    
    log "Please configure your API keys in the .env file"
}

verify_installation() {
    log "Verifying installation..."
    python3 -c "import tarotai; print('🔮 TarotAI imported successfully!')" || error "Installation verification failed"
    uv --version &> /dev/null || error "UV verification failed"
    success "Installation verified successfully!"
}

main() {
    log "Starting TarotAI setup..."
    command -v python3 &> /dev/null || error "Python 3.12+ is required"
    check_python_version
    check_uv
    setup_environment
    install_dependencies
    setup_config
    verify_installation
    echo
    success "Setup complete! 🎉"
    echo
    echo "To activate the environment:"
    echo "  source .venv/bin/activate"
    echo
    echo "Quick start:"
    echo "  1. Configure API keys in .env"
    echo "  2. Run 'make validate' to verify setup"
    echo "  3. Run 'make check' to run all tests"
}

main "$@"
