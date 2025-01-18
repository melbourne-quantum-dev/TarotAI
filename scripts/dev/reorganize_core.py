#!/usr/bin/env python3
"""
Script to reorganize core module structure and fix imports
"""
import os
import re
import shutil
from pathlib import Path
FILES_TO_MOVE = [
    'card_processor.py',
    'interpreter.py',
    'reading.py'
]

# Import patterns to update
IMPORT_REPLACEMENTS = {
    # Fix error imports
    r'from \.errors import': 'from ..errors import',  # Fix models/*.py imports
    r'from tarotai\.core\.errors\.errors import': 'from tarotai.core.errors import',  # Fix config.py import
        
    # Fix imports in service files
    r'from \.\.base': 'from ...ai.clients.base',
    r'from \.providers\.voyage': 'from ...ai.clients.providers.voyage',
    r'from \.types': 'from ..models.types',
    r'from \.reading': 'from .reading',
    r'from \.clients\.': 'from ...ai.clients.',
    r'from \.\.core\.models\.': 'from ..models.',
    r'from \.config': 'from ...config',
    r'from \.\.ai\.rag': 'from ...ai.rag',
    r'from \.prompts': 'from ...ai.prompts',
    
    # Fix imports in interpreter.py
    r'from \.config': 'from ...config',
    r'from \.\.ai\.rag': 'from ...ai.rag',
    r'from \.prompts': 'from ...ai.prompts',
    
    # Update imports in files that import these services
    r'from \.core import (CardProcessor|TarotInterpreter|ReadingInput)': r'from .core.services import \1',
    r'from \.\.core import (CardProcessor|TarotInterpreter|ReadingInput)': r'from ..core.services import \1',
    r'from \.\.\.core import (CardProcessor|TarotInterpreter|ReadingInput)': r'from ...core.services import \1',
    
    # Fix core/__init__.py imports (reverse the previous pattern)
    r'from \.(interpreter|reading|card_processor)': r'from .services.\1',
    
    # Fix services/__init__.py imports
    r'from \.services\.(card_processor|interpreter|reading)': r'from .\1',
}

def backup_file(file_path: Path) -> None:
    """Create a backup of a file before modifying it"""
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    shutil.copy2(file_path, backup_path)
    print(f"Created backup: {backup_path}")

def update_imports(file_path: Path) -> bool:
    """Update imports in a single file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    for old, new in IMPORT_REPLACEMENTS.items():
        content = re.sub(old, new, content)
    
    if content != original:
        print(f"Updating imports in {file_path}")
        backup_file(file_path)
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    return False

def verify_imports() -> bool:
    """Verify no circular imports exist"""
    success = True
    try:
        from tarotai.core import models
        print("✓ Core models import successful")
    except ImportError as e:
        print(f"✗ Core models import failed: {e}")
        success = False
    
    try:
        from tarotai.core import services
        print("✓ Core services import successful")
    except ImportError as e:
        print(f"✗ Core services import failed: {e}")
        success = False
    
    try:
        from tarotai.core import errors
        print("✓ Core errors import successful")
    except ImportError as e:
        print(f"✗ Core errors import failed: {e}")
        success = False
    
    return success

def main():
    """Main entry point"""
    # Get project root
    src_dir = Path(__file__).parent.parent.parent / 'src' / 'tarotai'
    core_dir = src_dir / 'core'
    services_dir = core_dir / 'services'
    
    # Create services directory if it doesn't exist
    services_dir.mkdir(exist_ok=True)
    
    # Create services/__init__.py
    services_init = services_dir / '__init__.py'
    if not services_init.exists():
        print(f"Creating {services_init}")
        with open(services_init, 'w') as f:
            f.write('"""Service layer for core business logic"""\n\n')
            f.write('from .card_processor import CardProcessor\n')
            f.write('from .interpreter import TarotInterpreter\n')
            f.write('from .reading import ReadingInput\n\n')
            f.write('__all__ = [\n')
            f.write('    "CardProcessor",\n')
            f.write('    "TarotInterpreter",\n')
            f.write('    "ReadingInput"\n')
            f.write(']\n')
    
    # Move files
    for file_name in FILES_TO_MOVE:
        src_file = core_dir / file_name
        dst_file = services_dir / file_name
        if src_file.exists():
            print(f"Moving {src_file} to {dst_file}")
            shutil.move(src_file, dst_file)
    
    # Update imports in all Python files
    python_files = src_dir.rglob('*.py')
    fixed_files = 0
    
    for file_path in python_files:
        if update_imports(file_path):
            fixed_files += 1
    
    print(f"\nUpdated imports in {fixed_files} files")
    
    # Verify imports work
    if verify_imports():
        print("\nImport verification successful!")
    else:
        print("\nWarning: Import verification failed!")
    
    print("\nDone! New structure:")
    os.system(f"tree {core_dir}")
    
    print("\nBackup files were created with .bak extension")
    print("You can remove them once you verify everything works:")
    print("find src/tarotai -name '*.bak' -delete")

if __name__ == '__main__':
    main()
