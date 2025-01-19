import pytest
from pathlib import Path
from tarotai.extensions.enrichment.knowledge.golden_dawn import GoldenDawnKnowledgeBase

@pytest.fixture
def golden_dawn_knowledge():
    return GoldenDawnKnowledgeBase(Path("data/golden_dawn.pdf"))

@pytest.mark.asyncio
async def test_golden_dawn_loading(golden_dawn_knowledge):
    """Test loading Golden Dawn knowledge base"""
    assert golden_dawn_knowledge is not None
    assert len(golden_dawn_knowledge.cards) > 0

@pytest.mark.asyncio
async def test_golden_dawn_card_parsing(golden_dawn_knowledge):
    """Test parsing of individual cards"""
    card = golden_dawn_knowledge.cards[0]
    assert card.name is not None
    assert card.keywords is not None
    assert len(card.keywords) > 0

@pytest.mark.asyncio
async def test_golden_dawn_invalid_path():
    """Test handling of invalid PDF path"""
    with pytest.raises(FileNotFoundError):
        GoldenDawnKnowledgeBase(Path("invalid_path.pdf"))
