import pytest
from tarotai.core.vector_store import VectorStore
from tarotai.core.embedding_manager import EmbeddingManager, CardEmbeddings
from tarotai.core.types import Reading, CardMeaning
from pathlib import Path

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
            cards=[("Test Card", True)],
            interpretation=f"Test interpretation {i}",
            model="test-model"
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
        cards=[("Target Card", False)],
        interpretation="Target interpretation",
        model="test-model"
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
        meaning_embedding=[0.1] * 1024,
        symbolism_embedding=[0.2] * 1024,
        contextual_embedding=[0.3] * 1024,
        version=2
    )
    assert len(embeddings.meaning_embedding) == 1024
    assert embeddings.version == 2
