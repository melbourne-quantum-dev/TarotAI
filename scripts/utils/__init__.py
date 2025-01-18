"""
Shared Utility Functions for Scripts
"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict

from rich.console import Console
from rich.table import Table

console = Console()

def log_processing_step(step: str, logger: logging.Logger) -> None:
    """Standardized logging for processing steps"""
    logger.info(f"Starting step: {step}")
    console.print(f"[bold cyan]➤ {step}[/]")

def validate_file(path: Path, required: bool = True) -> bool:
    """Validate file existence and permissions"""
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Required file not found: {path}")
        return False
        
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
        
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read file: {path}")
        
    return True

def track_usage(stats: Dict[str, Any], logger: logging.Logger) -> None:
    """Track and log usage statistics"""
    logger.info("Usage Statistics:")
    for key, value in stats.items():
        logger.info(f"  {key}: {value}")
        
    console.print("\n[bold]Usage Statistics:[/]")
    table = Table(show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in stats.items():
        table.add_row(key, str(value))
        
    console.print(table)

def save_results(data: Any, path: Path, logger: logging.Logger) -> None:
    """Save results with standardized formatting"""
    try:
        with open(path, "w") as f:
            if isinstance(data, dict):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        logger.info(f"Saved results to {path}")
    except Exception as e:
        logger.error(f"Failed to save results: {str(e)}")
        raise
