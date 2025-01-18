import pytest
from tarotai.core.models.card import TarotCard

@pytest.mark.unit
def test_minimal_card_creation():
    """Test card creation with minimal required fields"""
    card = TarotCard(
        name="The Magician",  # Changed from Test Card
        number=1,            # Changed from 0 (must be 1-14 for minor arcana)
        suit="wands",        # Must be a valid CardSuit enum value
        keywords=["test"],   # Required field
        upright_meaning="Test upright",     # Required field
        reversed_meaning="Test reversed"    # Required field
    )
    assert card.name == "The Magician"

@pytest.mark.unit
def test_card_creation_with_all_fields(sample_card_data):
    """Test card creation with all fields"""
    card = TarotCard(**sample_card_data)
    assert card.name == "Test Card"
    assert card.number == 0
    assert card.suit == "Test Suit"
    assert card.keywords == ["test"]
    assert card.upright_meaning == "Test upright"
    assert card.reversed_meaning == "Test reversed"

@pytest.mark.unit
def test_card_to_dict(sample_card):
    """Test card to_dict method"""
    card_dict = sample_card.to_dict()
    assert isinstance(card_dict, dict)
    assert card_dict["name"] == "Test Card"
    assert card_dict["number"] == 0
    assert card_dict["suit"] == "Test Suit"

@pytest.mark.unit
def test_card_get_element(sample_card):
    """Test card get_element method"""
    assert sample_card.get_element() == "Test Suit"

@pytest.mark.unit
def test_card_validation():
    """Test card validation"""
    with pytest.raises(ValueError):
        TarotCard(
            name="Invalid Card",
            number=-1,  # Invalid number
            suit="Test Suit"
        )
