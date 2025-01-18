"""Core TarotAI functionality"""

from .errors import (
    EmbeddingError,
    EnrichmentError,
    ErrorSeverity,
    ProcessingError,
    TarotAIError,
)
from .logging import setup_logging
from .models.card import TarotCard
from .models.deck import TarotDeck
from .models.types import (
    CardMeaning,
    CardSuit,
    QuestionContext,
    Reading,
    ReadingType,
    SpreadType,
    UserProfile,
)
from .services import CardProcessor, ReadingInput, TarotInterpreter

__all__ = [
    'TarotCard',
    'TarotDeck',
    'ReadingInput',
    'SpreadType',
    'ErrorSeverity',
    'TarotAIError',
    'ProcessingError',
    'EnrichmentError',
    'EmbeddingError',
    'setup_logging',
    'CardMeaning',
    'Reading',
    'CardSuit',
    'ReadingType',
    'UserProfile',
    'QuestionContext',
    'CardProcessor',
    'TarotInterpreter'
]
