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
	@if [ ! -d ".venv" ]; then \
		uv venv .venv; \
	fi
	@source .venv/bin/activate && \
	 export UV_INDEX_URL="https://pypi.org/simple" && \
	 export UV_CACHE_DIR=".uv_cache" && \
	 export UV_PIP_VERSION=">=23.3.2" && \
	 ./setup.sh
	$(QUANTUM_SUCCESS)

# Verify dependency integrity
verify-deps:
	@echo "Verifying dependency integrity..."
	@uv pip check || { \
		echo "❌ Dependency verification failed!"; \
		exit 1; \
	}
	$(QUANTUM_SUCCESS)

# Run tests
test:
	@echo "Running tests..."
	@pytest tests/ \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html \
		-v
	$(QUANTUM_SUCCESS)

# Generate coverage report
coverage:
	@echo "Generating coverage report..."
	@coverage report
	@coverage html
	$(QUANTUM_SUCCESS)

# Run code quality checks
lint:
	@echo "Running code quality checks..."
	@flake8 src/ tests/ \
		--max-line-length=79
	@mypy src/ tests/
	@python scripts/processing/validate_card_schema.py
	$(QUANTUM_SUCCESS)

# Format code
format:
	@echo "Formatting code..."
	@black src/ tests/
	$(QUANTUM_SUCCESS)

# Clean build artifacts
clean:
	@echo "Running project cleanup..."
	@python scripts/dev/cleanup.py --verbose
	$(QUANTUM_SIGNATURE)

# Run all checks
check: lint test
	$(QUANTUM_SUCCESS)

# Validate project structure and card data
validate:
	@echo "Validating project structure and card data..."
	@python scripts/processing/validate_card_schema.py
	$(QUANTUM_SUCCESS)

# Generate documentation
docs:
	@echo "Generating documentation..."
	@cd docs && make html
	$(QUANTUM_SUCCESS)

# Serve documentation locally
serve-docs:
	@echo "Serving documentation..."
	@cd docs/_build/html && python -m http.server 8000
	$(QUANTUM_SUCCESS)

# Validate card data
validate-cards:
	@echo "Validating card data..."
	@if ! python scripts/processing/validate_card_schema.py; then \
		echo "❌ Card validation failed!"; \
		exit 1; \
	fi
	$(QUANTUM_SUCCESS)

# Generate card data
generate-cards:
	@echo "Generating card data..."
	@if ! python scripts/processing/generate_card_data.py; then \
		echo "❌ Card generation failed!"; \
		exit 1; \
	fi
	$(QUANTUM_SUCCESS)

# Update embeddings
update-embeddings:
	@echo "Updating card embeddings..."
	@if ! python scripts/processing/update_embeddings.py; then \
		echo "❌ Embedding update failed!"; \
		exit 1; \
	fi
	$(QUANTUM_SUCCESS)

# Process Golden Dawn PDF
process-golden-dawn:
	@echo "Processing Golden Dawn PDF..."
	@if ! python scripts/processing/process_golden_dawn.py; then \
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
	@echo "✅ Data processing pipeline completed successfully!"
	$(QUANTUM_SIGNATURE)

# Help target
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
