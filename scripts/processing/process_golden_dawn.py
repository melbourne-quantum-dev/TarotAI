#!/usr/bin/env python3
"""
Golden Dawn Knowledge Processing Script
Extracts and structures knowledge from the Golden Dawn PDF source.
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# AI client imports
from tarotai.ai.clients import initialize_ai_clients
from tarotai.config import get_config
from tarotai.core.errors import ProcessingError

# Core imports
from tarotai.core.logging import setup_logging

# Enrichment imports
from tarotai.extensions.enrichment.knowledge.golden_dawn import (
    extract_pdf_content,
    save_knowledge,
)
from tarotai.extensions.enrichment.knowledge.image_processor import (
    GoldenDawnImageProcessor,
)

# Setup logging
logger = setup_logging()

async def enhanced_process_golden_dawn(
    pdf_path: Path,
    ai_clients: Dict[str, Any],
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Enhanced processing pipeline for Golden Dawn knowledge extraction.
    
    Args:
        pdf_path: Path to the Golden Dawn PDF
        ai_clients: Dictionary of initialized AI clients
        output_dir: Optional output directory (defaults to pdf_path.parent/processed)
    
    Returns:
        Dict containing structured knowledge and processing metadata
    """
    try:
        logger.info(f"Starting enhanced Golden Dawn processing: {pdf_path}")
        
        if output_dir is None:
            output_dir = pdf_path.parent / "processed"
            output_dir.mkdir(exist_ok=True)
            
        # Extract textual knowledge
        logger.info("Extracting textual knowledge...")
        knowledge = extract_pdf_content(pdf_path)
        
        # Save knowledge base
        knowledge_path = output_dir / "golden_dawn_knowledge.json"
        save_knowledge(knowledge, knowledge_path)
        logger.info(f"Saved knowledge base to {knowledge_path}")
        
        # Process images if Voyage client is available
        image_results = None
        if "voyage" in ai_clients:
            logger.info("Processing images with Voyage...")
            image_processor = GoldenDawnImageProcessor(ai_clients["voyage"])
            image_results = await image_processor.process_pdf_images(
                pdf_path,
                output_dir
            )
            logger.info(f"Processed {image_results['num_images']} images")
        else:
            logger.warning("Voyage client not available - skipping image processing")
        
        # Combine results
        output = {
            "knowledge": knowledge.dict(),
            "images": image_results,
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "version": "2.1.0",
                "pdf_path": str(pdf_path),
                "output_dir": str(output_dir)
            }
        }
        
        # Save combined results
        results_path = output_dir / "golden_dawn_results.json"
        with open(results_path, "w") as f:
            json.dump(output, f, indent=2)
        logger.info(f"Saved combined results to {results_path}")
        
        return output
        
    except Exception as e:
        logger.error(f"Error in enhanced processing: {str(e)}")
        raise ProcessingError(f"Golden Dawn processing failed: {str(e)}")

async def main():
    """Main entry point"""
    try:
        # Load configuration
        config = get_config()
        
        # Initialize AI clients
        ai_clients = await initialize_ai_clients()
        
        # Set paths
        pdf_path = Path(config.data_dir) / "sources" / "golden_dawn.pdf"
        output_dir = Path(config.data_dir) / "processed" / "golden_dawn"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Process Golden Dawn knowledge
        results = await enhanced_process_golden_dawn(
            pdf_path=pdf_path,
            ai_clients=ai_clients,
            output_dir=output_dir
        )
        
        logger.info("Golden Dawn processing completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
