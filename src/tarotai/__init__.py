"""
TarotAI - Neural-Enhanced Tarot Reading System
"""
from pathlib import Path

# Package version handling
try:
    from importlib.metadata import version
    __version__ = version("tarotai")
except Exception:
    __version__ = "2.0.0"

# Core imports
from .core import (
    TarotCard,
    TarotDeck,
    ReadingInput,
    SpreadType,
    ErrorSeverity,
    TarotAIError,
    ProcessingError,
    EnrichmentError,
    EmbeddingError,
    setup_logging
)

from .core.services import TarotInterpreter

# AI imports
from .ai import (
    UnifiedAIClient
)

# UI imports
from .ui import (
    TarotDisplay,
)

# CLI and Config
from .cli import app
from .config import get_config

__all__ = [
    # Core
    'TarotCard',
    'TarotDeck',
    'ReadingInput',
    'SpreadType',
    
    # Errors
    'ErrorSeverity',
    'TarotAIError',
    'ProcessingError',
    'EnrichmentError',
    'EmbeddingError',
    
    # Services
    'TarotInterpreter',
    
    # AI
    'UnifiedAIClient',
    
    # UI
    'TarotDisplay',
    
    # CLI and Config
    'app',
    'get_config',
    
    # Logging
    'setup_logging',
    
    # Version
    '__version__'
]
