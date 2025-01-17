"""
DEPRECATED - This functionality has been moved to process_golden_dawn.py

Golden Dawn PDF Processing Script

This script handles:
1. PDF content extraction
2. Knowledge structuring
3. Embedding generation
4. Cache management
5. Integration with TarotAI system
"""

import asyncio
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass
import numpy as np
from pydantic import BaseModel, validator

from src.tarotai.ai.prompts.templates import UPRIGHT_PROMPT, REVERSED_PROMPT
from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (
    GoldenDawnKnowledgeBase,
    save_knowledge
)
from src.tarotai.core.config import get_config
from src.tarotai.ai.embeddings.voyage import VoyageClient  # Assuming this is the correct import path
from src.tarotai.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

@dataclass
class CardEmbeddings:
    """Manages card meaning embeddings"""
    dimension: int = 1024
    embeddings: Dict[str, List[float]] = None
    _validate_cache: Dict[str, bool] = None

    def __post_init__(self):
        self.embeddings = {}
        self._validate_cache = {}

    async def generate_card_embeddings(self, card: Dict[str, Any], voyage_client) -> Dict[str, List[float]]:
        """Generate comprehensive embeddings for a card"""
        base_text = self._prepare_embedding_text(card)
        
        embeddings = {
            "base": await voyage_client.generate_embedding(base_text),
            "upright": await voyage_client.generate_embedding(card["upright_meaning"]),
            "reversed": await voyage_client.generate_embedding(card["reversed_meaning"]),
            "combined": await self._generate_combined_embedding(card, voyage_client)
        }
        
        self._validate_embeddings(embeddings)
        return embeddings

    def _prepare_embedding_text(self, card: Dict[str, Any]) -> str:
        """Prepare text for embedding generation"""
        return f"{card['name']} {card['traditional_title']} {' '.join(card['keywords'])}"

    def _validate_embeddings(self, embeddings: Dict[str, List[float]]) -> None:
        """Validate embedding structure and dimensions"""
        for name, embedding in embeddings.items():
            assert len(embedding) == self.dimension, f"Invalid dimension for {name}"
            self._validate_cache[name] = True

class KnowledgeProcessor:
    """Processes and validates card knowledge"""
    
    def __init__(self, embedding_manager: CardEmbeddings):
        self.embedding_manager = embedding_manager
        self.validation_rules = self._load_validation_rules()

    async def process_card(self, card: Dict[str, Any], voyage_client) -> Dict[str, Any]:
        """Process complete card knowledge"""
        try:
            self._validate_card_structure(card)
            
            card["embeddings"] = await self.embedding_manager.generate_card_embeddings(
                card, voyage_client
            )
            
            card["metadata"].update({
                "processed_at": datetime.now().isoformat(),
                "embedding_version": "2.0.0"
            })
            
            return card
            
        except Exception as e:
            logger.error(f"Error processing card {card.get('name')}: {str(e)}")
            raise

    def _validate_card_structure(self, card: Dict[str, Any]) -> None:
        """Validate card data structure"""
        required_fields = [
            "name", "number", "keywords", 
            "upright_meaning", "reversed_meaning"
        ]
        
        for field in required_fields:
            assert field in card, f"Missing required field: {field}"

class KnowledgeValidator:
    """Validation framework for processed knowledge"""
    
    def validate_card(self, card: Dict[str, Any]) -> bool:
        """Comprehensive card validation"""
        try:
            self._validate_structure(card)
            self._validate_content_quality(card)
            self._validate_embeddings(card.get("embeddings", {}))
            return True
        except Exception as e:
            logger.error(f"Validation failed: {str(e)}")
            return False
            
    def _validate_content_quality(self, card: Dict[str, Any]) -> None:
        """Validate content meets quality standards"""
        assert len(card["upright_meaning"]) >= 50, "Upright meaning too short"
        assert len(card["reversed_meaning"]) >= 50, "Reversed meaning too short"
        assert 3 <= len(card["keywords"]) <= 7, "Invalid keyword count"
        
    def _validate_embeddings(self, embeddings: Dict[str, Any]) -> None:
        """Validate embedding structure and quality"""
        required_embeddings = ["base", "upright", "reversed", "combined"]
        for emb in required_embeddings:
            assert emb in embeddings, f"Missing required embedding: {emb}"
            assert isinstance(embeddings[emb], list), f"Invalid embedding format for {emb}"
            assert len(embeddings[emb]) == 1024, f"Invalid embedding dimension for {emb}"

