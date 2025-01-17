#!/bin/bash

# TarotAI Setup Script for macOS/Linux/Windows (WSL)

# Configuration
VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
PYTHON_MIN_VERSION="3.10"
SETUP_DIR="scripts/setup"
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"

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
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Windows
        source "${VENV_DIR}/Scripts/activate" || log_error "Failed to activate virtual environment"
    else
        # macOS/Linux
        source "${VENV_DIR}/bin/activate" || log_error "Failed to activate virtual environment"
    fi
}

function setup_environment() {
    log_info "Setting up environment variables..."
    if [ ! -f "${ENV_FILE}" ]; then
        if [ -f "${ENV_EXAMPLE}" ]; then
            cp "${ENV_EXAMPLE}" "${ENV_FILE}"
            log_info "Created .env file from example"
        else
            log_warn "No .env.example file found - you'll need to create your own .env file"
        fi
    else
        log_info ".env file already exists"
    fi
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

function post_setup_instructions() {
    log_info ""
    log_info "Setup complete! To activate the virtual environment, run:"
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        log_info "  .\\.venv\\Scripts\\activate"
    else
        log_info "  source ${VENV_DIR}/bin/activate"
    fi
    log_info ""
    log_info "To run tests:"
    log_info "  pytest tests/"
    log_info ""
    log_info "To start the CLI interface:"
    log_info "  tarotai"
    log_info ""
    log_info "Remember to configure your API keys in the .env file!"
}

# Main execution
check_python_version
install_uv
create_venv
activate_venv
setup_environment
install_dependencies
verify_installation
post_setup_instructions
