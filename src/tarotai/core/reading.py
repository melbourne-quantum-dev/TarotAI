from typing import List, Tuple
from pathlib import Path
from .types import CardMeaning
from .deck import TarotDeck

class ReadingInput:
    """Base class for reading input methods"""
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        raise NotImplementedError

class RandomDrawInput(ReadingInput):
    """Input method using random card draw"""
    def __init__(self, deck: TarotDeck, count: int):
        self.deck = deck
        self.count = count
        
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        return self.deck.draw(self.count)

class ManualInput(ReadingInput):
    """Input method for manual card entry"""
    def __init__(self, deck: TarotDeck, cards: List[Tuple[str, bool]]):
        self.deck = deck
        self.card_names = [name for name, _ in cards]
        self.reversed = [rev for _, rev in cards]
        
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        return [
            (self.deck.get_card_by_name(name), rev)
            for name, rev in zip(self.card_names, self.reversed)
        ]
