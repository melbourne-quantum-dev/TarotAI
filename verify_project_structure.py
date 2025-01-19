#!/usr/bin/env python3
"""
Project structure verification tool for TarotAI.

This script ensures that the project structure matches the canonical structure
defined in SSOT.md. It verifies three key aspects:
1. Root directory structure contains only allowed directories
2. All required directories and files are present
3. Test coverage exists for all source files

The script is designed for both development and CI/CD use, with clear exit
codes and structured logging to facilitate pipeline integration.

Exit codes:
    0: All checks passed
    1: Structure verification failed
    2: Critical error during execution

Usage:
    ./verify_project_structure.py
"""
from pathlib import Path
from typing import List, Set, Dict, Optional
import logging
import sys
from dataclasses import dataclass

# Configure logging with a format that works well in both terminal and CI output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class VerificationResult:
    """Container for verification results with structured output."""
    passed: bool
    issues: List[str]
    category: str

    def __str__(self) -> str:
        """Provide a human-readable string representation of the results."""
        if self.passed:
            return f"{self.category}: ✓ Passed"
        return f"{self.category}: ✗ Failed ({len(self.issues)} issues)"

class ProjectStructure:
    """
    Manages project structure verification rules and execution.
    
    This class encapsulates all verification logic and maintains the canonical
    lists of required files and directories. It provides methods to verify
    different aspects of the project structure.
    """

    # Root level directories that are allowed
    ALLOWED_ROOT_DIRS: Set[str] = {
    'src',
    'tests',
    'docs',
    'data',
    'scripts',
    '.git',
    '.github',
    '__pycache__',
    '.pytest_cache',
    '.venv',
    'venv',
    '.cache',              # Add this
    '.aider.tags.cache.v3' # Add this
    }

    # Required directory structure based on SSOT.md
    REQUIRED_DIRS: Set[str] = {
        'src/tarotai/ai/agents/orchestration',
        'src/tarotai/ai/agents/validation',
        'src/tarotai/ai/clients/providers',
        'src/tarotai/ai/knowledge',
        'src/tarotai/ai/prompts/templates',
        'src/tarotai/ai/rag',
        'src/tarotai/ai/embeddings',  # Add this
        'src/tarotai/core/models',
        'src/tarotai/core/errors',
        'src/tarotai/core/validation',
        'src/tarotai/config/schemas',
        'tests/ai/agents',
        'tests/ai/clients',
        'tests/ai/rag',
        'tests/ai/embeddings',  # Add this
        'tests/core/models',
        'tests/core/validation',
    }

    # Required files based on SSOT.md
    REQUIRED_FILES: Set[str] = {
        'data/cards_ordered.json',
        'data/golden_dawn.json',
        'docs/architecture/SSOT.md',
        'src/tarotai/ai/agents/orchestration/interpreter.py',
        'src/tarotai/ai/agents/orchestration/reading.py',
        'src/tarotai/ai/clients/providers/claude.py',
        'src/tarotai/ai/clients/providers/deepseek_v3.py',
        'src/tarotai/ai/clients/providers/voyage.py',
        'src/tarotai/ai/clients/base.py',
        'src/tarotai/ai/clients/registry.py',
        'src/tarotai/ai/knowledge/golden_dawn.py',
        'src/tarotai/ai/rag/generator.py',
        'src/tarotai/ai/rag/manager.py',
        'src/tarotai/ai/rag/vector_store.py',
        'src/tarotai/core/models/card.py',
        'src/tarotai/core/models/deck.py',
        'src/tarotai/core/models/types.py',
        'src/tarotai/core/errors/base.py',
    }

    def __init__(self, root_path: Path):
        """
        Initialize the project structure verifier.
        
        Args:
            root_path: Path to the project root directory
        """
        self.root_path = root_path

    def verify_root_dirs(self) -> VerificationResult:
        """
        Verify only allowed directories exist at root level.
        
        This check prevents project pollution with unexpected directories
        and helps maintain a clean project structure.
        
        Returns:
            VerificationResult containing any issues found
        """
        issues = []
        root_items = [item.name for item in self.root_path.iterdir() if item.is_dir()]
        
        for item in root_items:
            if item not in self.ALLOWED_ROOT_DIRS:
                issues.append(f"Unexpected directory in root: {item}")
        
        return VerificationResult(
            passed=len(issues) == 0,
            issues=issues,
            category="Root Directory Structure"
        )

    def verify_required_structure(self) -> VerificationResult:
        """
        Verify all required directories and files exist.
        
        This check ensures that the project contains all necessary
        components as defined in the SSOT documentation.
        
        Returns:
            VerificationResult containing any issues found
        """
        issues = []
        
        # Check required directories
        for dir_path in self.REQUIRED_DIRS:
            full_path = self.root_path / dir_path
            if not full_path.exists():
                issues.append(f"Missing required directory: {dir_path}")
        
        # Check required files
        for file_path in self.REQUIRED_FILES:
            full_path = self.root_path / file_path
            if not full_path.exists():
                issues.append(f"Missing required file: {file_path}")
                
        return VerificationResult(
            passed=len(issues) == 0,
            issues=issues,
            category="Required Structure"
        )

    def verify_test_coverage(self) -> VerificationResult:
        """
        Verify test files exist for all source files.
        
        This check ensures that every Python module (except __init__.py)
        has a corresponding test file, maintaining test coverage.
        
        Returns:
            VerificationResult containing any issues found
        """
        issues = []
        src_path = self.root_path / 'src' / 'tarotai'
        test_path = self.root_path / 'tests'
        
        try:
            for src_file in src_path.rglob('*.py'):
                if src_file.name == '__init__.py':
                    continue
                    
                relative_path = src_file.relative_to(src_path)
                test_file = test_path / relative_path.parent / f"test_{relative_path.name}"
                
                if not test_file.exists():
                    issues.append(f"Missing test file: {test_file}")
        except Exception as e:
            logger.error(f"Error during test coverage verification: {str(e)}")
            issues.append(f"Test coverage verification failed: {str(e)}")
        
        return VerificationResult(
            passed=len(issues) == 0,
            issues=issues,
            category="Test Coverage"
        )

def run_verification() -> int:
    """
    Run all verification checks and return appropriate exit code.
    
    This function orchestrates the verification process and provides
    structured output for both human readers and CI/CD systems.
    
    Returns:
        int: Exit code indicating verification result
        0: All checks passed
        1: Structure verification failed
        2: Critical error during execution
    """
    try:
        root_path = Path(__file__).parent
        verifier = ProjectStructure(root_path)
        
        # Run all verifications
        results = [
            verifier.verify_root_dirs(),
            verifier.verify_required_structure(),
            verifier.verify_test_coverage()
        ]
        
        # Process results
        all_passed = all(result.passed for result in results)
        
        # Report results
        if all_passed:
            logger.info("\n✨ Project structure verification passed! ✨")
            return 0
        else:
            logger.error("\nProject structure verification failed!")
            for result in results:
                if not result.passed:
                    logger.error(f"\n{result.category} issues:")
                    for issue in result.issues:
                        logger.error(f"  - {issue}")
            return 1
            
    except Exception as e:
        logger.error(f"Critical error during verification: {str(e)}")
        return 2

if __name__ == '__main__':
    sys.exit(run_verification())