#!/usr/bin/env python3
"""
Project Cleanup Script
Maintains project structure and standards according to SSOT.md
"""

import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Set

class ProjectCleaner:
    """Maintains project structure and standards"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.allowed_extensions = {'.py', '.md', '.json', '.txt', '.yml', '.yaml'}
        self.max_file_size = 1024 * 1024  # 1MB
        self.required_dirs = {
            'src/tarotai',
            'tests',
            'scripts',
            'docs/architecture',
            'data'
        }
        
    def clean_project(self, verbose: bool = True) -> None:
        """Execute all cleanup operations"""
        self.remove_junk_files(verbose)
        self.enforce_directory_structure(verbose)
        self.validate_file_extensions(verbose)
        self.check_file_sizes(verbose)
        self.clean_pycache(verbose)
        self.remove_empty_dirs(verbose)
        
    def remove_junk_files(self, verbose: bool = True) -> None:
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
                        if verbose:
                            print(f"Removed junk file: {junk_file}")
                except Exception as e:
                    print(f"Error removing {junk_file}: {e}")

    def enforce_directory_structure(self, verbose: bool = True) -> None:
        """Ensure required directories exist"""
        for required_dir in self.required_dirs:
            dir_path = self.project_root / required_dir
            dir_path.mkdir(parents=True, exist_ok=True)
            if verbose:
                print(f"Ensured directory exists: {dir_path}")

    def validate_file_extensions(self, verbose: bool = True) -> None:
        """Check for disallowed file extensions"""
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.suffix not in self.allowed_extensions:
                if verbose:
                    print(f"Warning: Disallowed file extension: {file_path}")

    def check_file_sizes(self, verbose: bool = True) -> None:
        """Warn about large files"""
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and file_path.stat().st_size > self.max_file_size:
                if verbose:
                    print(f"Warning: Large file detected: {file_path} ({file_path.stat().st_size} bytes)")

    def clean_pycache(self, verbose: bool = True) -> None:
        """Remove all __pycache__ directories"""
        for pycache_dir in self.project_root.rglob('__pycache__'):
            try:
                shutil.rmtree(pycache_dir)
                if verbose:
                    print(f"Removed pycache: {pycache_dir}")
            except Exception as e:
                print(f"Error removing {pycache_dir}: {e}")

    def remove_empty_dirs(self, verbose: bool = True) -> None:
        """Remove empty directories"""
        for dir_path in sorted(self.project_root.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                    if verbose:
                        print(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    print(f"Error removing {dir_path}: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Clean up project files and directories")
    parser.add_argument('--verbose', action='store_true', help="Show detailed output")
    parser.add_argument('--quiet', action='store_true', help="Suppress all output")
    args = parser.parse_args()
    
    cleaner = ProjectCleaner()
    try:
        cleaner.clean_project(verbose=args.verbose and not args.quiet)
        if not args.quiet:
            print("Cleanup complete!")
    except Exception as e:
        print(f"Error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
