"""Validates TarotAI project structure."""
import os
from pathlib import Path

def validate_structure() -> bool:
    """Validate core project structure."""
    required_dirs = [
        "src/tarotai",
        "src/tarotai/core",
        "src/tarotai/ai",
        "src/tarotai/ui",
        "tests",
        "scripts/dev",
        "docs",
    ]
    
    required_files = [
        "setup.sh",
        "Makefile",
        "README.md",
        "pyproject.toml",
        ".env",
        "assistant_config.yml",
    ]
    
    project_root = Path(__file__).resolve().parent.parent
    
    # Check directories
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if not full_path.is_dir():
            print(f"❌ Missing directory: {dir_path}")
            return False
            
    # Check files
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.is_file():
            print(f"❌ Missing file: {file_path}")
            return False
            
    print("✅ Project structure validation passed!")
    return True

if __name__ == "__main__":
    success = validate_structure()
    exit(0 if success else 1)