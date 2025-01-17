from tarotai.core.types import Reading
from tarotai.core.deck import TarotDeck
from pathlib import Path

def test_reading_creation():
    """Test basic reading creation"""
    reading = Reading(
        id="test-reading",
        cards=[("The Fool", True), ("The Magician", False)],
        interpretation="Test interpretation",
        model="test-model"
    )
    assert len(reading.cards) == 2
    assert reading.cards[0][0] == "The Fool"
    assert reading.cards[1][1] is False

def test_reading_from_deck():
    """Test creating a reading from a deck"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    cards = deck.draw(3)
    reading = Reading(
        id="deck-reading",
        cards=cards,
        interpretation="Test deck reading",
        model="test-model"
    )
    assert len(reading.cards) == 3
    assert all(isinstance(card[0], str) for card in reading.cards)
