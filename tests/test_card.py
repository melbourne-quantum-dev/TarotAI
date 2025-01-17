from tarotai.core.card import TarotCard
from tarotai.core.types import CardMeaning

def test_card_creation():
    """Test basic card creation"""
    card = TarotCard(
        name="The Fool",
        number=0,
        suit="Major Arcana",
        keywords=["beginnings", "innocence"],
        upright_meaning="New beginnings, spontaneity",
        reversed_meaning="Foolishness, recklessness"
    )
    assert card.name == "The Fool"
    assert card.number == 0
    assert card.suit == "Major Arcana"

def test_card_to_dict():
    """Test card serialization to dictionary"""
    card = TarotCard(
        name="The Magician",
        number=1,
        suit="Major Arcana",
        keywords=["willpower", "creation"],
        upright_meaning="Manifestation, resourcefulness",
        reversed_meaning="Manipulation, poor planning"
    )
    card_dict = card.to_dict()
    assert isinstance(card_dict, dict)
    assert card_dict["name"] == "The Magician"
    assert "upright_meaning" in card_dict
