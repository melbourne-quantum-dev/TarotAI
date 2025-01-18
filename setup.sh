 #!/usr/bin/env bash                                                                                                                       
                                                                                                                                           
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
 }                                                                                                                                         
                                                                                                                                           
 setup_directories() {                                                                                                                     
     log_info "Setting up project directories..."                                                                                          
     mkdir -p src/tarotai/{core,ai,ui,extensions}                                                                                          
     mkdir -p tests/{core,ai,ui,extensions}                                                                                                
     mkdir -p data/{cards,embeddings,knowledge}                                                                                            
     mkdir -p docs/{architecture,api}                                                                                                      
 }                                                                                                                                         
                                                                                                                                           
 check_dependencies() {                                                                                                                    
     log_info "Checking dependencies..."                                                                                                   
     local missing_deps=()                                                                                                                 
                                                                                                                                           
     for tool in "${REQUIRED_TOOLS[@]}"; do                                                                                                
         if ! command -v "$tool" &> /dev/null; then                                                                                        
             missing_deps+=("$tool")                                                                                                       
         fi                                                                                                                                
     done                                                                                                                                  
                                                                                                                                           
     if [ ${#missing_deps[@]} -ne 0 ]; then                                                                                                
         log_error "Missing required tools: ${missing_deps[*]}"                                                                            
         log_info "Please install missing dependencies:"                                                                                   
         log_info "For Ubuntu/Debian:"                                                                                                     
         log_info "  sudo apt update && sudo apt install python3 python3-pip direnv"                                                       
         log_info "Install uv:"                                                                                                            
         log_info "  curl -LsSf https://astral.sh/uv/install.sh | sh"                                                                      
         exit 1                                                                                                                            
     fi                                                                                                                                    
 }                                                                                                                                         
                                                                                                                                           
 clean_venv() {                                                                                                                            
     if [ -d "$VENV_DIR" ]; then                                                                                                           
         log_info "Cleaning existing virtual environment..."                                                                               
         rm -rf "$VENV_DIR"                                                                                                                
     fi                                                                                                                                    
 }                                                                                                                                         
                                                                                                                                           
 create_venv() {                                                                                                                           
     log_info "Creating virtual environment with Python $PYTHON_VERSION..."                                                                
     uv venv                                                                                                                               
 }                                                                                                                                         
                                                                                                                                           
 install_pip() {                                                                                                                           
     log_info "Upgrading pip..."                                                                                                           
     "$VENV_DIR/bin/python" -m pip install --upgrade pip                                                                                   
 }                                                                                                                                         
                                                                                                                                           
 install_dependencies() {                                                                                                                  
     log_info "Installing project dependencies..."                                                                                         
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
                                                                                                                                           
     log_info "✨ Setup complete! Your development environment is ready."                                                                  
     log_info "Next steps:"                                                                                                                
     log_info "1. Run 'make test' to verify the installation"                                                                              
     log_info "2. Check 'make help' for available commands"                                                                                
 }                                                                                                                                         
                                                                                                                                           
 # Allow script to be sourced without running main                                                                                         
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then                                                                                              
     # Script is being run directly                                                                                                        
     main                                                                                                                                  
 else                                                                                                                                      
     # Script is being sourced (by Makefile)                                                                                               
     # Export functions for use in Makefile                                                                                                
     export -f setup_directories                                                                                                           
     export -f check_dependencies                                                                                                          
     export -f clean_venv                                                                                                                  
     export -f create_venv                                                                                                                 
     export -f install_pip                                                                                                                 
     export -f install_dependencies                                                                                                        
     export -f setup_direnv                                                                                                                
 fi          
 
