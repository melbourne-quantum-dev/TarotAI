 # Project variables                                                                                                                       
 PROJECT_NAME := TarotAI                                                                                                                   
 PYTHON := python3                                                                                                                         
 VENV := .venv                                                                                                                             
 VENV_BIN := $(VENV)/bin                                                                                                                   
 PYTHON_VERSION := 3.12.3                                                                                                                  
 SETUP_SCRIPT := ./setup.sh                                                                                                                
                                                                                                                                           
 # Directories                                                                                                                             
 SRC_DIR := src                                                                                                                            
 TESTS_DIR := tests                                                                                                                        
 DOCS_DIR := docs                                                                                                                          
 DATA_DIR := data                                                                                                                          
 CONFIG_DIR := config                                                                                                                      
                                                                                                                                           
 # Python paths                                                                                                                            
 PYTHONPATH := $(SRC_DIR):$(PYTHONPATH)                                                                                                    
 export PYTHONPATH                                                                                                                         
                                                                                                                                           
# Tools
UV := $(VENV_BIN)/uv
PYTEST := $(VENV_BIN)/pytest
BLACK := $(VENV_BIN)/black
MYPY := $(VENV_BIN)/mypy
RUFF := $(VENV_BIN)/ruff                                                                                                                            
                                                                                                                                           
 # Default target                                                                                                                          
 .PHONY: all                                                                                                                               
 all: install test lint format                                                                                                             
                                                                                                                                           
 # First-time setup                                                                                                                        
 .PHONY: bootstrap                                                                                                                         
 bootstrap:                                                                                                                                
     @echo "🎴 Bootstrapping $(PROJECT_NAME)..."                                                                                           
     @chmod +x $(SETUP_SCRIPT)                                                                                                             
     @$(SETUP_SCRIPT)                                                                                                                      
     @echo "✨ Bootstrap complete! Run 'make install' for development dependencies."                                                       
                                                                                                                                           
 # Environment management                                                                                                                  
 .PHONY: clean                                                                                                                             
 clean:                                                                                                                                    
     @echo "Running project cleanup..."                                                                                                    
     @echo "Project root: $(shell pwd)"                                                                                                    
     @echo "🎴 $(PROJECT_NAME)"                                                                                                            
     rm -rf $(VENV)                                                                                                                        
     rm -rf .pytest_cache                                                                                                                  
     rm -rf .mypy_cache                                                                                                                    
     rm -rf .ruff_cache                                                                                                                    
     rm -rf htmlcov                                                                                                                        
     rm -rf .coverage                                                                                                                      
     rm -rf coverage.xml                                                                                                                   
     find . -type d -name "__pycache__" -exec rm -rf {} +                                                                                  
     find . -type f -name "*.pyc" -delete                                                                                                  
                                                                                                                                           
 .PHONY: install                                                                                                                           
 install:                                                                                                                                  
     @if [ ! -f "$(SETUP_SCRIPT)" ]; then \                                                                                                
         echo "Error: setup.sh not found"; \                                                                                               
         exit 1; \                                                                                                                         
     fi                                                                                                                                    
     @chmod +x $(SETUP_SCRIPT)                                                                                                             
     @$(SETUP_SCRIPT)                                                                                                                      
     $(UV) pip install -e ".[dev,docs]"                                                                                                    
                                                                                                                                           
 # Testing                                                                                                                                 
 .PHONY: test                                                                                                                              
 test:                                                                                                                                     
     $(PYTEST) $(TESTS_DIR) -v --cov=$(SRC_DIR) --cov-report=html --cov-report=xml                                                         
                                                                                                                                           
 .PHONY: test-card-manager                                                                                                                 
 test-card-manager:                                                                                                                        
     $(PYTEST) $(TESTS_DIR)/core/test_card_manager.py -vv                                                                                  
                                                                                                                                           
 .PHONY: test-reading-input                                                                                                                
 test-reading-input:                                                                                                                       
     $(PYTEST) $(TESTS_DIR)/core/test_reading_input.py -vv                                                                                 
                                                                                                                                           
 .PHONY: test-golden-dawn                                                                                                                  
 test-golden-dawn:                                                                                                                         
     $(PYTEST) $(TESTS_DIR)/extensions/test_golden_dawn.py -vv                                                                             
                                                                                                                                           
 # Code quality                                                                                                                            
 .PHONY: format                                                                                                                            
 format:                                                                                                                                   
     $(BLACK) $(SRC_DIR) $(TESTS_DIR)                                                                                                      
                                                                                                                                           
 .PHONY: lint                                                                                                                              
 lint:                                                                                                                                     
     $(MYPY) $(SRC_DIR) $(TESTS_DIR)                                                                                                       
     $(RUFF) check $(SRC_DIR) $(TESTS_DIR)                                                                                                 
                                                                                                                                           
 # Data processing                                                                                                                         
 .PHONY: process-data                                                                                                                      
 process-data:                                                                                                                             
     $(PYTHON) scripts/processing/process_golden_dawn.py                                                                                   
     $(PYTHON) scripts/processing/generate_card_data.py                                                                                    
                                                                                                                                           
 # Documentation                                                                                                                           
 .PHONY: docs                                                                                                                              
 docs:                                                                                                                                     
     mkdocs build                                                                                                                          
                                                                                                                                           
 .PHONY: serve-docs                                                                                                                        
 serve-docs:                                                                                                                               
     mkdocs serve                                                                                                                          
                                                                                                                                           
 # Development helpers                                                                                                                     
 .PHONY: update-deps                                                                                                                       
 update-deps:                                                                                                                              
     $(UV) pip compile --upgrade                                                                                                           
     $(UV) pip sync                                                                                                                        
                                                                                                                                           
 .PHONY: validate                                                                                                                          
 validate:                                                                                                                                 
     $(PYTHON) scripts/processing/validate_card_schema.py                                                                                  
                                                                                                                                           
 # Help                                                                                                                                    
 .PHONY: help                                                                                                                              
 help:                                                                                                                                     
     @echo "🎴 $(PROJECT_NAME) Makefile commands:"                                                                                         
     @echo "make bootstrap    - First-time project setup"                                                                                  
     @echo "make clean       - Clean project files and caches"                                                                             
     @echo "make install     - Install project dependencies"                                                                               
     @echo "make test        - Run all tests with coverage"                                                                                
     @echo "make format      - Format code with black"                                                                                     
     @echo "make lint        - Run type checking and linting"                                                                              
     @echo "make process-data- Process Golden Dawn and card data"                                                                          
     @echo "make docs        - Build documentation"                                                                                        
     @echo "make update-deps - Update dependencies using uv" 