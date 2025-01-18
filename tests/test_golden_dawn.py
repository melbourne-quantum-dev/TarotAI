import pytest
from pathlib import Path
from tarotai.extensions.enrichment.knowledge.golden_dawn import GoldenDawnKnowledgeBase
from tarotai.ai.clients.providers.voyage import VoyageClient

@pytest.fixture
def test_pdf():
    return Path("tests/data/test_golden_dawn.pdf")

@pytest.fixture
def voyage_client():
    return VoyageClient()

def test_knowledge_base_initialization(test_pdf, voyage_client):
    """Test that GoldenDawnKnowledgeBase initializes correctly"""
    # Test with Voyage client
    knowledge_base = GoldenDawnKnowledgeBase(str(test_pdf), voyage_client)
    assert knowledge_base is not None
    assert hasattr(knowledge_base, 'knowledge')
    assert hasattr(knowledge_base, 'embeddings')
    
    # Test without Voyage client
    knowledge_base = GoldenDawnKnowledgeBase(str(test_pdf))
    assert knowledge_base is not None
    assert hasattr(knowledge_base, 'knowledge')
