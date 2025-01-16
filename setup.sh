#!/bin/bash

# TarotAI Setup Script for macOS/Linux

# Configuration
VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
PYTHON_MIN_VERSION="3.10"
SETUP_DIR="scripts/setup"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Functions
function log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

function log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

function log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

function check_python_version() {
    if ! python3 -c "import sys; assert sys.version_info >= (3,10)" &> /dev/null; then
        log_error "Python ${PYTHON_MIN_VERSION} or higher is required. Please install it and try again."
    fi
    log_info "Python version check passed"
}

function install_uv() {
    if ! command -v uv &> /dev/null; then
        log_info "Installing uv..."
        python3 -m pip install uv || log_error "Failed to install uv"
    fi
    log_info "uv is installed"
}

function create_venv() {
    if [ -d "${VENV_DIR}" ]; then
        log_warn "Existing virtual environment found. Resetting..."
        rm -rf "${VENV_DIR}" || log_error "Failed to remove existing virtual environment"
    fi
    
    log_info "Creating virtual environment..."
    uv venv "${VENV_DIR}" || log_error "Failed to create virtual environment"
}

function activate_venv() {
    log_info "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate" || log_error "Failed to activate virtual environment"
}

function install_dependencies() {
    log_info "Installing dependencies..."
    
    # First try with uv
    if uv pip install -r "${REQUIREMENTS}"; then
        log_info "Dependencies installed successfully with uv"
        return
    fi
    
    log_warn "uv installation failed, trying with pip..."
    
    # Fallback to pip if uv fails
    if python3 -m pip install -r "${REQUIREMENTS}"; then
        log_info "Dependencies installed successfully with pip"
    else
        log_error "Failed to install dependencies with both uv and pip"
    fi
}

function verify_installation() {
    log_info "Verifying installation..."
    
    # Install in development mode
    log_info "Installing tarotai in development mode..."
    uv pip install -e . || log_error "Failed to install tarotai package"
    
    # Verify import
    python3 -c "import tarotai; print('TarotAI setup successful!')" || log_error "Setup verification failed"
}

# Main execution
check_python_version
install_uv
create_venv
activate_venv
install_dependencies
verify_installation

log_info ""
log_info "Setup complete! To activate the virtual environment, run:"
log_info "  source ${VENV_DIR}/bin/activate"
log_info ""
log_info "To run tests:"
log_info "  pytest tests/"
