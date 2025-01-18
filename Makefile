# TarotAI Makefile
# Manages development workflows and quality checks

SHELL := /bin/bash
PYTHON := python3
VENV := .venv
QUANTUM_SUCCESS := @echo "✨ Success!"
QUANTUM_SIGNATURE := @echo "🎴 TarotAI"

.PHONY: all install clean test coverage lint format check validate migrate docs serve-docs

# Default target
all: check

# Install dependencies
install:
	@echo "Installing dependencies..."
	@./setup.sh
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
	@python scripts/validate_cards.py
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

# Run import migration
migrate:
	@echo "Running import migration..."
	@python scripts/dev/import_migration.py
	$(QUANTUM_SUCCESS)

# Run all checks
check: lint test migrate
	$(QUANTUM_SUCCESS)

# Validate project structure
validate:
	@echo "Validating project structure..."
	@python scripts/validate_structure.py
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


validate-cards:
	@echo "Validating card data..."
	@python scripts/processing/validate_card_schema.py
	$(QUANTUM_SUCCESS)

# Generate card data
generate-cards:
	@echo "Generating card data..."
	@python scripts/processing/generate_card_data.py
	$(QUANTUM_SUCCESS)

# Update embeddings
update-embeddings:
	@echo "Updating card embeddings..."
	@python scripts/processing/update_embeddings.py
	$(QUANTUM_SUCCESS)

# Process Golden Dawn PDF
process-golden-dawn:
	@echo "Processing Golden Dawn PDF..."
	@python scripts/processing/process_golden_dawn.py
	$(QUANTUM_SUCCESS)

# Full data processing pipeline
process-data: validate-cards generate-cards update-embeddings process-golden-dawn
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
	@echo "  migrate           - Run import migration"
	@echo "  check             - Run all checks"
	@echo "  validate          - Validate project structure"
	@echo "  docs              - Generate documentation"
	@echo "  serve-docs        - Serve documentation locally"
	@echo "  validate-cards    - Validate card data"
	@echo "  generate-cards    - Generate card data"
	@echo "  update-embeddings - Update card embeddings"
	@echo "  process-golden-dawn - Process Golden Dawn PDF"
	@echo "  process-data      - Run full data processing pipeline"
	@echo "  help              - Show this help message"
	$(QUANTUM_SIGNATURE)
