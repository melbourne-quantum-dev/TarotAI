# TarotAI Makefile
# Manages development workflows and quality checks

SHELL := /bin/bash
PYTHON := python3
VENV := .venv
QUANTUM_SUCCESS := @echo "✨ Success!"
QUANTUM_SIGNATURE := @echo "🎴 TarotAI"

.PHONY: all install clean test coverage lint format check validate docs serve-docs \
		validate-cards generate-cards update-embeddings process-golden-dawn process-data help

# Default target
all: check

# Install dependencies
install:
	@echo "Installing dependencies with modern resolver..."
	@if [ ! -d "$(VENV)" ]; then \
		uv venv $(VENV); \
	fi
	@source $(VENV)/bin/activate && \
	 export UV_INDEX_URL="https://pypi.org/simple" && \
	 export UV_CACHE_DIR=.cache/.uv_cache && \
	 export UV_PIP_VERSION=">=23.3.2" && \
	 export UV_PYTHON=">=3.12" && \
	 uv pip install -r <(grep -v realtimestt requirements.txt) && \
	 uv pip install -e .[dev] && \
	 uv pip install pytest pytest-cov pytest-asyncio

# Run test suite
test:
	@echo "Running test suite..."
	@source $(VENV)/bin/activate && pytest tests/ -v
	$(QUANTUM_SUCCESS)

# Run card manager tests
test-card-manager:
	@echo "Running card manager tests..."
	@source $(VENV)/bin/activate && pytest tests/core/test_card_manager.py -v
	$(QUANTUM_SUCCESS)

# Run reading input tests
test-reading-input:
	@echo "Running reading input tests..."
	@source $(VENV)/bin/activate && pytest tests/core/test_reading_input.py -v
	$(QUANTUM_SUCCESS)

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	@source $(VENV)/bin/activate && pytest tests/integration/ -v
	$(QUANTUM_SUCCESS)

# Run golden dawn specific tests
test-golden-dawn:
	@echo "Running Golden Dawn tests..."
	@source $(VENV)/bin/activate && \
	pytest tests/test_golden_dawn.py -v && \
	pytest tests/test_process_golden_dawn.py -v
	$(QUANTUM_SUCCESS)

# Generate test coverage report
coverage:
	@echo "Generating test coverage report..."
	@source $(VENV)/bin/activate && pytest tests/ --cov=src/ --cov-report=html
	$(QUANTUM_SUCCESS)

# Run code quality checks
lint:
	@echo "Running code quality checks..."
	@source $(VENV)/bin/activate && \
	flake8 src/ tests/ && \
	mypy src/ tests/
	$(QUANTUM_SUCCESS)

# Format code
format:
	@echo "Formatting code..."
	@source $(VENV)/bin/activate && black src/ tests/
	$(QUANTUM_SUCCESS)

# Clean build artifacts
clean:
	@echo "Running project cleanup..."
	@echo "Project root: $(shell pwd)"
	@rm -rf $(VENV)
	@rm -rf .cache
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	$(QUANTUM_SIGNATURE)

# Run all checks
check: lint test
	$(QUANTUM_SUCCESS)

# Validate project structure and card data
validate:
	@echo "Validating project structure and card data..."
	@source $(VENV)/bin/activate && $(PYTHON) scripts/processing/validate_card_schema.py
	$(QUANTUM_SUCCESS)

# Generate documentation
docs:
	@echo "Generating documentation..."
	@source $(VENV)/bin/activate && cd docs && make html
	$(QUANTUM_SUCCESS)

# Serve documentation locally
serve-docs:
	@echo "Serving documentation at http://localhost:8000..."
	@cd docs/_build/html && python3 -m http.server 8000

# Validate card data
validate-cards:
	@echo "Validating card data..."
	@source $(VENV)/bin/activate && $(PYTHON) scripts/processing/validate_card_schema.py
	$(QUANTUM_SUCCESS)

# Generate card data
generate-cards:
	@echo "Generating card data..."
	@if [ ! -f "scripts/processing/generate_card_data.py" ]; then \
		echo "❌ Error: generate_card_data.py not found!"; \
		exit 1; \
	fi
	@source $(VENV)/bin/activate && $(PYTHON) scripts/processing/generate_card_data.py
	$(QUANTUM_SUCCESS)

# Update card embeddings
update-embeddings:
	@echo "Updating card embeddings..."
	@source $(VENV)/bin/activate && $(PYTHON) scripts/processing/update_embeddings.py
	$(QUANTUM_SUCCESS)

# Process Golden Dawn PDF
process-golden-dawn:
	@echo "Processing Golden Dawn PDF..."
	@source $(VENV)/bin/activate && \
	if ! $(PYTHON) scripts/processing/process_golden_dawn.py; then \
		echo "❌ Golden Dawn processing failed!"; \
		exit 1; \
	fi
	$(QUANTUM_SUCCESS)

# Full data processing pipeline
process-data:
	@echo "Starting data processing pipeline..."
	@if ! make validate-cards; then \
		echo "❌ Pipeline failed at validation step"; \
		exit 1; \
	fi
	@if ! make generate-cards; then \
		echo "❌ Pipeline failed at card generation step"; \
		exit 1; \
	fi
	@if ! make update-embeddings; then \
		echo "❌ Pipeline failed at embedding update step"; \
		exit 1; \
	fi
	@if ! make process-golden-dawn; then \
		echo "❌ Pipeline failed at Golden Dawn processing step"; \
		exit 1; \
	fi
	$(QUANTUM_SUCCESS)

# Show help
help:
	@echo "TarotAI Makefile targets:"
	@echo "  install           - Install project dependencies"
	@echo "  test              - Run test suite"
	@echo "  coverage          - Generate test coverage report"
	@echo "  lint              - Run code quality checks"
	@echo "  format            - Format code"
	@echo "  clean             - Clean build artifacts"
	@echo "  check             - Run all checks"
	@echo "  validate          - Validate project structure and card data"
	@echo "  docs              - Generate documentation"
	@echo "  serve-docs        - Serve documentation locally"
	@echo "  validate-cards    - Validate card data"
	@echo "  generate-cards    - Generate card data"
	@echo "  update-embeddings - Update card embeddings"
	@echo "  process-golden-dawn - Process Golden Dawn PDF"
	@echo "  process-data      - Run full data processing pipeline"
	@echo "  help              - Show this help message"
	$(QUANTUM_SIGNATURE)
