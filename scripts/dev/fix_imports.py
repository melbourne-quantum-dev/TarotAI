#!/usr/bin/env python3
"""
Script to fix imports after refactoring
"""
import os
import re
from pathlib import Path
from typing import Set, Tuple

IMPORT_REPLACEMENTS = {
    # Core/Types imports
    r'from \.\.\.core\.types import': 'from ....core.models.types import',
    r'from \.\.core\.types import': 'from ...core.models.types import',
    r'from \.core\.types import': 'from ..core.models.types import',
    
    # Client imports
    r'from \.\.core import BaseAIClient': 'from ..clients.base import BaseAIClient',
    r'from \.\.\.core import BaseAIClient': 'from ...clients.base import BaseAIClient',
    r'from \.core import BaseAIClient': 'from .base import BaseAIClient',
    
    # AI Provider imports
    r'from \.\.embeddings\.voyage import VoyageClient': 'from .providers.voyage import VoyageClient',
    r'from \.deepseek_v3 import DeepSeekClient': 'from .providers.deepseek import DeepSeekClient',
    r'from \.claude import ClaudeClient': 'from .providers.claude import ClaudeClient',
    
    # Config imports
    r'from src\.tarotai\.config': 'from ....config',
    
    # Fix absolute imports
    r'from src\.tarotai\.ai\.embeddings': 'from ..embeddings',
    r'from src\.tarotai\.ai\.clients': 'from ..clients',
    
    # Fix client base imports in providers
    r'from \.\.clients\.base': 'from ..base',
    
    # Fix remaining absolute imports
    r'from src\.tarotai\.': 'from ....',
}

def find_absolute_imports(content: str) -> Set[str]:
    """Find any remaining absolute imports starting with 'src.tarotai'"""
    pattern = r'^from src\.tarotai\.[^\s]+ import|^import src\.tarotai\.'
    matches = re.finditer(pattern, content, re.MULTILINE)
    return {match.group(0) for match in matches}

def fix_imports(file_path: Path) -> Tuple[bool, Set[str]]:
    """Fix imports in a single file and return any remaining absolute imports"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    for old, new in IMPORT_REPLACEMENTS.items():
        content = re.sub(old, new, content)
    
    absolute_imports = find_absolute_imports(content)
    
    if content != original:
        print(f"Fixing imports in {file_path}")
        with open(file_path, 'w') as f:
            f.write(content)
        return True, absolute_imports
    return False, absolute_imports

def main():
    """Main entry point"""
    src_dir = Path(__file__).parent.parent.parent / 'src' / 'tarotai'
    python_files = src_dir.rglob('*.py')
    
    fixed_files = 0
    all_absolute_imports = set()
    
    for file_path in python_files:
        was_fixed, absolute_imports = fix_imports(file_path)
        if was_fixed:
            fixed_files += 1
        if absolute_imports:
            all_absolute_imports.update(absolute_imports)
    
    print(f"\nFixed imports in {fixed_files} files")
    
    if all_absolute_imports:
        print("\nWarning: Found remaining absolute imports:")
        for imp in sorted(all_absolute_imports):
            print(f"  {imp}")
        print("\nThese should be converted to relative imports.")

if __name__ == '__main__':
    main()