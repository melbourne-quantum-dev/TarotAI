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
    return [0.1] * 1024

@pytest.fixture
def vector_store():
    store = VectorStore()
    # Add some test readings
    for i in range(10):
        reading = Reading(
            id=f"test-{i}",
            cards=[CardMeaning(
                name="The Fool",
                number=0,
                suit="major",
                arcana_type="major",
                is_reversed=True,
                keywords=["beginnings", "innocence"],
                upright_meaning="Test upright",
                reversed_meaning="Test reversed"
            )],
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
        embedding = [float(i)] * 1024
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
    assert len(results) == 5
    assert results[0][0].id == "target"

def test_embedding_manager_initialization(tmp_path):
    manager = EmbeddingManager(tmp_path)
    assert manager.version == 1
    assert len(manager.card_embeddings) == 0

def test_card_embeddings_serialization():
    embeddings = CardEmbeddings(
        text_embedding=[0.1] * 1024,
        image_embedding=[0.2] * 1024,
        version="2.0"
    )
    assert len(embeddings.text_embedding) == 1024
    assert embeddings.version == "2.0"
