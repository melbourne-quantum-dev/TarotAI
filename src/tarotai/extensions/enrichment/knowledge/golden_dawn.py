from PyPDF2 import PdfReader
from typing import List, Dict, Optional
import os
import pickle
from pathlib import Path
from tqdm import tqdm
from voyageai import get_embedding
from dotenv import load_dotenv
from ..exceptions import EnrichmentError

load_dotenv()

def extract_pdf_content(pdf_path: str) -> List[Dict[str, str]]:
    """Extract structured content from PDF"""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        sections = []
        
        print(f"Processing {pdf_path}...")
        for i, page in tqdm(enumerate(reader.pages), total=len(reader.pages)):
            text = page.extract_text()
            if text:
                sections.append({
                    "page": i + 1,
                    "content": text,
                    "metadata": {
                        "source": "Golden Dawn Book",
                        "chapter": "Unknown"
                    }
                })
        
        print(f"Processed {len(sections)} sections from {len(reader.pages)} pages")
        return sections
    except Exception as e:
        raise ValueError(f"Failed to extract PDF content: {str(e)}")

class GoldenDawnKnowledgeBase:
    """Knowledge base for Golden Dawn tarot interpretations."""
    
    def __init__(self, pdf_path: str):
        cache_path = Path(pdf_path).with_suffix('.pkl')
        
        if cache_path.exists():
            print(f"Loading cached knowledge base from {cache_path}")
            with open(cache_path, 'rb') as f:
                self.sections = pickle.load(f)
        else:
            self.sections = extract_pdf_content(pdf_path)
            print(f"Saving knowledge base cache to {cache_path}")
            with open(cache_path, 'wb') as f:
                pickle.dump(self.sections, f)
                
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
