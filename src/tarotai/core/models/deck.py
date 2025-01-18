"""
TarotDeck implementation for TarotAI.
Handles deck operations including shuffling, drawing, and management of card states.
"""

import json
import random
import traceback
from pathlib import Path
from typing import List, Optional, Tuple

from tarotai.core.errors import DeckError
from tarotai.core.models.types import CardMeaning, CardSuit, ErrorSeverity


class TarotDeck:
    """
    Tarot deck implementation following the Golden Dawn Book T sequence:
    - Aces (Wands, Cups, Swords, Pentacles)
    - Pips by decan (5-7 Wands, 8-10 Pentacles, 2-4 Swords, etc.)
    - Court Cards
    - Major Arcana (0-XXI)
    """
    
    BOOK_T_SEQUENCE = [
        # Aces
        (CardSuit.WANDS, [1]),
        (CardSuit.CUPS, [1]),
        (CardSuit.SWORDS, [1]),
        (CardSuit.PENTACLES, [1]),
        # Pips by decan
        (CardSuit.WANDS, range(5, 8)),
        (CardSuit.PENTACLES, range(8, 11)),
        (CardSuit.SWORDS, range(2, 5)),
        (CardSuit.CUPS, range(5, 8)),
        (CardSuit.WANDS, range(8, 11)),
        (CardSuit.PENTACLES, range(2, 5)),
        (CardSuit.SWORDS, range(5, 8)),
        (CardSuit.CUPS, range(8, 11)),
        (CardSuit.WANDS, range(2, 5)),
        (CardSuit.PENTACLES, range(5, 8)),
        (CardSuit.SWORDS, range(8, 11)),
        (CardSuit.CUPS, range(2, 5)),
        # Courts (Knight=11, Queen=12, King=13, Princess=14)
        (CardSuit.WANDS, range(11, 15)),
        (CardSuit.CUPS, range(11, 15)),
        (CardSuit.SWORDS, range(11, 15)),
        (CardSuit.PENTACLES, range(11, 15)),
        # Majors (0-XXI)
        (CardSuit.MAJOR, range(0, 22))
    ]

    def __init__(self, cards_data: Path):
        """Initialize deck with cards from JSON data file"""
        self.cards: List[CardMeaning] = self._load_cards(cards_data)
        self._drawn_cards: List[CardMeaning] = []
        self.reset()

    def _load_cards(self, cards_data: Path) -> List[CardMeaning]:
        """Load card definitions from JSON file"""
        try:
            with open(cards_data, 'r') as f:
                cards_raw = json.load(f)
                return [CardMeaning(**card) for card in cards_raw]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise DeckError(
                f"Failed to load cards data: {e}",
                detail={
                    "file_path": str(cards_data),
                    "error_type": type(e).__name__
                },
                severity=ErrorSeverity.CRITICAL
            )
        except Exception as e:
            raise DeckError(
                f"Invalid card data format: {e}",
                detail={
                    "file_path": str(cards_data),
                    "error_type": type(e).__name__,
                    "traceback": traceback.format_exc() if self.config.dev_mode else None
                },
                severity=ErrorSeverity.CRITICAL
            )

    def _arrange_deck(self) -> List[CardMeaning]:
        """Arrange cards in Book T sequence"""
        arranged = []
        for suit, numbers in self.BOOK_T_SEQUENCE:
            suit_cards = [c for c in self.cards if c.suit == suit and c.number in numbers]
            arranged.extend(sorted(suit_cards, key=lambda x: x.number))
        return arranged

    def shuffle(self) -> None:
        """Shuffle the remaining cards in the deck"""
        random.shuffle(self._current_deck)

    def draw(self, count: int = 1) -> List[Tuple[CardMeaning, bool]]:
        """Draw specified number of cards from the deck"""
        if count > len(self._current_deck):
            raise DeckError(f"Cannot draw {count} cards, only {len(self._current_deck)} remaining")
        
        drawn = []
        for _ in range(count):
            card = self._current_deck.pop()
            is_reversed = random.random() > 0.5
            drawn.append((card, is_reversed))
            self._drawn_cards.append(card)
        
        return drawn

    def reset(self) -> None:
        """Reset deck to initial state"""
        self._current_deck = self._arrange_deck()
        self._drawn_cards = []
        self.shuffle()

    @property
    def remaining(self) -> int:
        """Number of cards remaining in deck"""
        return len(self._current_deck)

    @property
    def drawn(self) -> int:
        """Number of cards drawn from deck"""
        return len(self._drawn_cards)

    def get_card_by_name(self, name: str) -> Optional[CardMeaning]:
        """Retrieve a card by its name"""
        return next((card for card in self.cards if card.name.lower() == name.lower()), None)

    def get_cards_by_suit(self, suit: CardSuit) -> List[CardMeaning]:
        """Retrieve all cards of a specific suit"""
        return [card for card in self.cards if card.suit == suit]
