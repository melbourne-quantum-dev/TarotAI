from PyPDF2 import PdfReader
from typing import List, Dict, Optional
import os
from voyageai import get_embedding
from dotenv import load_dotenv
from ..exceptions import EnrichmentError

load_dotenv()

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    """Extract structured content from PDF"""
    if not os.path.exists(pdf_path):
        raise EnrichmentError(f"PDF file not found at {pdf_path}")
    
    reader = PdfReader(pdf_path)
    sections = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            sections.append({
                "page": i + 1,
                "content": text,
                "metadata": {
                    "source": "Golden Dawn Book",
                    "chapter": "Unknown"  # Can be enhanced with chapter detection
                }
            })
    
    return sections

class GoldenDawnKnowledgeBase:
    """Knowledge base for Golden Dawn tarot interpretations."""
    
    def __init__(self, pdf_path: str):
        self.sections = extract_pdf_content(pdf_path)
        self.embeddings = self._generate_embeddings()
        
    def _generate_embeddings(self) -> List[Dict]:
        """Generate embeddings for all sections"""
        embeddings = []
        voyage_key = os.getenv("VOYAGE_API_KEY")
        if not voyage_key:
            raise EnrichmentError("Voyage API key not found in environment variables.")
            
        for section in self.sections:
            embedding = get_embedding(
                section['content'],
                model="voyage-2",
                api_key=voyage_key
            )
            embeddings.append({
                "content": section['content'],
                "embedding": embedding,
                "metadata": section['metadata']
            })
        return embeddings

    def find_relevant_sections(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """Find most relevant sections using cosine similarity."""
        # TODO: Implement proper vector similarity search
        # For now return first few sections
        return self.embeddings[:top_k]
