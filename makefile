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
 \t@echo "🎴 Bootstrapping $(PROJECT_NAME)..."                                                                                           
 \t@chmod +x $(SETUP_SCRIPT)                                                                                                             
 \t@$(SETUP_SCRIPT)                                                                                                                      
 \t@echo "✨ Bootstrap complete! Run 'make install' for development dependencies."                                                       
                                                                                                                                           
 # Environment management                                                                                                                  
 .PHONY: clean                                                                                                                             
 clean:                                                                                                                                    
 \t@echo "Running project cleanup..."                                                                                                    
 \t@echo "Project root: $(shell pwd)"                                                                                                    
 \t@echo "🎴 $(PROJECT_NAME)"                                                                                                            
 \trm -rf $(VENV)                                                                                                                        
 \trm -rf .pytest_cache                                                                                                                  
 \trm -rf .mypy_cache                                                                                                                    
 \trm -rf .ruff_cache                                                                                                                    
 \trm -rf htmlcov                                                                                                                        
 \trm -rf .coverage                                                                                                                      
 \trm -rf coverage.xml                                                                                                                   
 \tfind . -type d -name "__pycache__" -exec rm -rf {} +                                                                                  
 \tfind . -type f -name "*.pyc" -delete                                                                                                  
                                                                                                                                           
 .PHONY: install                                                                                                                           
 install:                                                                                                                                  
 \t@if [ ! -f "$(SETUP_SCRIPT)" ]; then \                                                                                                
 \t\techo "Error: setup.sh not found"; \                                                                                               
 \t\texit 1; \                                                                                                                         
 \tfi                                                                                                                                    
 \t@chmod +x $(SETUP_SCRIPT)                                                                                                             
 \t@$(SETUP_SCRIPT)                                                                                                                      
 \t$(UV) pip install -e ".[dev,docs]"                                                                                                    
                                                                                                                                           
 # Testing                                                                                                                                 
 .PHONY: test                                                                                                                              
 test:                                                                                                                                     
 \t$(PYTEST) $(TESTS_DIR) -v --cov=$(SRC_DIR) --cov-report=html --cov-report=xml                                                         
                                                                                                                                           
 .PHONY: test-card-manager                                                                                                                 
 test-card-manager:                                                                                                                        
 \t$(PYTEST) $(TESTS_DIR)/core/test_card_manager.py -vv                                                                                  
                                                                                                                                           
 .PHONY: test-reading-input                                                                                                                
 test-reading-input:                                                                                                                       
 \t$(PYTEST) $(TESTS_DIR)/core/test_reading_input.py -vv                                                                                 
                                                                                                                                           
 .PHONY: test-golden-dawn                                                                                                                  
 test-golden-dawn:                                                                                                                         
 \t$(PYTEST) $(TESTS_DIR)/extensions/test_golden_dawn.py -vv                                                                             
                                                                                                                                           
 # Code quality                                                                                                                            
 .PHONY: format                                                                                                                            
 format:                                                                                                                                   
 \t$(BLACK) $(SRC_DIR) $(TESTS_DIR)                                                                                                      
                                                                                                                                           
 .PHONY: lint                                                                                                                              
 lint:                                                                                                                                     
 \t$(MYPY) $(SRC_DIR) $(TESTS_DIR)                                                                                                       
 \t$(RUFF) check $(SRC_DIR) $(TESTS_DIR)                                                                                                 
                                                                                                                                           
 # Data processing                                                                                                                         
 .PHONY: process-data                                                                                                                      
 process-data:                                                                                                                             
 \t$(PYTHON) scripts/processing/process_golden_dawn.py                                                                                   
 \t$(PYTHON) scripts/processing/generate_card_data.py                                                                                    
                                                                                                                                           
 # Documentation                                                                                                                           
 .PHONY: docs                                                                                                                              
 docs:                                                                                                                                     
 \tmkdocs build                                                                                                                          
                                                                                                                                           
 .PHONY: serve-docs                                                                                                                        
 serve-docs:                                                                                                                               
 \tmkdocs serve                                                                                                                          
                                                                                                                                           
 # Development helpers                                                                                                                     
 .PHONY: update-deps                                                                                                                       
 update-deps:                                                                                                                              
 \t$(UV) pip compile --upgrade                                                                                                           
 \t$(UV) pip sync                                                                                                                        
                                                                                                                                           
 .PHONY: validate                                                                                                                          
 validate:                                                                                                                                 
 \t$(PYTHON) scripts/processing/validate_card_schema.py                                                                                  
                                                                                                                                           
 # Help                                                                                                                                    
 .PHONY: help                                                                                                                              
 help:                                                                                                                                     
 \t@echo "🎴 $(PROJECT_NAME) Makefile commands:"                                                                                         
 \t@echo "make bootstrap    - First-time project setup"                                                                                  
 \t@echo "make clean       - Clean project files and caches"                                                                             
 \t@echo "make install     - Install project dependencies"                                                                               
 \t@echo "make test        - Run all tests with coverage"                                                                                
 \t@echo "make format      - Format code with black"                                                                                     
 \t@echo "make lint        - Run type checking and linting"                                                                              
 \t@echo "make process-data- Process Golden Dawn and card data"                                                                          
 \t@echo "make docs        - Build documentation"                                                                                        
 \t@echo "make update-deps - Update dependencies using uv" 
