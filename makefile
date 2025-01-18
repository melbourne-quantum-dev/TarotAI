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
