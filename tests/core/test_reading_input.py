import pytest
from unittest.mock import AsyncMock
from tarotai.core.services.reading import ReadingInput, RandomDrawInput, ManualInput
from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import CardMeaning

@pytest.fixture
def mock_deck():
    deck = TarotDeck(Path("tests/data/test_cards.json"))
    return deck

@pytest.fixture
def mock_ai_client():
    return AsyncMock()

@pytest.fixture 
def mock_voyage_client():
    return AsyncMock()

class TestReadingInput(ReadingInput):
    """Concrete implementation for testing base class"""
    def get_cards(self):
        return [("Test Card", False)]

@pytest.mark.asyncio
async def test_analyze_combinations(mock_ai_client):
    """Test analyze_combinations method"""
    reading_input = TestReadingInput()
    result = await reading_input.analyze_combinations(mock_ai_client)
    
    mock_ai_client.generate_response.assert_called_once()
    assert isinstance(result, dict)

@pytest.mark.asyncio 
async def test_generate_embeddings(mock_voyage_client):
    """Test generate_embeddings method"""
    reading_input = TestReadingInput()
    result = await reading_input.generate_embeddings(mock_voyage_client)
    
    mock_voyage_client.generate_batch_embeddings.assert_called()
    assert result is not None

def test_random_draw_input(mock_deck):
    """Test RandomDrawInput implementation"""
    input = RandomDrawInput(mock_deck, 3)
    cards = input.get_cards()
    
    assert len(cards) == 3
    assert all(isinstance(card[0], CardMeaning) for card in cards)

def test_manual_input(mock_deck):
    """Test ManualInput implementation"""
    input = ManualInput(mock_deck, [("The Fool", False), ("The Magician", True)])
    cards = input.get_cards()
    
    assert len(cards) == 2
    assert cards[0][0].name == "The Fool"
    assert cards[1][0].name == "The Magician"
    assert cards[1][1] is True

def test_manual_input_invalid_card(mock_deck):
    """Test error handling for invalid cards"""
    with pytest.raises(ValueError):
        input = ManualInput(mock_deck, [("Invalid Card", False)])
        input.get_cards()
