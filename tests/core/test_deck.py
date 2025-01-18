import pytest
from pathlib import Path
from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import CardSuit
from tarotai.core.errors import DeckError

@pytest.fixture
def test_deck():
    return TarotDeck(Path("data/test_cards.json"))

def test_deck_initialization(test_deck):
    """Test deck initialization with valid data"""
    assert len(test_deck.cards) == 2  # Based on test_cards.json
    assert test_deck.remaining == 2
    assert test_deck.drawn == 0

def test_deck_shuffle(test_deck):
    """Test deck shuffling"""
    initial_order = test_deck._current_deck.copy()
    test_deck.shuffle()
    assert test_deck._current_deck != initial_order

def test_deck_draw(test_deck):
    """Test drawing cards from the deck"""
    drawn_cards = test_deck.draw(2)
    assert len(drawn_cards) == 2
    assert test_deck.remaining == 0
    assert test_deck.drawn == 2

def test_deck_reset(test_deck):
    """Test resetting the deck"""
    test_deck.draw(2)
    test_deck.reset()
    assert test_deck.remaining == 2
    assert test_deck.drawn == 0

def test_deck_get_card_by_name(test_deck):
    """Test retrieving a card by name"""
    card = test_deck.get_card_by_name("Test Card 1")
    assert card is not None
    assert card.name == "Test Card 1"

def test_deck_get_cards_by_suit(test_deck):
    """Test retrieving cards by suit"""
    wands_cards = test_deck.get_cards_by_suit(CardSuit.WANDS)
    assert len(wands_cards) == 1
    assert wands_cards[0].suit == CardSuit.WANDS

def test_deck_draw_too_many_cards(test_deck):
    """Test drawing more cards than available"""
    with pytest.raises(DeckError):
        test_deck.draw(3)
