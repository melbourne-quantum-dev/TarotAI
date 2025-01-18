#!/bin/bash

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[SETUP]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

check_data_structure() {
    log "Checking data directory structure..."
    required_dirs=("data" "data/embeddings" "data/processed")
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            log "Creating directory: $dir"
            mkdir -p "$dir"
        fi
    done
    
    # Check for required data files
    required_files=("data/cards_ordered.json" "data/golden_dawn.pdf")
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            error "Missing required file: $file"
        fi
    done
    success "Data structure validated"
}

check_python_dependencies() {
    log "Checking Python dependencies..."
    required_packages=("PyPDF2" "numpy" "pydantic" "voyageai")
    missing_packages=()
    
    for pkg in "${required_packages[@]}"; do
        if ! python3 -c "import $pkg" &> /dev/null; then
            missing_packages+=("$pkg")
        fi
    done
    
    if [ ${#missing_packages[@]} -ne 0 ]; then
        log "Missing packages detected. Attempting to install..."
        uv pip install --strict "${missing_packages[@]}" || error "Failed to install missing packages"
    fi
    
    success "All required Python packages installed"
}

setup_environment() {
    if [ -d ".venv" ]; then
        log "Removing existing virtual environment..."
        rm -rf .venv
    fi
    
    log "Creating fresh virtual environment..."
    uv venv .venv || error "Failed to create virtual environment"
    source .venv/bin/activate || error "Failed to activate environment"
    
    # Ensure pip is up-to-date
    python -m pip install --upgrade pip || error "Failed to update pip"
}

# Configure uv environment
export UV_INDEX_URL="https://pypi.org/simple"
export UV_CACHE_DIR=".uv_cache"
export UV_PIP_VERSION=">=23.3.2"

verify_dependencies() {
    log "Verifying dependency integrity..."
    uv pip check || {
        error "Dependency integrity check failed"
        echo "Run 'uv pip sync' to fix dependency conflicts"
    }
    success "Dependencies verified"
}

install_dependencies() {
    log "Installing project dependencies with uv..."
    echo
    
    # Purge old cache
    log "Clearing old cache..."
    uv pip cache purge
    
    # Install core dependencies manually first
    log "Installing core dependencies..."
    uv pip install --strict \
        PyPDF2>=3.0.0 \
        numpy>=1.26.0 \
        pydantic>=2.10.5 \
        voyageai>=0.3.0 || {
        error "Failed to install core dependencies"
    }
    
    # Install package with modern resolver
    echo "Installing package in editable mode with modern resolver..."
    uv pip install \
        --resolution=highest \
        --no-cache-dir \
        --strict \
        -e . || {
        error "Failed to install package"
        echo "Tip: Check if all required build tools are installed"
    }
    echo "✓ Package installed"
    
    # Install core dependencies
    echo "Installing core dependencies with strict resolution..."
    if [ -f "requirements.txt" ]; then
        uv pip sync \
            --resolution=highest \
            --strict \
            requirements.txt || {
            error "Failed to sync core dependencies"
            echo "Tip: Check requirements.txt for version conflicts"
        }
        echo "✓ Core dependencies installed"
    else
        echo "⚠ No requirements.txt found - skipping core dependencies"
    fi
    
    # Install dev dependencies
    echo "Installing development dependencies..."
    if [ -f "dev-requirements.txt" ]; then
        uv pip sync \
            --resolution=highest \
            --strict \
            dev-requirements.txt || {
            error "Failed to sync dev dependencies"
            echo "Tip: Check dev-requirements.txt for version conflicts"
        }
        echo "✓ Development dependencies installed"
    else
        echo "⚠ No dev-requirements.txt found - skipping dev dependencies"
    fi
    
    # Verify installation
    echo "Verifying installation..."
    if ! python3 -c "import tarotai" &> /dev/null; then
        error "Failed to verify installation - tarotai package not found"
    fi
    
    # Verify dependency integrity
    verify_dependencies
    
    success "Dependencies installed successfully with modern resolver"
    echo
}

verify_api_keys() {
    log "Verifying API keys..."
    required_keys=("DEEPSEEK_API_KEY" "VOYAGE_API_KEY")
    for key in "${required_keys[@]}"; do
        if [ -z "${!key:-}" ]; then
            error "Missing required API key: $key"
        fi
    done
    success "API keys verified"
}

verify_setup() {
    log "Verifying complete setup..."
    check_data_structure
    check_python_dependencies
    setup_environment
    install_dependencies
    verify_api_keys
    verify_dependencies
    success "Setup verification complete!"
}

clean_setup() {
    log "Cleaning up setup..."
    if [ -d ".venv" ]; then
        log "Removing virtual environment..."
        rm -rf .venv
    fi
    if [ -d ".uv_cache" ]; then
        log "Clearing UV cache..."
        rm -rf .uv_cache
    fi
    success "Cleanup complete!"
}

print_help() {
    echo "Usage: setup.sh [OPTION]"
    echo
    echo "Options:"
    echo "  --verify-keys    Verify required API keys"
    echo "  --verify-deps    Verify dependency integrity"
    echo "  --clean          Clean up existing setup"
    echo "  --verify         Verify complete setup"
    echo "  -h, --help       Show this help message"
    echo
    echo "Running without options performs full setup"
}

main() {
    local action="full"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verify-keys)
                verify_api_keys
                exit 0
                ;;
            --verify-deps)
                verify_dependencies
                exit 0
                ;;
            --clean)
                clean_setup
                exit 0
                ;;
            --verify)
                verify_setup
                exit 0
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            *)
                error "Unknown argument: $1"
                ;;
        esac
        shift
    done

    # Default full setup
    log "Starting TarotAI setup for data processing..."
    check_data_structure
    check_python_dependencies
    setup_environment
    install_dependencies
    verify_api_keys
    verify_dependencies
    success "Setup complete! Ready for data processing 🎴"
    echo
    echo "Next steps:"
    echo "  make process-data"
}

main "$@"
