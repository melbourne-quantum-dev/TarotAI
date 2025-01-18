import pytest

from tarotai.ai.embeddings.manager import EmbeddingManager
from tarotai.ai.rag.vector_store import VectorStore
from tarotai.core.models.types import (
    CardEmbeddings,
    CardMeaning,
    QuestionContext,
    Reading,
    ReadingType,
    SpreadType,
)


@pytest.fixture
def mock_embedding():
    return [0.1] * 768  # Updated to match the embedding size in test deck

@pytest.fixture
def test_deck():
    """Load the generated test deck"""
    deck_path = Path("data/test_deck.json")
    if not deck_path.exists():
        pytest.skip("Test deck not found, run generate_test_deck.py first")
    
    with open(deck_path) as f:
        data = json.load(f)
    return [CardMeaning(**card) for card in data['cards']]

@pytest.fixture
def vector_store(test_deck):
    store = VectorStore()
    # Add test deck cards to the vector store
    for i, card in enumerate(test_deck):
        embedding = [float(i)] * 768  # Match the embedding size
        reading = Reading(
            id=f"test-{i}",
            cards=[card],
            interpretation=f"Test interpretation {i}",
            model="test-model",
            context=QuestionContext(
                question="Test question",
                focus="Test focus",
                raw_question="Test raw question"
            ),
            reading_type=ReadingType.GENERAL,
            spread_type=SpreadType.SINGLE,
            is_reversed=[False]
        )
        store.add_reading(reading, embedding)
    store.build_index()
    return store

def test_vector_store_add_reading(vector_store):
    assert len(vector_store.mapping) == 10
    assert vector_store.index.get_n_items() == 10

def test_vector_store_find_similar(vector_store, mock_embedding):
    # Add a target reading
    target_reading = Reading(
        id="target",
        cards=[CardMeaning(
            name="The Fool",
            number=0,
            suit="major",
            arcana_type="major",
            is_reversed=False,
            keywords=["beginnings", "innocence"],
            upright_meaning="Test upright",
            reversed_meaning="Test reversed"
        )],
        interpretation="Target interpretation",
        model="test-model",
        context=QuestionContext(
            question="Target question",
            focus="Target focus",
            raw_question="Target raw question"
        ),
        reading_type=ReadingType.GENERAL,
        spread_type=SpreadType.SINGLE,
        is_reversed=[False]
    )
    vector_store.add_reading(target_reading, mock_embedding)
    
    # Find similar
    results = vector_store.find_similar(mock_embedding)
    assert len(results) >= 1  # Changed to >= since we only care that target is in results
    assert any(result[0].id == "target" for result in results)  # Check if target is in results

def test_embedding_manager_initialization(tmp_path):
    manager = EmbeddingManager(tmp_path)
    assert manager.version == 1
    assert len(manager.card_embeddings) == 0

def test_card_embeddings_serialization(test_deck):
    # Test with a card from the generated deck
    card = test_deck[0]
    embeddings = CardEmbeddings(
        text_embedding=card.embeddings['upright'],
        image_embedding=card.embeddings['reversed'],
        version="2.0"
    )
    assert len(embeddings.text_embedding) == 768
    assert embeddings.version == "2.0"

def test_embedding_manager_generate_embedding(tmp_path):
    """Test generating embeddings"""
    manager = EmbeddingManager(tmp_path)
    embedding = manager.generate_embedding("Test text")
    assert len(embedding) == 768

def test_embedding_manager_save_embeddings(tmp_path):
    """Test saving embeddings"""
    manager = EmbeddingManager(tmp_path)
    manager.generate_embedding("Test text")
    manager.save_embeddings()
    assert (tmp_path / "embeddings.json").exists()

def test_vector_store_add_reading(vector_store):
    """Test adding a reading to the vector store"""
    assert len(vector_store.mapping) == 10
    assert vector_store.index.get_n_items() == 10

def test_vector_store_find_similar(vector_store, mock_embedding):
    """Test finding similar readings"""
    results = vector_store.find_similar(mock_embedding)
    assert len(results) >= 1
