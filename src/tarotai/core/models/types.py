import uuid
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

__all__ = [
    'CardMeaning', 'Reading', 'CardSuit', 'SpreadType',
    'ReadingType', 'UserProfile', 'QuestionContext'
]

class ErrorSeverity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class CardSuit(str, Enum):
    MAJOR = "major"
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"

class SpreadType(str, Enum):
    SINGLE = "single"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    HORSESHOE = "horseshoe"

class ReadingType(str, Enum):
    GENERAL = "general"
    LOVE = "love"
    CAREER = "career"
    SPIRITUAL = "spiritual"
    SPECIFIC = "specific"

class QuestionContext(BaseModel):
    question: str
    focus: str
    raw_question: str
    additional_context: Optional[Dict[str, str]] = None

class CardMeaning(BaseModel):
    name: str
    number: Optional[int] = Field(default=None, ge=0, le=21)  # 0-21 for Major, 1-14 for Minor
    suit: Optional[CardSuit] = None
    keywords: List[str] = Field(default_factory=list)
    upright_meaning: str = ""
    reversed_meaning: str = ""
    element: Optional[str] = None
    astrological: Optional[str] = None
    kabbalistic: Optional[str] = None
    decan: Optional[str] = None
    golden_dawn: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Golden Dawn specific card data"
    )
    embeddings: Optional[Dict[str, List[float]]] = Field(
        default=None,
        description="Embeddings for card meanings and images"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "last_updated": datetime.now().isoformat(),
            "source": "generated",
            "confidence": 1.0
        },
        description="Metadata about the card data"
    )

class Reading(BaseModel):
    """Represents a tarot reading"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    context: QuestionContext
    reading_type: ReadingType
    spread_type: SpreadType
    cards: List[CardMeaning]
    is_reversed: List[bool]
    timestamp: datetime = Field(default_factory=datetime.now)
    interpretation: Optional[str] = None
    model: Optional[str] = None

class UserProfile(BaseModel):
    id: str
    preferences: Dict[str, str]
    history: Optional[List[str]] = None

class CardEmbeddings(BaseModel):
    text_embedding: List[float]
    image_embedding: Optional[List[float]] = None
    multimodal_embedding: Optional[List[float]] = None
    quantized_embedding: Optional[List[int]] = None
    reduced_dimension_embedding: Optional[List[float]] = None
    version: str = "2.0"

class ReadingEmbeddings(BaseModel):
    card_embeddings: List[CardEmbeddings]
    position_embeddings: List[List[float]]
    context_embedding: List[float]
    version: int = 2
