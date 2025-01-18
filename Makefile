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

# Help target
help:
	@echo "TarotAI Makefile targets:"
	@echo "  install     - Install project dependencies"
	@echo "  test        - Run test suite"
	@echo "  coverage    - Generate test coverage report"
	@echo "  lint        - Run code quality checks"
	@echo "  format      - Format code"
	@echo "  clean       - Clean build artifacts"
	@echo "  migrate     - Run import migration"
	@echo "  check       - Run all checks"
	@echo "  validate    - Validate project structure"
	@echo "  docs        - Generate documentation"
	@echo "  serve-docs  - Serve documentation locally"
	@echo "  help        - Show this help message"
	$(QUANTUM_SIGNATURE)