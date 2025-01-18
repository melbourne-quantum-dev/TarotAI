from pathlib import Path
from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import CardMeaning

def test_deck_initialization():
    """Test that the deck initializes with all 78 cards"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    assert len(deck.cards) == 78
    assert all(isinstance(card, CardMeaning) for card in deck.cards)

def test_deck_shuffle():
    """Test that shuffling doesn't lose cards"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    initial_order = [card.name for card in deck._current_deck]
    deck.shuffle()
    shuffled_order = [card.name for card in deck._current_deck]
    
    assert len(shuffled_order) == 78
    assert set(shuffled_order) == set(initial_order)
    assert shuffled_order != initial_order  # Very small chance this could fail

def test_deck_draw():
    """Test drawing cards from the deck"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    drawn = deck.draw(3)
    
    assert len(drawn) == 3
    assert all(isinstance(card, tuple) and len(card) == 2 for card in drawn)
    assert deck.remaining == 75
    assert deck.drawn == 3
