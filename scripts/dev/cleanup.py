#!/usr/bin/env python3
"""
Project Cleanup Script
Maintains project structure and standards according to SSOT.md
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Optional, Set

class ProjectCleaner:
    """Maintains project structure and standards"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.allowed_extensions = {'.py', '.md', '.json', '.txt', '.yml', '.yaml'}
        self.max_file_size = 1024 * 1024  # 1MB
        self.required_dirs = {
            'src/tarotai',
            'tests',
            'scripts',
            'docs/architecture',
            'data'
        }
        
    def clean_project(self) -> None:
        """Execute all cleanup operations"""
        self.remove_junk_files()
        self.enforce_directory_structure()
        self.validate_file_extensions()
        self.check_file_sizes()
        self.clean_pycache()
        self.remove_empty_dirs()
        
    def remove_junk_files(self) -> None:
        """Remove common junk files"""
        junk_patterns = [
            '*.log', '*.bak', '*.tmp', '*.swp', '*.DS_Store',
            '*.pyc', '*.pyo', '*.pyd', '*.py.class', '*.ipynb_checkpoints'
        ]
        
        for pattern in junk_patterns:
            for junk_file in self.project_root.rglob(pattern):
                try:
                    if junk_file.is_file():
                        junk_file.unlink()
                        print(f"Removed junk file: {junk_file}")
                except Exception as e:
                    print(f"Error removing {junk_file}: {e}")

    def enforce_directory_structure(self) -> None:
        """Ensure required directories exist"""
        for required_dir in self.required_dirs:
            dir_path = self.project_root / required_dir
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Ensured directory exists: {dir_path}")

    def validate_file_extensions(self) -> None:
        """Check for disallowed file extensions"""
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.suffix not in self.allowed_extensions:
                print(f"Warning: Disallowed file extension: {file_path}")

    def check_file_sizes(self) -> None:
        """Warn about large files"""
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.stat().st_size > self.max_file_size:
                print(f"Warning: Large file detected: {file_path} ({file_path.stat().st_size} bytes)")

    def clean_pycache(self) -> None:
        """Remove all __pycache__ directories"""
        for pycache_dir in self.project_root.rglob('__pycache__'):
            try:
                shutil.rmtree(pycache_dir)
                print(f"Removed pycache: {pycache_dir}")
            except Exception as e:
                print(f"Error removing {pycache_dir}: {e}")

    def remove_empty_dirs(self) -> None:
        """Remove empty directories"""
        for dir_path in sorted(self.project_root.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                    print(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    print(f"Error removing {dir_path}: {e}")

def main():
    cleaner = ProjectCleaner()
    cleaner.clean_project()
    print("Cleanup complete!")

if __name__ == "__main__":
    main()
