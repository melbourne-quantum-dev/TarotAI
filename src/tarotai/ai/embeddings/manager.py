from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import json
from ..models.types import CardMeaning

@dataclass
class CardEmbeddings:
    """Multi-vector embeddings for a tarot card"""
    meaning_embedding: List[float]
    symbolism_embedding: List[float]
    contextual_embedding: List[float]
    version: int = 1

class EmbeddingManager:
    """Manages card and reading embeddings"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.version = 1
        self.card_embeddings: Dict[str, CardEmbeddings] = {}
        
    def load_embeddings(self) -> None:
        """Load saved embeddings from disk"""
        embeddings_file = self.data_dir / "card_embeddings.json"
        if embeddings_file.exists():
            with open(embeddings_file) as f:
                data = json.load(f)
                self.card_embeddings = {
                    k: CardEmbeddings(**v) 
                    for k, v in data.items()
                }
                
    def save_embeddings(self) -> None:
        """Save current embeddings to disk"""
        embeddings_file = self.data_dir / "card_embeddings.json"
        with open(embeddings_file, "w") as f:
            json.dump({
                k: v.__dict__ 
                for k, v in self.card_embeddings.items()
            }, f)
            
    async def update_card_embeddings(
        self,
        cards: List[CardMeaning],
        voyage_client
    ) -> Dict[str, CardEmbeddings]:
        """Generate or update embeddings for cards"""
        new_embeddings = {}
        for card in cards:
            # Generate multi-vector embeddings
            meaning_text = f"{card.upright_meaning} {card.reversed_meaning}"
            symbolism_text = f"{card.keywords} {card.element} {card.astrological}"
            context_text = f"{card.book_t_description} {card.golden_dawn_title}"
            
            new_embeddings[card.name] = CardEmbeddings(
                meaning_embedding=await voyage_client.generate_embedding(meaning_text),
                symbolism_embedding=await voyage_client.generate_embedding(symbolism_text),
                contextual_embedding=await voyage_client.generate_embedding(context_text),
                version=self.version
            )
            
        self.card_embeddings.update(new_embeddings)
        self.version += 1
        self.save_embeddings()
        return new_embeddings
