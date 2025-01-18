"""Core TarotAI functionality"""

from .models.card import TarotCard
from .models.deck import TarotDeck
from .models.types import CardSuit, CardMeaning, SpreadType
from .services.reading import ReadingInput
from .errors import (
    ErrorSeverity,
    TarotAIError,
    ProcessingError,
    EnrichmentError,
    EmbeddingError
)
from .logging import setup_logging

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
    'setup_logging'
]
from .models.types import (
    CardMeaning, Reading, CardSuit, SpreadType,
    ReadingType, UserProfile, QuestionContext
)
from .services import (
    CardProcessor,
    TarotInterpreter,
    ReadingInput
)

__all__ = [
    'CardMeaning', 'Reading', 'CardSuit', 'SpreadType',
    'ReadingType', 'UserProfile', 'QuestionContext',
    'CardProcessor', 'TarotInterpreter', 'ReadingInput'
]
