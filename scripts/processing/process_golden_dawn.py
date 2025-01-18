# scripts/processing/process_golden_dawn.py                                                                                      
"""Process Golden Dawn PDF and extract structured knowledge."""
import json
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from PyPDF2 import PdfReader
from tqdm import tqdm

from tarotai.extensions.enrichment.knowledge.golden_dawn import (
    GoldenDawnKnowledge,
    GoldenDawnKnowledgeBase,
    GoldenDawnReadingMethod,
    HistoricalApproach,
    GoldenDawnLore,
)
from tarotai.ai.clients.providers.voyage import VoyageClient

load_dotenv()


async def process_golden_dawn_pdf(pdf_path: Path, output_dir: Path) -> Dict[str, Path]:
    """Process the Golden Dawn PDF and save structured knowledge.

    This must be run before generate_meanings.py as it creates the required
    knowledge base files that are dependencies for card interpretation.

    Args:
        pdf_path: Path to the Golden Dawn PDF file.
        output_dir: Directory to save processed files.

    Returns:
        Dictionary of output file paths with keys:
        - knowledge: Path to golden_dawn_knowledge.json
        - images: Path to golden_dawn_images.json
        - embeddings: Path to golden_dawn_embeddings.json

    Raises:
        FileNotFoundError: If the PDF file is not found.
        RuntimeError: If processing fails at any stage
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"Golden Dawn PDF not found at {pdf_path}")

    # Initialize AI clients
    voyage_client = VoyageClient()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize knowledge base
    knowledge_base = GoldenDawnKnowledgeBase(str(pdf_path), voyage_client)

    # If there's an image processing task, await it
    if hasattr(knowledge_base, '_image_processing_task'):
        knowledge_base.image_embeddings = await knowledge_base._image_processing_task

    # Add validation before saving
    for card in knowledge_base.knowledge.cards:
        if not card.get("title"):
            card["title"] = f"Golden Dawn Interpretation of {card['name']}"
        if not card.get("symbolism"):
            card["symbolism"] = []
        if not card.get("reading_methods"):
            card["reading_methods"] = []

    # Save processed data
    output_files = {
        "knowledge": output_dir / "golden_dawn_knowledge.json",
        "images": output_dir / "golden_dawn_images.json",
        "embeddings": output_dir / "golden_dawn_embeddings.json",
    }

    # Save knowledge
    with open(output_files["knowledge"], "w") as f:
        json.dump(knowledge_base.knowledge.dict(), f, indent=2)

    # Save image data if available
    if hasattr(knowledge_base, "image_embeddings"):
        with open(output_files["images"], "w") as f:
            json.dump(knowledge_base.image_embeddings, f, indent=2)

    # Save embeddings
    with open(output_files["embeddings"], "w") as f:
        json.dump(
            {
                "text_embeddings": knowledge_base.embeddings,
                "version": knowledge_base.version,
            },
            f,
            indent=2,
        )

    return output_files


async def main():
    """Main function for processing Golden Dawn PDF."""
    # Paths
    pdf_path = Path("data/golden_dawn.pdf")
    output_dir = Path("data/processed/golden_dawn")
    
    # Verify PDF exists
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"Golden Dawn PDF not found at {pdf_path}. "
            "Please ensure the PDF is in the data directory."
        )
        
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing Golden Dawn PDF at {pdf_path}...")
    print("This process may take several minutes depending on the PDF size.")
    
    try:
        output_files = await process_golden_dawn_pdf(pdf_path, output_dir)
        print("\nProcessing complete! Output files created:")
        for name, path in output_files.items():
            print(f"- {name}: {path}")
        print("\nYou can now run generate_meanings.py to create card interpretations.")
    except Exception as e:
        print(f"\nError processing PDF: {str(e)}")
        print("Please ensure:")
        print("1. The PDF exists at data/golden_dawn.pdf")
        print("2. You have sufficient disk space")
        print("3. Your environment variables are properly configured")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
