"""Core module for TarotAI"""

from .errors import (
    TarotError,
    TarotHTTPException,
    DeckError,
    ConfigError,
    EnrichmentError
)

from .models.types import (
    CardMeaning,
    Reading,
    QuestionContext,
    CardEmbeddings,
    ReadingEmbeddings,
    CardSuit,
    SpreadType,
    ReadingType,
    UserProfile
)

from .models.deck import TarotDeck
from .models.card import TarotCard, CardManager
from .services.interpreter import TarotInterpreter
from .services.reading import ReadingInput
from .services.card_processor import CardProcessor

__all__ = [
    # Errors
    'TarotError',
    'TarotHTTPException',
    'DeckError',
    'ConfigError',
    'EnrichmentError',
    
    # Types
    'CardMeaning',
    'Reading',
    'QuestionContext',
    'CardEmbeddings',
    'ReadingEmbeddings',
    'CardSuit',
    'SpreadType',
    'ReadingType',
    'UserProfile',
    
    # Core components
    'TarotDeck',
    'TarotCard',
    'CardManager',
    'ReadingInput',
    'CardProcessor',
    'TarotInterpreter'
]
