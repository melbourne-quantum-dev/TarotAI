"""
Core card implementation for TarotAI.

This module handles card operations, validation, and transformations.
See also: 
- src/tarotai/core/types.py for CardMeaning model
- src/tarotai/core/deck.py for deck management
"""

from pathlib import Path
from typing import List, Dict, Optional, Any
import json
from pydantic import BaseModel, Field, validator
from tarotai.core.models.types import CardMeaning, CardSuit
from tarotai.core.errors.errors import DeckError

class CardError(Exception):
    """Base exception for card-related errors.
    
    See also:
    - src/tarotai/core/errors.py for other error types
    """
    pass

class TarotCard(BaseModel):
    """
    Represents a tarot card with enhanced functionality.
    Extends the base CardMeaning model with additional methods.
    
    Attributes:
        name: Name of the card
        number: Card number (0-21 for Major, 1-14 for Minor)
        suit: Card suit (Wands, Cups, Swords, Pentacles, or Major Arcana)
        keywords: List of keywords associated with the card
        upright_meaning: Meaning when card is upright
        reversed_meaning: Meaning when card is reversed
        element: Associated element (Fire, Water, Air, Earth)
        planetary_correspondence: Associated planetary correspondence
        
    See also:
    - src/tarotai/core/types.py for CardMeaning base model
    - src/tarotai/core/deck.py for deck operations
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
        """Validate card number based on suit.
        
        Raises:
            ValueError: If number is invalid for the card's suit
        """
        if values.get('suit') == CardSuit.MAJOR and not 0 <= v <= 21:
            raise ValueError("Major Arcana cards must be numbered 0-21")
        if values.get('suit') != CardSuit.MAJOR and not 1 <= v <= 14:
            raise ValueError("Minor Arcana cards must be numbered 1-14")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert card to dictionary for serialization.
        
        Returns:
            Dictionary representation of the card
        """
        return self.dict()

    def get_meaning(self, is_reversed: bool = False) -> str:
        """Get the meaning of the card based on orientation.
        
        Args:
            is_reversed: Whether to get reversed meaning
            
        Returns:
            Card meaning text
        """
        return self.reversed_meaning if is_reversed else self.upright_meaning

    def get_keywords(self, is_reversed: bool = False) -> List[str]:
        """Get keywords for the card, optionally reversed.
        
        Args:
            is_reversed: Whether to mark keywords as reversed
            
        Returns:
            List of keywords
        """
        if is_reversed:
            return [f"Reversed: {kw}" for kw in self.keywords]
        return self.keywords

    def get_element(self) -> str:
        """Get the elemental association of the card.
        
        Returns:
            Element name (Fire, Water, Air, Earth)
            
        See also:
        - src/tarotai/core/types.py for CardSuit enum
        """
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
        """String representation of the card.
        
        Returns:
            Formatted string with card name and suit
        """
        return f"{self.name} ({self.suit or 'Major Arcana'})"

class CardManager:
    """
    Manages loading, saving, and querying tarot cards.
    
    See also:
    - src/tarotai/core/deck.py for deck operations
    - src/tarotai/core/types.py for card type definitions
    """
    def __init__(self, cards_file: Path = Path("data/cards_ordered.json")):
        """Initialize card manager.
        
        Args:
            cards_file: Path to JSON file containing card definitions
        """
        self.cards_file = cards_file
        self.cards: List[TarotCard] = self._load_cards()

    def _load_cards(self) -> List[TarotCard]:
        """Load cards from JSON file and validate against TarotCard model.
        
        Returns:
            List of validated TarotCard instances
            
        Raises:
            CardError: If card data is invalid or cannot be loaded
        """
        try:
            with open(self.cards_file, 'r', encoding='utf-8') as f:
                raw_cards = json.load(f)["cards"]
            return [TarotCard(**card) for card in raw_cards]
        except Exception as e:
            raise CardError(f"Failed to load cards: {str(e)}")

    def get_card_by_name(self, name: str) -> Optional[TarotCard]:
        """Retrieve a card by its name.
        
        Args:
            name: Name of card to retrieve
            
        Returns:
            TarotCard instance if found, None otherwise
        """
        return next((card for card in self.cards if card.name.lower() == name.lower()), None)

    def get_cards_by_suit(self, suit: CardSuit) -> List[TarotCard]:
        """Retrieve all cards of a specific suit.
        
        Args:
            suit: CardSuit to filter by
            
        Returns:
            List of cards matching the suit
        """
        return [card for card in self.cards if card.suit == suit]

    def get_major_arcana(self) -> List[TarotCard]:
        """Retrieve all Major Arcana cards.
        
        Returns:
            List of Major Arcana cards
        """
        return [card for card in self.cards if card.suit == CardSuit.MAJOR]

    def get_minor_arcana(self) -> List[TarotCard]:
        """Retrieve all Minor Arcana cards.
        
        Returns:
            List of Minor Arcana cards
        """
        return [card for card in self.cards if card.suit != CardSuit.MAJOR]

    def get_cards_by_element(self, element: str) -> List[TarotCard]:
        """Retrieve all cards associated with a specific element.
        
        Args:
            element: Element name to filter by
            
        Returns:
            List of cards matching the element
        """
        return [card for card in self.cards if card.get_element().lower() == element.lower()]

    def save_cards(self, output_file: Optional[Path] = None) -> None:
        """Save cards to a JSON file.
        
        Args:
            output_file: Optional path to save file (defaults to cards_file)
            
        Raises:
            CardError: If saving fails
        """
        try:
            cards_dict = {"cards": [card.to_dict() for card in self.cards]}
            with open(output_file or self.cards_file, 'w', encoding='utf-8') as f:
                json.dump(cards_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise CardError(f"Failed to save cards: {str(e)}")
