# Contributing to TarotAI

Version 2.1.0

## Development Workflow

### Setup
```bash
pip install -r requirements.txt && \
pip install -e ".[dev]" && \
pip install types-pydantic types-httpx types-python-dotenv types-requests
```

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/ tests/
```

### Type Checking
```bash
mypy src/ tests/
```

## Documentation Contributions

When contributing to documentation:
- Update all relevant files (SSOT.md, README.md)
- Keep documentation in sync with code
- Use consistent terminology
- Follow Markdown style guide
- Include examples where applicable

For community standards, see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
