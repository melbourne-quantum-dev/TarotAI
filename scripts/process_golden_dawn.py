"""
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
from typing import Dict, Any

from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (
    GoldenDawnKnowledgeBase,
    save_knowledge
)
from src.tarotai.core.config import get_config
from src.tarotai.core.logging import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

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
