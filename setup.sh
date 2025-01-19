#!/bin/bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project configuration
PYTHON_VERSION="3.12.3"
VENV_DIR=".venv"
REQUIRED_TOOLS=("python3" "pip" "uv" "direnv")

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

check_dependencies() {
    log_info "Checking dependencies..."
    for tool in "${REQUIRED_TOOLS[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is required but not installed."
        fi
    done
}

setup_directories() {
    log_info "Setting up project directories..."
    mkdir -p src/tarotai/{core,extensions,utils}
    mkdir -p tests/{core,extensions,utils}
    mkdir -p docs/{api,guides}
    mkdir -p data/{raw,processed}
    mkdir -p config
}

clean_venv() {
    if [ -d "$VENV_DIR" ]; then
        log_info "Cleaning existing virtual environment..."
        rm -rf "$VENV_DIR"
    fi
}

create_venv() {
    log_info "Creating virtual environment with Python $PYTHON_VERSION..."
    # Install required system packages
    if ! command -v python3-venv &> /dev/null; then
        log_info "Installing python3-venv..."
        sudo apt-get update
        sudo apt-get install -y python3-venv python3-pip
    fi
    # Create and activate venv
    python3 -m venv .venv
    source .venv/bin/activate
    # Install uv using pip
    pip install uv
}

install_pip() {
    log_info "Upgrading pip..."
    python3 -m pip install --upgrade pip
}

install_dependencies() {
    log_info "Installing project dependencies..."
    source .venv/bin/activate
    uv pip install -e ".[dev,docs]"
}

setup_direnv() {
    log_info "Setting up direnv..."
    if [ ! -f ".envrc" ]; then
        cat > .envrc <<'EOF'
layout python3
export PYTHONPATH=$PWD/src:$PYTHONPATH
export TAROTAI_ENV=development
EOF
        direnv allow
    fi
}

main() {
    log_info "🎴 Setting up TarotAI development environment..."
    
    check_dependencies
    setup_directories
    clean_venv
    create_venv
    install_pip
    install_dependencies
    setup_direnv
    
    log_info "✨ Setup complete! Run 'make install' for development dependencies."
}

# Allow script to be sourced without running main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Script is being run directly
    main
else
    # Script is being sourced
    # Export functions so they can be used in the shell
    export -f log_info
    export -f log_warn
    export -f log_error
    export -f check_dependencies
    export -f setup_directories
    export -f clean_venv
    export -f create_venv
    export -f install_pip
    export -f install_dependencies
    export -f setup_direnv
fi