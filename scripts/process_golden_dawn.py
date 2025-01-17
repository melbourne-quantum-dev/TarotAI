"""
Golden Dawn PDF Processing Script

This script handles:
1. PDF content extraction
2. Knowledge structuring
3. Embedding generation
4. Cache management
5. Integration with TarotAI system

Version: 2.0.0
Last Updated: 2025-01-17
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
from src.tarotai.ai.clients.base import BaseAIClient
from src.tarotai.extensions.enrichment.knowledge.golden_dawn import extract_pdf_content

# Define expected fields for card validation
EXPECTED_FIELDS = [
    "name", "number", "suit", "element", 
    "astrological", "kabbalistic", "keywords",
    "upright_meaning", "reversed_meaning"
]

from src.tarotai.ai.prompts.templates import UPRIGHT_PROMPT, REVERSED_PROMPT
from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (
    GoldenDawnKnowledgeBase,
    save_knowledge
)
from pydantic import BaseModel, Field, validator
from pathlib import Path
from src.tarotai.core.config import get_config
from src.tarotai.core.logging import setup_logging
from src.tarotai.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

class GoldenDawnConfig(BaseModel):
    """Configuration specific to Golden Dawn processing"""
    voyage_api_key: str = Field(..., env="VOYAGE_API_KEY")
    data_dir: Path = Field(default=Path("data"))
    batch_size: int = Field(default=10, description="Number of cards to process per batch")
    
    @validator('data_dir')
    def validate_data_dir(cls, v):
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v

def get_golden_dawn_config() -> GoldenDawnConfig:
    """Get Golden Dawn specific configuration"""
    try:
        return GoldenDawnConfig()
    except Exception as e:
        logger.error(f"Failed to load Golden Dawn configuration: {str(e)}")
        raise
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

    async def generate_batch_embeddings(self, cards: List[Dict[str, Any]], voyage_client) -> Dict[str, Dict[str, List[float]]]:
        """Generate embeddings for multiple cards in batch"""
        # Prepare batch texts
        base_texts = [self._prepare_embedding_text(card) for card in cards]
        upright_texts = [card["upright_meaning"] for card in cards]
        reversed_texts = [card["reversed_meaning"] for card in cards]
        
        # Generate embeddings in parallel
        base_embeddings = await voyage_client.generate_batch_embedding(base_texts)
        upright_embeddings = await voyage_client.generate_batch_embedding(upright_texts)
        reversed_embeddings = await voyage_client.generate_batch_embedding(reversed_texts)
        
        # Combine results
        results = {}
        for i, card in enumerate(cards):
            embeddings = {
                "base": base_embeddings[i],
                "upright": upright_embeddings[i],
                "reversed": reversed_embeddings[i],
                "combined": await self._generate_combined_embedding(card, voyage_client)
            }
            self._validate_embeddings(embeddings)
            results[card["name"]] = embeddings
            
        return results

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

    async def process_batch(self, cards: List[Dict[str, Any]], voyage_client) -> List[Dict[str, Any]]:
        """Process multiple cards in batch"""
        try:
            # Validate all cards first
            for card in cards:
                self._validate_card_structure(card)
            
            # Generate embeddings in batch
            batch_embeddings = await self.embedding_manager.generate_batch_embeddings(
                cards, voyage_client
            )
            
            # Update cards with embeddings and metadata
            processed_cards = []
            for card in cards:
                card["embeddings"] = batch_embeddings[card["name"]]
                card["metadata"].update({
                    "processed_at": datetime.now().isoformat(),
                    "embedding_version": "2.0.0",
                    "batch_processed": True
                })
                processed_cards.append(card)
            
            return processed_cards
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            raise

    def _validate_card_structure(self, card: Dict[str, Any]) -> None:
        """Validate card data structure"""
        required_fields = [
            "name", "number", "keywords", 
            "upright_meaning", "reversed_meaning"
        ]
        
        for field in required_fields:
            assert field in card, f"Missing required field: {field}"

class EnhancedCardValidator:
    """Extended validation with AI-assisted checks"""
    
    def __init__(self, expected_fields: List[str]):
        self.expected_fields = expected_fields
        
    def validate_card(self, card: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive card validation"""
        validation = {
            "complete": True,
            "missing_fields": [],
            "issues": []
        }
        
        # Check for missing fields
        for field in self.expected_fields:
            if field not in card or not card[field]:
                validation["complete"] = False
                validation["missing_fields"].append(field)
                
        # Validate content quality
        if "upright_meaning" in card and len(card["upright_meaning"]) < 50:
            validation["issues"].append("Upright meaning too short")
        if "reversed_meaning" in card and len(card["reversed_meaning"]) < 50:
            validation["issues"].append("Reversed meaning too short")
        if "keywords" in card and not (3 <= len(card["keywords"]) <= 7):
            validation["issues"].append("Invalid keyword count")
            
        return validation
    
    async def validate_with_ai(self, card: Dict[str, Any], ai_client) -> Dict[str, Any]:
        """Perform AI-assisted validation"""
        validation = self.validate_card(card)
        
        if not validation["complete"]:
            # Use AI to suggest missing fields
            prompt = f"""
            Suggest values for missing fields in {card['name']}:
            {validation['missing_fields']}
            
            Consider:
            - Element: {card.get('element')}
            - Astrological: {card.get('astrological')}
            - Kabbalistic: {card.get('kabbalistic')}
            """
            
            suggestions = await ai_client.json_prompt(prompt)
            validation["suggestions"] = suggestions
        
        return validation

