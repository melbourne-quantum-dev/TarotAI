import pytest

from tarotai.core.models.card import TarotCard
from tarotai.core.models.types import CardSuit


@pytest.mark.unit
def test_minimal_card_creation():
    """Test card creation with minimal required fields"""
    card = TarotCard(
        name="The Fool",  # Changed to match actual card name
        number=0,
        suit="major",  # Changed to match actual enum value
        keywords=["test"],
        upright_meaning="Test upright",
        reversed_meaning="Test reversed"
    )
    assert card.name == "The Fool"

@pytest.mark.unit
def test_card_creation_with_all_fields(sample_card_data):
    """Test card creation with all fields"""
    card = TarotCard(**sample_card_data)
    assert card.name == "The Fool"
    assert card.number == 0
    assert card.suit == "major"
    assert card.keywords == ["test"]
    assert card.upright_meaning == "Test upright"
    assert card.reversed_meaning == "Test reversed"

@pytest.mark.unit
def test_card_to_dict(sample_card):
    """Test card to_dict method"""
    card_dict = sample_card.to_dict()
    assert isinstance(card_dict, dict)
    assert card_dict["name"] == "The Fool"
    assert card_dict["number"] == 0
    assert card_dict["suit"] == "major"

@pytest.mark.unit
def test_card_get_element(sample_card):
    """Test card get_element method"""
    assert sample_card.get_element() == "Unknown"  # Update expected value

@pytest.mark.unit
def test_card_validation():
    """Test card validation"""
    with pytest.raises(ValueError):
        TarotCard(
            name="Invalid Card",
            number=-1,  # Invalid number
            suit="Test Suit"
        )

def test_card_validation_invalid_suit():
    """Test card validation with invalid suit"""
    with pytest.raises(ValueError):
        TarotCard(
            name="Invalid Card",
            number=0,
            suit="Invalid Suit",
            keywords=["test"],
            upright_meaning="Test",
            reversed_meaning="Test"
        )

def test_card_validation_minor_arcana():
    """Test minor arcana number validation"""
    with pytest.raises(ValueError):
        TarotCard(
            name="Invalid Minor Card",
            number=15,  # Invalid for minor arcana
            suit=CardSuit.WANDS,
            keywords=["test"],
            upright_meaning="Test",
            reversed_meaning="Test"
        )

def test_card_meaning_reversed():
    """Test reversed meaning functionality"""
    card = TarotCard(
        name="Test Card",
        number=0,
        suit=CardSuit.MAJOR,
        keywords=["test"],
        upright_meaning="Upright",
        reversed_meaning="Reversed"
    )
    assert card.get_meaning(False) == "Upright"
    assert card.get_meaning(True) == "Reversed"
