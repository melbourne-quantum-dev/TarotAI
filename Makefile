.PHONY: setup test lint format clean

setup:
	@echo "Setting up development environment..."
	@./setup.sh

test:
	@echo "Running tests..."
	@uv run pytest tests/ --cov=tarotai --cov-report=term-missing

lint:
	@echo "Running linting..."
	@uv run flake8 src/ tests/
	@uv run mypy src/ tests/

format:
	@echo "Formatting code..."
	@uv run black src/ tests/

clean:
	@echo "Cleaning up..."
	@rm -rf .venv/ __pycache__/ .pytest_cache/ .mypy_cache/
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '__pycache__' -delete
