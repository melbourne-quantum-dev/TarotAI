#!/usr/bin/env python3
"""
TarotAI Project Structure Maintenance
Handles cleanup and structural organization
"""

import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Set, Dict
from dataclasses import dataclass

@dataclass
class FileRelocation:
    source: str
    target: str
    description: str

@dataclass
class ProjectStructure:
    """Project structure configuration"""
    protected_files: Set[str]
    protected_dirs: Set[str]
    relocations: List[FileRelocation]
    cache_dirs: Set[str]
    
    @classmethod
    def create_default(cls) -> 'ProjectStructure':
        return cls(
            protected_files={
                'setup.sh', 'Makefile', 'README.md', 'CONTRIBUTING.md', 
                'requirements.txt', '.gitignore', 'pyproject.toml',
                'assistant_config.yml', '.env', '.envrc', 'dev-requirements.txt',
                'pytest.ini', 'mypy.ini', 'setup.py', 'uv.lock',
                'CODE_OF_CONDUCT.md'
            },
            protected_dirs={
                'src/tarotai',
                'tests',
                'scripts',
                'docs/architecture',
                'data',
                '.git',
                '.cache'
            },
            relocations=[
                FileRelocation(
                    'errors.py',
                    'src/tarotai/core/errors/base.py',
                    'Core errors module'
                ),
                FileRelocation(
                    'signatures.py',
                    'src/tarotai/core/utils/signatures.py',
                    'Signature utilities'
                ),
                FileRelocation(
                    'check_bashrc.sh',
                    'scripts/dev/check_bashrc.sh',
                    'Development utilities'
                )
            ],
            cache_dirs={
                'knowledge_cache',
                '__pycache__',
                '.pytest_cache',
                '.mypy_cache',
                '.ruff_cache',
                '.uv_cache'
            }
        )

class ProjectCleaner:
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).resolve().parent.parent.parent
        self.structure = ProjectStructure.create_default()
        
    def clean(self, dry_run: bool = False, verbose: bool = True) -> None:
        """Execute cleanup and structural organization"""
        if verbose:
            print(f"Project root: {self.project_root}")
            if dry_run:
                print("DRY RUN - no files will be modified")
        
        self._relocate_files(dry_run, verbose)
        self._organize_caches(dry_run, verbose)
        self._fix_malformed_names(dry_run, verbose)
        self._enforce_structure(dry_run, verbose)
    
    def _relocate_files(self, dry_run: bool, verbose: bool) -> None:
        """Handle file relocations"""
        for relocation in self.structure.relocations:
            source = self.project_root / relocation.source
            target = self.project_root / relocation.target
            
            if source.exists():
                if verbose:
                    action = "Would move" if dry_run else "Moving"
                    print(f"{action}: {relocation.source} → {relocation.target}")
                    print(f"  Reason: {relocation.description}")
                
                if not dry_run:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(target))
    
    def _organize_caches(self, dry_run: bool, verbose: bool) -> None:
        """Organize cache directories"""
        cache_root = self.project_root / '.cache'
        
        for cache_dir in self.structure.cache_dirs:
            # Look for cache directories recursively
            for path in self.project_root.rglob(cache_dir):
                if path.is_dir() and self._should_move_cache(path):
                    target = cache_root / path.relative_to(self.project_root)
                    if verbose:
                        action = "Would organize" if dry_run else "Organizing"
                        print(f"{action} cache: {path} → {target}")
                    
                    if not dry_run:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(path), str(target))
    
    def _fix_malformed_names(self, dry_run: bool, verbose: bool) -> None:
        """Fix malformed file and directory names"""
        patterns = {
            r'\*\*.*\*\*': lambda x: x.replace('**', ''),  # Fix malformed __init__ patterns
            r'\.py\.bak$': '.py.backup',  # Standardize backup files
        }
        
        for path in self.project_root.rglob('*'):
            for pattern, fix in patterns.items():
                if re.search(pattern, path.name):
                    new_name = re.sub(pattern, fix, path.name)
                    new_path = path.parent / new_name
                    
                    if verbose:
                        action = "Would rename" if dry_run else "Renaming"
                        print(f"{action}: {path.name} → {new_name}")
                    
                    if not dry_run and not new_path.exists():
                        path.rename(new_path)
    
    def _enforce_structure(self, dry_run: bool, verbose: bool) -> None:
        """Ensure required directories exist"""
        for dir_path in self.structure.protected_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                if verbose:
                    action = "Would create" if dry_run else "Creating"
                    print(f"{action} directory: {full_path}")
                if not dry_run:
                    full_path.mkdir(parents=True, exist_ok=True)
    
    def _should_move_cache(self, path: Path) -> bool:
        """Determine if a cache directory should be moved"""
        return not any(
            parent.name.startswith('.cache')
            for parent in path.parents
        )

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="TarotAI Project Structure Maintenance",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--dry-run', action='store_true', help="Show what would be done")
    parser.add_argument('--verbose', action='store_true', help="Show detailed output")
    args = parser.parse_args()
    
    try:
        cleaner = ProjectCleaner()
        cleaner.clean(dry_run=args.dry_run, verbose=args.verbose)
        print("\nMaintenance complete!")
    except Exception as e:
        print(f"Error during maintenance: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()