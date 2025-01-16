"""
Core card implementation for TarotAI.
Handles card operations, validation, and transformations.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import json
from pydantic import BaseModel, Field, validator
from .types import CardMeaning, CardSuit

class CardError(Exception):
    """Base exception for card-related errors."""
    pass

class TarotCard(BaseModel):
    """
    Represents a tarot card with enhanced functionality.
    Extends the base CardMeaning model with additional methods.
    """
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
        """Validate card number based on suit."""
        if values.get('suit') == CardSuit.MAJOR and not 0 <= v <= 21:
            raise ValueError("Major Arcana cards must be numbered 0-21")
        if values.get('suit') != CardSuit.MAJOR and not 1 <= v <= 14:
            raise ValueError("Minor Arcana cards must be numbered 1-14")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization."""
        return self.dict()

    def get_meaning(self, is_reversed: bool = False) -> str:
        """Get the meaning of the card based on orientation."""
        return self.reversed_meaning if is_reversed else self.upright_meaning

    def get_keywords(self, is_reversed: bool = False) -> List[str]:
        """Get keywords for the card, optionally reversed."""
        if is_reversed:
            return [f"Reversed: {kw}" for kw in self.keywords]
        return self.keywords

    def get_element(self) -> str:
        """Get the elemental association of the card."""
        if self.element:
            return self.element
        if self.suit == CardSuit.WANDS:
            return "Fire"
        if self.suit == CardSuit.CUPS:
            return "Water"
        if self.suit == CardSuit.SWORDS:
            return "Air"
        if self.suit == CardSuit.PENTACLES:
            return "Earth"
        return "Unknown"

    def __str__(self) -> str:
        """String representation of the card."""
        return f"{self.name} ({self.suit or 'Major Arcana'})"

class CardManager:
    """
    Manages loading, saving, and querying tarot cards.
    """
    def __init__(self, cards_file: Path = Path("data/cards_ordered.json")):
        self.cards_file = cards_file
        self.cards: List[TarotCard] = self._load_cards()

    def _load_cards(self) -> List[TarotCard]:
        """Load cards from JSON file and validate against TarotCard model."""
        try:
            with open(self.cards_file, 'r', encoding='utf-8') as f:
                raw_cards = json.load(f)["cards"]
            return [TarotCard(**card) for card in raw_cards]
        except Exception as e:
            raise CardError(f"Failed to load cards: {str(e)}")

    def get_card_by_name(self, name: str) -> Optional[TarotCard]:
        """Retrieve a card by its name."""
        return next((card for card in self.cards if card.name.lower() == name.lower()), None)

    def get_cards_by_suit(self, suit: CardSuit) -> List[TarotCard]:
        """Retrieve all cards of a specific suit."""
        return [card for card in self.cards if card.suit == suit]

    def get_major_arcana(self) -> List[TarotCard]:
        """Retrieve all Major Arcana cards."""
        return [card for card in self.cards if card.suit == CardSuit.MAJOR]

    def get_minor_arcana(self) -> List[TarotCard]:
        """Retrieve all Minor Arcana cards."""
        return [card for card in self.cards if card.suit != CardSuit.MAJOR]

    def get_cards_by_element(self, element: str) -> List[TarotCard]:
        """Retrieve all cards associated with a specific element."""
        return [card for card in self.cards if card.get_element().lower() == element.lower()]

    def save_cards(self, output_file: Optional[Path] = None) -> None:
        """Save cards to a JSON file."""
        try:
            cards_dict = {"cards": [card.to_dict() for card in self.cards]}
            with open(output_file or self.cards_file, 'w', encoding='utf-8') as f:
                json.dump(cards_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise CardError(f"Failed to save cards: {str(e)}")
