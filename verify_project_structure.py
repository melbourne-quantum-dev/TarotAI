# Add this to verify_project_structure.py
#!/usr/bin/env python3
"""Verify project structure and identify stray files."""

from pathlib import Path
import sys
from typing import Set, Dict
import argparse

ALLOWED_ROOT_DIRS = {
    'src',
    'tests',
    'docs',
    'scripts',
    '.git',
    '.github',
    '.pytest_cache',
    '__pycache__',
    'venv',
    '.venv',
    'build',
    'dist',
    '.idea',
    '.vscode',
    '.cache',           # Coverage cache
    '.backups',         # Backup directory
    'data',            # Data directory
    '.aider.tags.cache.v3',  # Aider cache
    'list'             # Virtual env directory
}

ALLOWED_ROOT_FILES = {
    'README.md',
    'LICENSE',
    'setup.py',
    'pyproject.toml',
    'requirements.txt',
    'requirements-dev.txt',
    '.gitignore',
    '.pre-commit-config.yaml',
    'pytest.ini',
    'tox.ini',
    'assistant_config.yml',
    'MANIFEST.in',
    '.envrc',          # Direnv config
    '.envrc.example',  # Direnv example
    '.env',            # Environment file
    'coverage.xml',    # Coverage report
    '.coverage',       # Coverage data
    'CODE_OF_CONDUCT.md',
    'CONTRIBUTING.md',
    'makefile',
    'setup.sh',
    '.aider.chat.history.md',
    '.aider.input.history',
    'verify_project_structure.py'  # This script
}

def check_project_structure(root_path: Path) -> bool:
    """Check project structure and identify stray items."""
    issues = []
    
    # Check root directory
    for item in root_path.iterdir():
        if item.is_dir():
            if item.name not in ALLOWED_ROOT_DIRS:
                issues.append(f"Unexpected directory in root: {item.name}")
        else:
            if item.name not in ALLOWED_ROOT_FILES:
                issues.append(f"Unexpected file in root: {item.name}")
    
    # Check src directory structure
    src_path = root_path / 'src' / 'tarotai'
    if not src_path.exists():
        issues.append("Missing src/tarotai directory")
    else:
        # Check for Python files outside of src/tarotai
        for py_file in root_path.rglob("*.py"):
            # Ignore specific directories
            if any(x in str(py_file) for x in [
                '/src/', '/tests/', '/scripts/', 
                '/.backups/', '/venv/', '/.venv/',
                '/list/', '/build/', '/dist/'
            ]):
                continue
            issues.append(f"Stray Python file: {py_file.relative_to(root_path)}")
    
    # Verify package structure
    if src_path.exists():
        required_dirs = ['ai', 'core', 'config', 'ui']
        for dir_name in required_dirs:
            if not (src_path / dir_name).exists():
                issues.append(f"Missing required directory in src/tarotai: {dir_name}")
    
    if issues:
        print("❌ Project structure verification failed!")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("✅ Project structure verified!")
    
    # Print current structure
    print("\nCurrent Project Structure:")
    print("==========================")
    for item in sorted(root_path.rglob("*")):
        if item.is_file() and not any(x in str(item) for x in ['__pycache__', '.git', '.pytest_cache', 'venv', '.venv', 'build', 'dist']):
            try:
                rel_path = item.relative_to(root_path)
                print(f"  {rel_path}")
            except ValueError:
                continue
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Verify project structure")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                      help="Project root directory path")
    
    args = parser.parse_args()
    
    if not check_project_structure(args.root):
        sys.exit(1)

if __name__ == "__main__":
    main()