async def process_card_batch(
    cards: List[Dict[str, Any]],
    gd_knowledge: Dict[str, Any],
    ai_clients: Dict[str, BaseAIClient]
) -> List[Dict[str, Any]]:
    """Process batch of cards with optimized AI client usage"""
    
    # Use DeepSeek for meaning generation
    meaning_tasks = [
        ai_clients["deepseek"].generate_meaning_from_correspondences(card, gd_knowledge)
        for card in cards
    ]
    
    # Use Claude for structured knowledge extraction
    knowledge_tasks = [
        ai_clients["claude"].extract_structured_knowledge(card.get("raw_content", ""))
        for card in cards
    ]
    
    # Run in parallel
    meanings, knowledge = await asyncio.gather(
        asyncio.gather(*meaning_tasks),
        asyncio.gather(*knowledge_tasks)
    )
    
    # Update cards
    for i, card in enumerate(cards):
        card.update({
            "upright_meaning": meanings[i],
            "golden_dawn": knowledge[i]
        })
    
    return cards

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

async def enhanced_process_golden_dawn(
    pdf_path: Path,
    voyage_client,
    ai_clients: Dict[str, BaseAIClient]
) -> Dict[str, Any]:
    """Enhanced processing with AI client optimization"""
    try:
        logger.info(f"Starting enhanced Golden Dawn processing: {pdf_path}")
        
        # Extract knowledge using Claude
        pdf_content = extract_pdf_content(pdf_path)
        gd_knowledge = await ai_clients["claude"].extract_structured_knowledge(pdf_content)
        
        # Process cards in optimized batches
        cards = gd_knowledge.get("cards", [])
        processed_cards = await process_card_batch(cards, gd_knowledge, ai_clients)
        
        # Validate results
        validator = EnhancedCardValidator(EXPECTED_FIELDS)
        validation_results = await asyncio.gather(*[
            validator.validate_with_ai(card, ai_clients["deepseek"])
            for card in processed_cards
        ])
        
        # Generate embeddings
        embedding_manager = CardEmbeddings()
        for card in processed_cards:
            card["embeddings"] = await embedding_manager.generate_card_embeddings(
                card, voyage_client
            )
        
        return {
            "cards": processed_cards,
            "validation": validation_results,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "ai_models_used": list(ai_clients.keys()),
                "embedding_dimension": embedding_manager.dimension
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to process Golden Dawn PDF: {str(e)}")
        raise

async def main():
    """Main execution function"""
    try:
        # Get Golden Dawn specific configuration
        config = get_golden_dawn_config()
        
        # Define paths
        pdf_path = config.data_dir / "golden_dawn.pdf"
        output_path = config.data_dir / "knowledge_cache" / "golden_dawn_processed.json"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize Voyage client
        voyage_client = VoyageClient()  # Assuming you have this import
        
        # Process PDF
        # Initialize AI clients
        ai_clients = {
            "deepseek": DeepSeekClient(),
            "claude": ClaudeClient()
        }
        
        result = await enhanced_process_golden_dawn(
            pdf_path, 
            voyage_client,
            ai_clients
        )
        
        # Save results
        save_knowledge(result, output_path)
        logger.info(f"Successfully saved processed knowledge to {output_path}")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
