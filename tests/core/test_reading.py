from pathlib import Path

import pytest

from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import Reading
from tarotai.core.services.reading import ManualInput


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

def test_manual_reading_creation():
    """Test manual reading creation"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    manual_input = ManualInput(
        deck,
        cards=[("The Fool", True), ("The Magician", False)]
    )
    cards = manual_input.get_cards()
    assert len(cards) == 2
    assert cards[0][0].name == "The Fool"
    assert cards[0][1] is True
    assert cards[1][0].name == "The Magician"
    assert cards[1][1] is False

def test_manual_reading_invalid_card():
    """Test manual reading with invalid card"""
    deck = TarotDeck(Path("data/cards_ordered.json"))
    with pytest.raises(ValueError):
        ManualInput(
            deck,
            cards=[("Invalid Card", False)]
        ).get_cards()
