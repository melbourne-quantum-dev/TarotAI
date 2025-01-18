.PHONY: all setup test lint format clean docs validate check update

define QUANTUM_SIGNATURE
@echo "╔══════════════════════════════════════════════════════════════╗"
@echo "║ ┌──────────────────────────────────────────────────────────┐ ║"
@echo "║ │                ⚛ DR. ZHOU'S QUANTUM REALM ⚛             │ ║"
@echo "║ └──────────────────────────────────────────────────────────┘ ║"
@echo "║                                                              ║"
@echo "║    ▓▒░ Quantum Computing Enthusiast ░▒▓                     ║"
@echo "║         Faraday Cage Certified                               ║"
@echo "║         Typing Speed: 0.99c                                  ║"
@echo "║                                                              ║"
@echo "╚══════════════════════════════════════════════════════════════╝"
endef

define QUANTUM_SUCCESS
@echo "╔══════════════════════════════════════════════════════════════╗"
@echo "║ ┌──────────────────────────────────────────────────────────┐ ║"
@echo "║ │                ⚡ QUANTUM STATE ACHIEVED ⚡               │ ║"
@echo "║ └──────────────────────────────────────────────────────────┘ ║"
@echo "║                                                              ║"
@echo "║    ▓▒░ Wavefunction Successfully Collapsed ░▒▓              ║"
@echo "║         Entanglement Verified                               ║"
@echo "║                                                              ║"
@echo "╚══════════════════════════════════════════════════════════════╝"
endef

# Default target
all: check

# Setup environment
setup:
	@echo "Setting up development environment..."
	@./setup.sh
	$(QUANTUM_SIGNATURE)

# Run tests with coverage
test:
	@echo "Running tests..."
	@pytest tests/ \
		--cov=tarotai \
		--cov-report=term-missing
	$(QUANTUM_SUCCESS)

# Run all code quality checks
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
	@echo "Cleaning up..."
	@rm -rf .venv/ __pycache__/ .pytest_cache/ .mypy_cache/ .uv_cache/
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '__pycache__' -delete
	$(QUANTUM_SIGNATURE)

# Generate documentation
docs:
	@echo "Generating documentation..."
	@pdoc --html --output-dir docs src/tarotai
	$(QUANTUM_SUCCESS)

# Validate configuration and data
validate:
	@echo "Validating configuration..."
	@python -c "from tarotai.config.schemas.config import get_config; get_config()"
	@echo "Validating card data..."
	@python scripts/validate_cards.py
	$(QUANTUM_SUCCESS)

# Run all checks (test + lint + validate)
check: test lint validate
	@echo "All checks passed!"
	$(QUANTUM_SUCCESS)

# Update dependencies
update:
	@echo "Updating dependencies..."
	@uv pip compile --upgrade
	@uv pip sync
	$(QUANTUM_SUCCESS)