async def generate_keywords(card: Dict, ai_client, gd_info: Dict) -> List[str]:
    """Generate keywords for a card using AI and Golden Dawn knowledge"""
    prompt = f"""
    Generate 3-5 keywords for {card['name']} considering:
    - Element: {card['element']}
    - Astrological: {card['astrological']}
    - Kabbalistic: {card['kabbalistic']}
    - Golden Dawn Symbolism: {gd_info.get('symbolism', [])}
    - Traditional Meanings: {gd_info.get('traditional_meanings', [])}
    
    Return as JSON list.
    """
    return await ai_client.json_prompt(prompt)

async def generate_meanings(card: Dict[str, Any], ai_client, golden_dawn: GoldenDawnKnowledgeBase) -> Dict[str, Any]:
    """Generate upright and reversed meanings for a card."""
    # Prepare context variables
    context = {
        "card_name": card["name"],
        "element": card["element"],
        "astrological": card["astrological"],
        "kabbalistic": card["kabbalistic"],
        "golden_dawn_title": golden_dawn.get_card_info(card["name"]).get("title", "")
    }
    
    # Generate keywords if missing
    if not card.get("keywords"):
        card["keywords"] = await generate_keywords(card, ai_client, golden_dawn.get_card_info(card["name"]))
    
    # Generate meanings if missing
    if not card.get("upright_meaning"):
        prompt = UPRIGHT_PROMPT.format(**context)
        card["upright_meaning"] = await ai_client.generate_response(prompt)
    
    if not card.get("reversed_meaning"):
        prompt = REVERSED_PROMPT.format(**context)
        card["reversed_meaning"] = await ai_client.generate_response(prompt)
    
    # Add metadata
    card["metadata"] = {
        "last_updated": datetime.now().isoformat(),
        "source": "generated",
        "confidence": 0.95
    }
    
    return card

async def generate_embeddings(card: Dict[str, Any], voyage_client) -> Dict[str, Any]:
    """Generate embeddings for a card's meanings."""
    if not card.get("embeddings"):
        card["embeddings"] = {}
    
    if not card["embeddings"].get("upright"):
        card["embeddings"]["upright"] = await voyage_client.generate_embedding(card["upright_meaning"])
    
    if not card["embeddings"].get("reversed"):
        card["embeddings"]["reversed"] = await voyage_client.generate_embedding(card["reversed_meaning"])
    
    return card

async def process_cards(cards: List[Dict[str, Any]], ai_client, voyage_client, golden_dawn: GoldenDawnKnowledgeBase) -> List[Dict[str, Any]]:
    """Process all cards to generate meanings and embeddings."""
    processed_cards = []
    for card in cards:
        try:
            card = await generate_meanings(card, ai_client, golden_dawn)
            card = await generate_embeddings(card, voyage_client)
            processed_cards.append(card)
        except Exception as e:
            logger.error(f"Error processing card {card.get('name')}: {str(e)}")
            processed_cards.append(card)  # Keep the original card data
    return processed_cards

async def process_golden_dawn(pdf_path: Path, voyage_client) -> Dict[str, Any]:
    """Main processing function for Golden Dawn PDF"""
    try:
        logger.info(f"Starting Golden Dawn PDF processing: {pdf_path}")
        
        # Initialize knowledge base and embedding manager
        golden_dawn = GoldenDawnKnowledgeBase(pdf_path)
        embedding_manager = CardEmbeddings()
        knowledge_processor = KnowledgeProcessor(embedding_manager)
        
        # Get processed knowledge
        knowledge = golden_dawn.knowledge.dict()
        
        # Process each card with enhanced pipeline
        processed_cards = []
        for card in knowledge.get("cards", []):
            processed_card = await knowledge_processor.process_card(
                card, 
                voyage_client
            )
            processed_cards.append(processed_card)
        
        # Prepare output data
        output = {
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "source_file": str(pdf_path),
                "version": "2.0.0",
                "embedding_dimension": embedding_manager.dimension
            },
            "knowledge": {
                "cards": processed_cards,
                "correspondences": knowledge.get("correspondences", {})
            },
            "embeddings": {
                "card_count": len(processed_cards),
                "embedding_version": "2.0.0"
            }
        }
        
        return output
        
    except Exception as e:
        logger.error(f"Failed to process Golden Dawn PDF: {str(e)}")
        raise

async def main():
    """Main execution function"""
    try:
        # Get configuration
        config = get_config()
        data_dir = Path(config.data_dir)
        
        # Define paths
        pdf_path = data_dir / "golden_dawn.pdf"
        output_path = data_dir / "knowledge_cache" / "golden_dawn_processed.json"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize Voyage client
        voyage_client = VoyageClient()  # Assuming you have this import
        
        # Process PDF
        result = await process_golden_dawn(pdf_path, voyage_client)
        
        # Save results
        save_knowledge(result, output_path)
        logger.info(f"Successfully saved processed knowledge to {output_path}")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
