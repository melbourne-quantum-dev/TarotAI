"""
Golden Dawn PDF Processing Script

This script handles:
1. PDF content extraction
2. Knowledge structuring
3. Integration with TarotAI system

Version: 2.0.0
Last Updated: 2025-01-17
"""

import asyncio
from pathlib import Path
import logging
import os
from typing import Dict, Any, List
from src.tarotai.core.card_processor import CardProcessor
from src.tarotai.core.ai_clients import initialize_ai_clients
from src.tarotai.config.schemas.config import get_config
from src.tarotai.core.logging import setup_logging
from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (
    extract_pdf_content,
    save_knowledge
)

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

async def enhanced_process_golden_dawn(
    pdf_path: Path,
    ai_clients: Dict[str, Any],
    card_processor: CardProcessor
) -> Dict[str, Any]:
    """Enhanced processing with AI client optimization"""
    try:
        logger.info(f"Starting enhanced Golden Dawn processing: {pdf_path}")
        
        # Extract knowledge using Claude
        pdf_content = extract_pdf_content(pdf_path)
        gd_knowledge = await ai_clients["claude"].extract_structured_knowledge(pdf_content)
        
        # Process cards
        cards = gd_knowledge.get("cards", [])
        processed_cards = []
        
        for card in cards:
            try:
                # Generate meanings and embeddings
                card = await card_processor.generate_meanings(card, gd_knowledge)
                card = await card_processor.generate_embeddings(card)
                processed_cards.append(card)
            except Exception as e:
                logger.error(f"Error processing card {card.get('name')}: {str(e)}")
                processed_cards.append(card)  # Keep original card data
        
        return {
            "cards": processed_cards,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "ai_models_used": list(ai_clients.keys())
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to process Golden Dawn PDF: {str(e)}")
        raise

async def main():
    """Main execution function"""
    try:
        # Check required API keys
        required_keys = {
            "DEEPSEEK_API_KEY": "DeepSeek meaning generation", 
            "ANTHROPIC_API_KEY": "Claude knowledge extraction",
            "VOYAGE_API_KEY": "Voyage embeddings"
        }
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}\n"
                f"Please set these environment variables:\n"
                + "\n".join(f"- {key}: {required_keys[key]}" for key in missing_keys)
            )
            
        # Get configuration
        config = get_config()
        
        # Define paths
        pdf_path = config.tarot.data_dir / "golden_dawn.pdf"
        output_path = config.tarot.data_dir / "knowledge_cache" / "golden_dawn_processed.json"
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize clients
        ai_clients = initialize_ai_clients()
        card_processor = CardProcessor(ai_clients["deepseek"], ai_clients["voyage"])
        
        # Process PDF
        result = await enhanced_process_golden_dawn(
            pdf_path, 
            ai_clients,
            card_processor
        )
        
        # Save results
        save_knowledge(result, output_path)
        logger.info(f"Successfully saved processed knowledge to {output_path}")
        
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
