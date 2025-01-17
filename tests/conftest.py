import pytest
from pathlib import Path
from tarotai.core.deck import TarotDeck
from tarotai.core.config import get_config
from tarotai.core.card import TarotCard

@pytest.fixture(scope="session")
def config():
    return get_config()

@pytest.fixture
def test_deck(config):
    test_data = config.tarot.data_dir / "test_cards.json"
    if not test_data.exists():
        pytest.skip("Test data file not found")
    return TarotDeck(test_data)

@pytest.fixture
def empty_deck(config):
    return TarotDeck(config.tarot.data_dir / "empty.json")

@pytest.fixture
def sample_card():
    return TarotCard(
        name="Test Card",
        number=0,
        suit="Test Suit",
        keywords=["test"],
        upright_meaning="Test upright",
        reversed_meaning="Test reversed"
    )

@pytest.fixture
def sample_card_data():
    return {
        "name": "Test Card",
        "number": 0,
        "suit": "Test Suit",
        "keywords": ["test"],
        "upright_meaning": "Test upright",
        "reversed_meaning": "Test reversed"
    }
