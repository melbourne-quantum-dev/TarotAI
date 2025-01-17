"""
Core type definitions for TarotAI system.
This module contains all Pydantic models and type hints used throughout the application.
"""

from datetime import date
from enum import Enum
from typing import List, Dict, Optional, Any, Literal, Tuple
from pydantic import BaseModel, Field, validator

# Enums
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
    
    @property
    def display_name(self) -> str:
        return {
            "single": "◈ Single Card",
            "three_card": "◈ Three Card",
            "celtic_cross": "◈ Celtic Cross",
            "horseshoe": "◈ Horseshoe"
        }[self.value]

class ReadingType(str, Enum):
    SINGLE = "single"
    THREE_CARD = "three_card"
    CELTIC_CROSS = "celtic_cross"
    CUSTOM = "custom"

# Models
class UserProfile(BaseModel):
    """User profile information for personalized readings"""
    name: Optional[str] = Field(None, description="User's preferred name")
    birth_date: Optional[date] = Field(None, description="User's birth date for astrological context")
    reading_style: Literal["practical", "spiritual", "psychological"] = Field(
        "practical", 
        description="Preferred interpretation style"
    )
    detail_level: Literal["brief", "moderate", "detailed"] = Field(
        "moderate",
        description="Preferred level of detail in readings"
    )

class QuestionContext(BaseModel):
    """Represents the context of a tarot reading question"""
    focus: str = Field(..., description="Main focus or theme of the reading")
    raw_question: str = Field(..., description="Original question asked by the querent")
    additional_context: Optional[Dict[str, str]] = Field(default=None)
    user_profile: Optional[UserProfile] = Field(
        None,
        description="User profile information for personalized readings"
    )
    reading_history: Optional[List["Reading"]] = Field(
        None,
        description="User's previous readings for pattern analysis"
    )
    temporal_context: Optional[Dict[str, Any]] = Field(
        None,
        description="Temporal context like moon phase and astrological transits"
    )

class CardMeaning(BaseModel):
    """Represents the meaning of a tarot card"""
    name: str
    number: int = Field(..., ge=0, le=21)
    suit: Optional[CardSuit]
    keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
    element: Optional[str] = None
    planetary_correspondence: Optional[str] = None

    @validator('number')
    def validate_number(cls, v, values):
        if values.get('suit') == CardSuit.MAJOR and not 0 <= v <= 21:
            raise ValueError("Major Arcana cards must be numbered 0-21")
        if values.get('suit') != CardSuit.MAJOR and not 1 <= v <= 14:
            raise ValueError("Minor Arcana cards must be numbered 1-14")
        return v

class SpreadPosition(BaseModel):
    """Represents a position in a tarot spread"""
    name: str
    description: str
    influence: str

class Reading(BaseModel):
    """Represents a complete tarot reading"""
    context: QuestionContext
    reading_type: ReadingType
    positions: List[SpreadPosition]
    cards: List[CardMeaning]
    is_reversed: List[bool]
    timestamp: str = Field(..., description="ISO format timestamp of the reading")
    interpretation: Optional[str] = None

# Type Aliases
CardTuple = Tuple[CardMeaning, bool]
CardEmbedding = List[float]
ReadingEmbedding = Dict[str, CardEmbedding]
