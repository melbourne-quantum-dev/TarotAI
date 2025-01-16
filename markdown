# TarotAI

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

TarotAI is a neural-enhanced tarot reading system that combines traditional divination with modern AI-powered insights. It provides programmatic access to tarot readings through a CLI interface and offers advanced features like:

- AI-enhanced card interpretations
- Multiple spread types
- Context-aware interpretation engine
- Reading history and pattern analysis
- Voice interface support

## Features

- 🃏 Traditional tarot deck implementation
- 🤖 AI-powered card meaning enrichment
- 🎙️ Voice interface for hands-free readings
- 📊 Reading history tracking and analysis
- 🧠 Semantic search using embeddings
- 🎨 Rich terminal interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/melbourne-quantum-dev/tarotai.git
   cd tarotai
   ```

2. Set up the environment:
   ```bash
   make install
   source .venv/bin/activate
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Run the CLI:
   ```bash
   tarotai --help
   ```

## Usage

### Command Line Interface
```bash
# Perform a reading
tarotai read --spread-type three_card --focus "Career" --question "What should I focus on?"

# Interactive mode
tarotai interactive

# Voice interface
tarotai voice
```

### Python API
```python
from tarotai import TarotReader

reader = TarotReader()
reading = reader.execute_reading(
    spread_type="three_card",
    focus="Relationships",
    question="What should I know about my current relationship?"
)
```

## Development

### Setup
```bash
make install
make activate
```

### Running Tests
```bash
make test
```

### Code Formatting
```bash
black src/ tests/
```

### Type Checking
```bash
mypy src/ tests/
```

## Contributing

We welcome contributions! Please see our [Contribution Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the Golden Dawn tradition
- Built with modern Python tools
- Powered by AI technologies
