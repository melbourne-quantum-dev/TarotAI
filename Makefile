# Makefile for TarotAI project setup

.PHONY: install test clean

install:
	@echo "Setting up virtual environment and installing dependencies..."
	uv venv .venv
	. .venv/bin/activate && uv pip install -r requirements.txt
	@echo "\nSetup complete! Run 'make activate' to start working."

activate:
	@echo "Activating virtual environment..."
	@bash -c "source .venv/bin/activate && exec bash"

test:
	@echo "Running tests..."
	. .venv/bin/activate && pytest tests/

clean:
	@echo "Cleaning up..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .mypy_cache
	@echo "Clean complete!"

help:
	@echo "Available commands:"
	@echo "  make install    - Set up virtual environment and install dependencies"
	@echo "  make activate   - Activate virtual environment"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean up project files"
	@echo "  make help       - Show this help message"
