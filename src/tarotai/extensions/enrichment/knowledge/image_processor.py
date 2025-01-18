import io
import json
from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF
from PIL import Image

from tarotai.ai.clients.providers.voyage import VoyageClient
from tarotai.core.errors import EnrichmentError


class GoldenDawnImageProcessor:
    """Processes and stores Golden Dawn PDF images with multimodal embeddings"""
    
    def __init__(self, voyage_client: VoyageClient):
        self.voyage_client = voyage_client
        self.image_cache: Dict[str, Dict[str, Any]] = {}
        self.embedding_cache: Dict[str, List[float]] = {}
        
    async def extract_images(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract images from PDF with metadata"""
        if not pdf_path.exists():
            raise EnrichmentError(f"PDF file not found: {pdf_path}")
            
        try:
            doc = fitz.open(pdf_path)
            image_data = {}
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images(full=True)
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Convert to PIL Image
                    pil_img = Image.open(io.BytesIO(image_bytes))
                    
                    # Store image metadata
                    image_key = f"page_{page_num+1}_img_{img_index+1}"
                    image_data[image_key] = {
                        "page": page_num + 1,
                        "dimensions": pil_img.size,
                        "format": base_image["ext"],
                        "colorspace": base_image["colorspace"],
                        "dpi": base_image.get("dpi", 72),
                        "image": pil_img  # Store PIL image for processing
                    }
                    
            return image_data
        except Exception as e:
            raise EnrichmentError(f"Failed to extract images: {str(e)}")
            
    async def generate_image_embeddings(self, image_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate multimodal embeddings for extracted images"""
        embeddings = {}
        
        for img_key, img_meta in image_data.items():
            content = [
                {
                    "type": "text",
                    "text": f"Golden Dawn symbolism from page {img_meta['page']}"
                },
                {
                    "type": "image",
                    "image": img_meta["image"]
                }
            ]
            
            embedding = await self.voyage_client.generate_multimodal_embedding(
                content,
                image_quality="medium",
                max_image_size=1024
            )
            
            embeddings[img_key] = {
                "embedding": embedding,
                "metadata": {
                    "page": img_meta["page"],
                    "dimensions": img_meta["dimensions"],
                    "format": img_meta["format"],
                    "colorspace": img_meta["colorspace"],
                    "dpi": img_meta["dpi"]
                }
            }
            
        return embeddings
        
    async def process_pdf_images(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Full processing pipeline for PDF images"""
        image_data = await self.extract_images(pdf_path)
        embeddings = await self.generate_image_embeddings(image_data)
        
        output_path = output_dir / "golden_dawn_image_embeddings.json"
        with open(output_path, "w") as f:
            json.dump(embeddings, f, indent=2)
            
        return {
            "status": "success",
            "num_images": len(embeddings),
            "output_path": str(output_path)
        }
