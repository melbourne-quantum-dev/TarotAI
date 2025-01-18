import pytest
from pathlib import Path
from tarotai.core.models.card import CardManager, TarotCard, CardError
from tarotai.core.models.types import CardSuit

@pytest.fixture
def card_manager():
    return CardManager(Path("tests/data/test_cards.json"))

def test_card_manager_initialization(card_manager):
    """Test CardManager initialization"""
    assert len(card_manager.cards) > 0
    assert all(isinstance(card, TarotCard) for card in card_manager.cards)

def test_get_card_by_name(card_manager):
    """Test retrieving card by name"""
    card = card_manager.get_card_by_name("The Fool")
    assert card is not None
    assert card.name == "The Fool"
    
    # Test case sensitivity
    card = card_manager.get_card_by_name("the fool")
    assert card is not None
    
    # Test non-existent card
    card = card_manager.get_card_by_name("Non-existent Card")
    assert card is None

def test_get_cards_by_suit(card_manager):
    """Test filtering cards by suit"""
    wands = card_manager.get_cards_by_suit(CardSuit.WANDS)
    assert len(wands) > 0
    assert all(card.suit == CardSuit.WANDS for card in wands)
    
    majors = card_manager.get_cards_by_suit(CardSuit.MAJOR)
    assert len(majors) == 22  # 22 Major Arcana cards

def test_get_major_arcana(card_manager):
    """Test retrieving Major Arcana cards"""
    majors = card_manager.get_major_arcana()
    assert len(majors) == 22
    assert all(card.suit == CardSuit.MAJOR for card in majors)

def test_get_minor_arcana(card_manager):
    """Test retrieving Minor Arcana cards"""
    minors = card_manager.get_minor_arcana()
    assert len(minors) == 56  # 56 Minor Arcana cards
    assert all(card.suit != CardSuit.MAJOR for card in minors)

def test_get_cards_by_element(card_manager):
    """Test filtering cards by element"""
    fire_cards = card_manager.get_cards_by_element("Fire")
    assert len(fire_cards) > 0
    assert all(card.get_element() == "Fire" for card in fire_cards)

def test_save_cards(tmp_path, card_manager):
    """Test saving cards to file"""
    test_file = tmp_path / "test_cards.json"
    card_manager.save_cards(test_file)
    
    assert test_file.exists()
    assert test_file.stat().st_size > 0
    
    # Test error handling
    with pytest.raises(CardError):
        card_manager.save_cards(Path("/invalid/path/test.json"))

def test_load_cards_error_handling():
    """Test error handling when loading cards"""
    with pytest.raises(CardError):
        CardManager(Path("non_existent_file.json"))
