.PHONY: setup test lint format clean signature config docs typecheck check

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

define QUANTUM_PROGRESS
@echo "╔══════════════════════════════════════════════════════════════╗"
@echo "║ ┌──────────────────────────────────────────────────────────┐ ║"
@echo "║ │                ⚛ QUANTUM STATE IN PROGRESS ⚛            │ ║"
@echo "║ └──────────────────────────────────────────────────────────┘ ║"
@echo "║                                                              ║"
@echo "║    ▓▒░ Wavefunction Collapsing... ░▒▓                       ║"
@echo "║         Please hold while we entangle your code              ║"
@echo "║                                                              ║"
@echo "╚══════════════════════════════════════════════════════════════╝"
endef

define QUANTUM_SHUTDOWN
@echo "╔══════════════════════════════════════════════════════════════╗"
@echo "║ ┌──────────────────────────────────────────────────────────┐ ║"
@echo "║ │                ⚛ QUANTUM REALM SHUTDOWN ⚛               │ ║"
@echo "║ └──────────────────────────────────────────────────────────┘ ║"
@echo "║                                                              ║"
@echo "║    ▓▒░ Wavefunction Collapsed ░▒▓                           ║"
@echo "║         Entanglement Disrupted                               ║"
@echo "║         Schrödinger's Cat: Safe                              ║"
@echo "║                                                              ║"
@echo "╚══════════════════════════════════════════════════════════════╝"
endef

signature:
	$(QUANTUM_SIGNATURE)

setup:
	@echo "Setting up development environment..."
	@./setup.sh
	$(QUANTUM_SIGNATURE)

test:
	@echo "Running tests..."
	@pytest tests/ \
		--cov=tarotai \
		--cov-report=term-missing
	$(QUANTUM_SUCCESS)

lint:
	@echo "Running linting..."
	@flake8 src/ tests/ \
		--max-line-length=79
	@mypy src/ tests/
	$(QUANTUM_PROGRESS)

format:
	@echo "Formatting code..."
	@black src/ tests/
	$(QUANTUM_SUCCESS)

clean:
	@echo "Cleaning up..."
	@rm -rf .venv/ __pycache__/ .pytest_cache/ .mypy_cache/
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '__pycache__' -delete
	$(QUANTUM_SHUTDOWN)

config:
	@echo "Validating configuration..."
	@python -c "from tarotai.config.schemas.config import get_config; get_config()"
	$(QUANTUM_SUCCESS)

docs:
	@echo "Generating documentation..."
	@pdoc --html --output-dir docs src/tarotai
	$(QUANTUM_SUCCESS)

typecheck:
	@echo "Running type checking..."
	@mypy src/ tests/
	$(QUANTUM_SUCCESS)

validate-cards:
	@echo "Validating card data structure..."
	@python -c "from tarotai.core.models.card import CardManager; CardManager()._load_cards()"
	$(QUANTUM_SUCCESS)

check: lint typecheck test validate-cards
	@echo "All checks passed!"
	$(QUANTUM_SUCCESS)
