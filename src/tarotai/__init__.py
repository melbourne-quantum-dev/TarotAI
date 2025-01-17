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
from .core.deck import TarotDeck
from .core.card import TarotCard, CardManager
from .core.interpreter import TarotInterpreter
from .core.types import CardMeaning, Reading
from .cli import app

__all__ = [
    "TarotDeck",
    "TarotReader",
    "TarotDisplay",
    "TarotInterface",
    "Reading",
    "CardMeaning",
    "QuestionContext",
    "get_data_path",
    "app"
]
