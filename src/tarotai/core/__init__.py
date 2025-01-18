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
"""
Core functionality for TarotAI
"""
from .models.types import *
from .models.card import *
from .models.deck import *
from .services.reading import *
from .services.interpreter import *
from .services.card_processor import *

__all__ = [
    'CardMeaning',
    'CardSuit',
    'TarotDeck',
    'ReadingInput',
    'TarotInterpreter',
    'CardProcessor'
]
"""
Core functionality for TarotAI
"""
from .models.types import *
from .models.card import *
from .models.deck import *
from .services.reading import *
from .services.interpreter import *
from .services.card_processor import *

__all__ = [
    'CardMeaning',
    'CardSuit',
    'TarotDeck',
    'ReadingInput',
    'TarotInterpreter',
    'CardProcessor'
]
