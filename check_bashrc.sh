#!/bin/bash

# Check if direnv is installed
if ! command -v direnv &> /dev/null; then
    echo "❌ Error: direnv is not installed."
    echo "Install it with:"
    echo "  sudo apt install direnv  # On Ubuntu/Debian"
    echo "  brew install direnv      # On macOS"
    exit 1
fi

# Check if direnv is hooked in ~/.bashrc
if ! grep -q 'eval "$(direnv hook bash)"' ~/.bashrc; then
    echo "❌ Error: direnv hook is missing in ~/.bashrc."
    echo "Add this line to your ~/.bashrc:"
    echo '  eval "$(direnv hook bash)"'
    exit 1
fi

# Check if .envrc exists in the project directory
PROJECT_DIR="$(pwd)"
if [ ! -f "$PROJECT_DIR/.envrc" ]; then
    echo "❌ Error: .envrc file is missing in current directory."
    echo "Create it with:"
    echo "  touch .envrc"
    echo "And add the following content:"
    echo '  source .venv/bin/activate'
    echo '  export TAROTAI_DATA_DIR="$(pwd)/data"'
    echo '  export OPENAI_API_KEY="your-key-here"'
    echo '  alias tarotai="python -m tarotai"'
    echo '  alias pytest="python -m pytest"'
    echo '  alias aider="aider"'
    exit 1
fi

# Check if .envrc is allowed
if ! direnv status | grep -q "Allowed"; then
    echo "❌ Error: .envrc is not allowed."
    echo "Run this command to allow it:"
    echo "  direnv allow"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Virtual environment is not activated."
    echo "Ensure your .envrc contains:"
    echo '  source .venv/bin/activate'
    exit 1
fi

# Check if environment variables are set
if [ -z "$TAROTAI_DATA_DIR" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: Environment variables are not set."
    echo "Ensure your .envrc contains:"
    echo '  export TAROTAI_DATA_DIR="$(pwd)/data"'
    echo '  export OPENAI_API_KEY="your-key-here"'
    exit 1
fi

# Check if aliases are set
if ! alias tarotai &> /dev/null || ! alias pytest &> /dev/null || ! alias aider &> /dev/null; then
    echo "❌ Error: Aliases are not set."
    echo "Ensure your .envrc contains:"
    echo '  alias tarotai="python -m tarotai"'
    echo '  alias pytest="python -m pytest"'
    echo '  alias aider="aider"'
    exit 1
fi

# If all checks pass
echo "✅ Your bashrc and direnv setup are correct!"
echo "You can now use:"
echo "  - tarotai"
echo "  - pytest"
echo "  - aider"
echo "  - make test/lint/format"
