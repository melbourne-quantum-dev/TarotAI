"""
TarotAI - Neural-Enhanced Tarot Reading System
"""

# Package version handling
try:
    from importlib.metadata import version
    __version__ = version("tarotai")
except Exception:
    __version__ = "2.0.0"

# Core imports
from tarotai.core.models import SpreadType, TarotCard, TarotDeck
from tarotai.core.services import TarotInterpreter, setup_logging
from tarotai.core.services.reading import ReadingInput

# AI imports
from .ai import UnifiedAIClient

# CLI and Config
from .cli import app
from .config import get_config

# UI imports
from .ui import TarotDisplay

__all__ = [
    # Core Models
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
    'setup_logging',
    
    # AI
    'UnifiedAIClient',
    
    # UI
    'TarotDisplay',
    
    # CLI and Config
    'app',
    'get_config',
    
    # Version
    '__version__'
]
