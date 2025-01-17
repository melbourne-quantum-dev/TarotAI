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
from typing import Dict, Any, List
import json

from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (
    GoldenDawnKnowledgeBase,
    save_knowledge
)
from src.tarotai.core.config import get_config
from src.tarotai.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

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

async def process_golden_dawn(pdf_path: Path) -> Dict[str, Any]:
    """Main processing function for Golden Dawn PDF"""
    try:
        logger.info(f"Starting Golden Dawn PDF processing: {pdf_path}")
        
        # Initialize knowledge base
        golden_dawn = GoldenDawnKnowledgeBase(pdf_path)
        
        # Get processed knowledge
        knowledge = golden_dawn.knowledge.dict()
        
        # Generate embeddings
        embeddings = golden_dawn.embeddings
        
        # Prepare output data
        output = {
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "source_file": str(pdf_path),
                "version": "2.0.0"
            },
            "knowledge": knowledge,
            "embeddings": embeddings
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
        
        # Process PDF
        result = await process_golden_dawn(pdf_path)
        
        # Save results
        save_knowledge(result, output_path)
        logger.info(f"Successfully saved processed knowledge to {output_path}")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
