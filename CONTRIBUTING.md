# Contributing to TarotAI

Thank you for your interest in contributing to TarotAI! We welcome contributions from everyone.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .[dev]
   ```
4. Create a new branch for your changes
5. Make your changes
6. Run tests and linting:
   ```bash
   pytest tests/
   flake8 src/ tests/
   mypy src/ tests/
   black src/ tests/
   ```
7. Commit your changes with a descriptive message
8. Push your branch to your fork
9. Open a pull request

## Code Style

- Follow PEP 8 style guide
- Use type hints for all public functions
- Document all public interfaces
- Keep lines under 88 characters
- Use black for code formatting
- Use flake8 for linting

## Testing

- Write tests for new features
- Maintain 100% test coverage
- Use pytest for testing
- Use pytest-asyncio for async tests
- Use pytest-cov for coverage reporting

## Pull Requests

- Keep PRs focused on a single feature/bugfix
- Include tests for new features
- Update documentation if needed
- Describe your changes in the PR description
- Reference any related issues

## Reporting Issues

When reporting issues, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc)
- Any relevant logs or screenshots

## Code of Conduct

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
