from pathlib import Path

# Declare namespace package
__import__('pkg_resources').declare_namespace(__name__)

# Package version
__version__ = "2.1.0"

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