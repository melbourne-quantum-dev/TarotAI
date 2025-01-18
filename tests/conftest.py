import pytest

from tarotai.config.schemas.config import get_config
from tarotai.core.models.card import TarotCard
from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import CardSuit


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
        name="The Fool",
        number=0,
        suit=CardSuit.MAJOR,  # Use enum value
        keywords=["test"],
        upright_meaning="Test upright",
        reversed_meaning="Test reversed"
    )

@pytest.fixture
def sample_card_data():
    return {
        "name": "The Fool",
        "number": 0,
        "suit": CardSuit.MAJOR.value,
        "keywords": ["test"],
        "upright_meaning": "Test upright",
        "reversed_meaning": "Test reversed"
    }

@pytest.fixture
def sample_reading_data():
    return {
        "id": "test-reading",
        "cards": [{
            "name": "The Fool",
            "number": 0,
            "suit": "major",
            "keywords": ["test"],
            "upright_meaning": "Test upright",
            "reversed_meaning": "Test reversed"
        }],
        "interpretation": "Test interpretation",
        "model": "test-model",
        "context": {
            "question": "Test",
            "focus": "Test",
            "raw_question": "Test"
        },
        "reading_type": "GENERAL",
        "spread_type": "SINGLE",
        "is_reversed": [False]
    }
