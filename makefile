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
VERIFY_SCRIPT := $(shell pwd)/verify_project_structure.py

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

# Data processing targets
.PHONY: process-data
process-data: 
	$(UV) run python $(shell pwd)/scripts/processing/process_golden_dawn.py
	$(UV) run python $(shell pwd)/scripts/processing/generate_meanings.py

# Display targets
.PHONY: display-cards
display-cards:
	@echo "🎴 Displaying cards..."
	$(PYTHON) src/tarotai/cli.py display-cards

.PHONY: display-reading
display-reading:
	@echo "🎴 Displaying sample reading..."
	$(PYTHON) src/tarotai/cli.py display-reading

.PHONY: display-status
display-status:
	@echo "🎴 Displaying system status..."
	$(PYTHON) src/tarotai/cli.py status

.PHONY: process-golden-dawn
process-golden-dawn:
	@echo "🎴 Processing Golden Dawn PDF..."
	$(PYTHON) scripts/processing/process_golden_dawn.py

.PHONY: generate-meanings
generate-meanings:
	@echo "🎴 Generating card meanings..."
	$(UV) run python $(shell pwd)/scripts/processing/generate_meanings.py

.PHONY: generate-base-deck
generate-base-deck:
	@echo "🎴 Generating base deck structure..."
	$(PYTHON) scripts/processing/generate_meanings.py --base-deck

# Testing targets
.PHONY: verify-structure
verify-structure:
	@echo "🔍 Verifying project structure..."
	$(PYTHON) $(VERIFY_SCRIPT)
	@echo "✓ Project structure verified"

.PHONY: test
test: verify-structure
	@echo "🧪 Running tests..."
	$(PYTEST) $(TESTS_DIR) -v

.PHONY: test-card-manager
test-card-manager:
	$(PYTEST) $(TESTS_DIR)/core/test_card_manager.py -v

# Code quality targets
.PHONY: lint
lint:
	$(BLACK) $(SRC_DIR) $(TESTS_DIR) --check
	$(RUFF) check $(SRC_DIR) $(TESTS_DIR)
	$(MYPY) $(SRC_DIR)

.PHONY: format
format:
	$(BLACK) $(SRC_DIR) $(TESTS_DIR)
	$(RUFF) check $(SRC_DIR) $(TESTS_DIR) --fix

# Documentation targets
.PHONY: docs
docs:
	$(MAKE) -C $(DOCS_DIR) html

.PHONY: clean-docs
clean-docs:
	$(MAKE) -C $(DOCS_DIR) clean

# Utility targets
.PHONY: clean
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: help
help:
	@echo "🎴 TarotAI Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make bootstrap    - Initialize development environment"
	@echo "  make install      - Install project dependencies"
	@echo "  make clean        - Remove virtual environment and cache files"
	@echo ""
	@echo "Development:"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code using black and ruff"
	@echo "  make test         - Run all tests"
	@echo "  make test-card-manager - Run card manager tests only"
	@echo ""
	@echo "Data Processing:"
	@echo "  make process-data - Process Golden Dawn text and generate embeddings"
	@echo ""
	@echo "Display:"
	@echo "  make display-cards    - Show all cards with meanings"
	@echo "  make display-reading  - Show a sample reading"
	@echo "  make display-status   - Show system status"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         - Build documentation"
	@echo "  make clean-docs   - Clean documentation build"
	@echo ""
	@echo "Verification:"
	@echo "  make verify-structure - Check project structure against SSOT"

.DEFAULT_GOAL := help
