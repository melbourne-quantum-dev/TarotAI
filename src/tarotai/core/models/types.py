from enum import Enum, auto
from typing import List, Optional, Dict
from datetime import datetime
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
    number: int = Field(ge=0, le=21)  # 0-21 for Major, 1-14 for Minor
    suit: Optional[CardSuit] = None
    keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
    element: Optional[str] = None
    planet: Optional[str] = None

class Reading(BaseModel):
    context: QuestionContext
    reading_type: ReadingType
    spread_type: SpreadType
    cards: List[CardMeaning]
    is_reversed: List[bool]
    timestamp: datetime = Field(default_factory=datetime.now)
    interpretation: Optional[str] = None

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
