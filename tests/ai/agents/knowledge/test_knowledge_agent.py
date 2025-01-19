import pytest
import json
from pathlib import Path
from scripts.processing.process_golden_dawn import process_golden_dawn_pdf

@pytest.fixture
def test_pdf():
    return Path("tests/data/test_golden_dawn.pdf")

@pytest.fixture
def output_dir():
    return Path("tests/output")

@pytest.mark.asyncio
async def test_pdf_processing(test_pdf, output_dir):
    """Test the full PDF processing pipeline"""
    output_files = await process_golden_dawn_pdf(test_pdf, output_dir)
    
    # Verify output files were created
    assert output_files["knowledge"].exists()
    assert output_files["embeddings"].exists()
    
    # Verify file contents
    with open(output_files["knowledge"]) as f:
        knowledge = json.load(f)
        assert "reading_methods" in knowledge
        assert "historical_approaches" in knowledge
        
    with open(output_files["embeddings"]) as f:
        embeddings = json.load(f)
        assert "text_embeddings" in embeddings
        assert "version" in embeddings
