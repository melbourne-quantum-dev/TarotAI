from pathlib import Path

# Package version handling
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # Python < 3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("tarotai")
except PackageNotFoundError:
    __version__ = "2.1.0"  # Fallback to hardcoded version

# Package data files
def get_data_path():
    """Get path to package data files"""
    return Path(__file__).parent / "data"

# Expose core components
from .core.models.deck import TarotDeck
from .core.models.card import TarotCard, CardManager
from .core.services.interpreter import TarotInterpreter
from .core.models.types import (
    CardMeaning,
    Reading,
    QuestionContext,
    CardSuit,
    SpreadType,
    ReadingType,
    UserProfile,
    CardEmbeddings,
    ReadingEmbeddings
)
from .ui.display import TarotDisplay
from .core.reading import ReadingInput
from .core.card_processor import CardProcessor
from .cli import app

__all__ = [
    # Core models
    "TarotDeck",
    "TarotCard",
    "CardManager",
    
    # Types
    "CardMeaning",
    "Reading",
    "QuestionContext",
    "CardSuit",
    "SpreadType",
    "ReadingType",
    "UserProfile",
    "CardEmbeddings",
    "ReadingEmbeddings",
    
    # Processing
    "CardProcessor",
    "ReadingInput",
    "TarotInterpreter",
    
    # UI
    "TarotDisplay",
    
    # Utils
    "get_data_path",
    
    # CLI
    "app"
]
