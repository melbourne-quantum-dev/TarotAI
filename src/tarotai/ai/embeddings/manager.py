import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from tarotai.core.models.types import CardEmbeddings, CardMeaning
from tarotai.extensions.enrichment.knowledge.golden_dawn import GoldenDawnKnowledgeBase


@dataclass
class CardEmbeddings:
    """Multi-vector embeddings for a tarot card"""
    meaning_embedding: List[float]
    symbolism_embedding: List[float]
    contextual_embedding: List[float]
    version: int = 1

class EmbeddingManager:
    """Manages card and reading embeddings with version control and validation"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.version = 1
        self.card_embeddings: Dict[str, CardEmbeddings] = {}
        self._setup_validation_rules()
        
    def _setup_validation_rules(self):
        """Setup validation rules for embeddings"""
        self.validation_rules = {
            "embedding_size": 768,
            "required_fields": ["meaning_embedding", "symbolism_embedding"],
            "allowed_versions": [1, 2]
        }
        
    async def update_golden_dawn_embeddings(
        self,
        knowledge_base: GoldenDawnKnowledgeBase
    ) -> Dict[str, Dict]:
        """Update embeddings from Golden Dawn knowledge base"""
        golden_dawn_embeddings = {}
        
        # Get text embeddings
        text_embeddings = await knowledge_base._generate_text_embeddings()
        for embedding in text_embeddings:
            key = f"golden_dawn_{embedding['metadata']['type']}_{embedding['metadata']['name']}"
            golden_dawn_embeddings[key] = {
                "embedding": embedding["embedding"],
                "metadata": embedding["metadata"]
            }
            
        # Get image embeddings if available
        if hasattr(knowledge_base, 'image_embeddings'):
            image_embeddings = await knowledge_base._generate_image_embeddings()
            for embedding in image_embeddings:
                key = f"golden_dawn_image_{embedding['metadata']['name']}"
                golden_dawn_embeddings[key] = {
                    "embedding": embedding["embedding"],
                    "metadata": embedding["metadata"]
                }
                
        return golden_dawn_embeddings
        
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
