from tarotai.core.card import TarotCard

def test_minimal_card_creation():
    """Test card creation with minimal required fields"""
    card = TarotCard(
        name="Test Card",
        number=0,
        suit="Test Suit"
    )
    assert card.name == "Test Card"
    assert card.number == 0
    assert card.suit == "Test Suit"
