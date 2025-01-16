
# Install project dependencies
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install -e .

# Generate card meanings using AI
source .venv/bin/activate
uv run python scripts/generate_meanings.py

# Process Golden Dawn PDF
source .venv/bin/activate
uv run python src/tarotai/extensions/enrichment/enricher.py

# Clean up temporary files and caches
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache
rm -rf .mypy_cache

# Format code and run linting
source .venv/bin/activate
uv run black src/ tests/
uv run flake8 src/ tests/
uv run mypy src/ tests/
