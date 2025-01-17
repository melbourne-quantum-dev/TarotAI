from PyPDF2 import PdfReader
from typing import List, Dict, Optional
import os
import json
from pathlib import Path
from tqdm import tqdm
from voyageai import get_embedding
from dotenv import load_dotenv
from pydantic import BaseModel
from ..exceptions import EnrichmentError

class GoldenDawnReadingMethod(BaseModel):
    name: str
    description: str
    steps: List[str]
    positions: List[str]
    notes: Optional[str] = None

class HistoricalApproach(BaseModel):
    reader: str
    era: str
    approach: str
    key_insights: List[str]
    notes: Optional[str] = None

class GoldenDawnLore(BaseModel):
    topic: str
    description: str
    symbolism: List[str]
    references: List[str]
    notes: Optional[str] = None

class GoldenDawnKnowledge(BaseModel):
    reading_methods: Dict[str, GoldenDawnReadingMethod]
    historical_approaches: Dict[str, HistoricalApproach]
    lore: Dict[str, GoldenDawnLore]
    optimal_practices: List[str]
    miscellaneous: Dict[str, str]

load_dotenv()

def extract_pdf_content(pdf_path: str) -> GoldenDawnKnowledge:
    """Extract structured content from the Golden Dawn PDF."""
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    try:
        reader = PdfReader(pdf_path)
        knowledge = GoldenDawnKnowledge(
            reading_methods={},
            historical_approaches={},
            lore={},
            optimal_practices=[],
            miscellaneous={}
        )

        print(f"Processing {pdf_path}...")
        for page in tqdm(reader.pages, total=len(reader.pages)):
            text = page.extract_text()
            if not text:
                continue

            # Extract reading methods
            if "Reading Method:" in text:
                method_name = text.split("Reading Method:")[1].split("\n")[0].strip()
                method_description = text.split("Description:")[1].split("\n")[0].strip()
                steps = [step.strip() for step in text.split("Steps:")[1].split("\n") if step.strip()]
                positions = [pos.strip() for pos in text.split("Positions:")[1].split("\n") if pos.strip()]
                knowledge.reading_methods[method_name] = GoldenDawnReadingMethod(
                    name=method_name,
                    description=method_description,
                    steps=steps,
                    positions=positions
                )

            # Extract historical approaches
            if "Historical Approach:" in text:
                reader_name = text.split("Reader:")[1].split("\n")[0].strip()
                era = text.split("Era:")[1].split("\n")[0].strip()
                approach = text.split("Approach:")[1].split("\n")[0].strip()
                key_insights = [insight.strip() for insight in text.split("Key Insights:")[1].split("\n") if insight.strip()]
                knowledge.historical_approaches[reader_name] = HistoricalApproach(
                    reader=reader_name,
                    era=era,
                    approach=approach,
                    key_insights=key_insights
                )

            # Extract lore
            if "Lore:" in text:
                topic = text.split("Topic:")[1].split("\n")[0].strip()
                description = text.split("Description:")[1].split("\n")[0].strip()
                symbolism = [symbol.strip() for symbol in text.split("Symbolism:")[1].split("\n") if symbol.strip()]
                references = [ref.strip() for ref in text.split("References:")[1].split("\n") if ref.strip()]
                knowledge.lore[topic] = GoldenDawnLore(
                    topic=topic,
                    description=description,
                    symbolism=symbolism,
                    references=references
                )

            # Extract optimal practices
            if "Optimal Practice:" in text:
                practices = [p.strip() for p in text.split("Optimal Practice:")[1].split("\n") if p.strip()]
                knowledge.optimal_practices.extend(practices)

            # Extract miscellaneous content
            if "Miscellaneous:" in text:
                key = text.split("Miscellaneous:")[1].split("\n")[0].strip()
                value = "\n".join([line.strip() for line in text.split("\n")[1:] if line.strip()])
                knowledge.miscellaneous[key] = value

        print(f"Processed Golden Dawn knowledge from {len(reader.pages)} pages")
        return knowledge
    except Exception as e:
        raise ValueError(f"Failed to extract PDF content: {str(e)}")

class GoldenDawnKnowledgeBase:
    """Knowledge base for Golden Dawn tarot interpretations."""
    
    def __init__(self, pdf_path: str):
        cache_path = Path(pdf_path).with_suffix('.json')
        
        if cache_path.exists():
            print(f"Loading cached knowledge base from {cache_path}")
            self.knowledge = load_knowledge(cache_path)
        else:
            self.knowledge = extract_pdf_content(pdf_path)
            print(f"Saving knowledge base cache to {cache_path}")
            save_knowledge(self.knowledge, cache_path)
                
        self.embeddings = self._generate_embeddings()
        self.card_index = self._create_card_index()
        self.version = "2.1.0"
        self._setup_validation_rules()
        
    def _setup_validation_rules(self):
        """Setup validation rules for Golden Dawn knowledge"""
        self.validation_rules = {
            "required_fields": [
                "title", "symbolism", "reading_methods"
            ],
            "allowed_symbols": [
                "Wand", "Cup", "Sword", "Pentacle",
                "Flame", "Water", "Air", "Earth"
            ],
            "max_reading_methods": 5
        }
    
    def _create_card_index(self) -> Dict[str, Dict]:
        """Create a quick lookup index for card information"""
        index = {}
        for method in self.knowledge.reading_methods.values():
            for card_ref in method.card_references:
                index[card_ref.card_name] = card_ref.details
        return index
    
    def get_card_info(self, card_name: str) -> Dict:
        """Get Golden Dawn knowledge for a specific card"""
        return self.card_index.get(card_name, {
            "title": "",
            "symbolism": [],
            "reversed_notes": "",
            "shadow_aspects": []
        })
    
    def get_reading_methods(self, card_name: str) -> List[Dict]:
        """Get reading methods that reference this card"""
        return [
            method for method in self.knowledge.reading_methods.values()
            if any(ref.card_name == card_name for ref in method.card_references)
        ]

def save_knowledge(knowledge: GoldenDawnKnowledge, output_path: Path) -> None:
    """Save Golden Dawn knowledge to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(knowledge.dict(), f, indent=2, ensure_ascii=False)

def load_knowledge(input_path: Path) -> GoldenDawnKnowledge:
    """Load Golden Dawn knowledge from a JSON file."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return GoldenDawnKnowledge(**data)
        
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
