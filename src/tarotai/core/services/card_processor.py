"""
Centralized card processing logic

Handles:
- Meaning generation
- Embedding creation
- Validation
- Batch processing

Version: 2.0.0
Last Updated: 2025-01-17
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from tarotai.ai.clients.base import BaseAIClient
from tarotai.ai.clients.providers.voyage import VoyageClient

logger = logging.getLogger(__name__)

class CardProcessor:
    """Centralized card processing logic"""
    
    def __init__(self, ai_client: BaseAIClient, voyage_client: VoyageClient):
        self.ai_client = ai_client
        self.voyage_client = voyage_client

    async def generate_meanings(self, card: Dict[str, Any], golden_dawn: Dict[str, Any]) -> Dict[str, Any]:
        """Generate upright and reversed meanings for a card."""
        try:
            # Prepare context variables
            context = {
                "card_name": card["name"],
                "element": card["element"],
                "astrological": card["astrological"],
                "kabbalistic": card["kabbalistic"],
                "golden_dawn_title": golden_dawn.get("title", "")
            }
            
            # Generate keywords if missing
            if not card.get("keywords"):
                card["keywords"] = await self._generate_keywords(card, golden_dawn)
            
            # Generate meanings if missing
            if not card.get("upright_meaning"):
                card["upright_meaning"] = await self.ai_client.generate_response(
                    f"Generate upright meaning for {card['name']} considering: {context}"
                )
            
            if not card.get("reversed_meaning"):
                card["reversed_meaning"] = await self.ai_client.generate_response(
                    f"Generate reversed meaning for {card['name']} considering: {context}"
                )
            
            # Add metadata
            card["metadata"] = {
                "last_updated": datetime.now().isoformat(),
                "source": "generated",
                "confidence": 0.95
            }
            
            return card
            
        except Exception as e:
            logger.error(f"Error generating meanings for {card.get('name')}: {str(e)}")
            raise

    async def generate_embeddings(self, card: Dict[str, Any]) -> Dict[str, Any]:
        """Generate embeddings for a card's meanings."""
        try:
            if not card.get("embeddings"):
                card["embeddings"] = {}
            
            if not card["embeddings"].get("upright"):
                card["embeddings"]["upright"] = await self.voyage_client.generate_embedding(
                    card["upright_meaning"]
                )
            
            if not card["embeddings"].get("reversed"):
                card["embeddings"]["reversed"] = await self.voyage_client.generate_embedding(
                    card["reversed_meaning"]
                )
            
            return card
            
        except Exception as e:
            logger.error(f"Error generating embeddings for {card.get('name')}: {str(e)}")
            raise

    async def _generate_keywords(self, card: Dict[str, Any], golden_dawn: Dict[str, Any]) -> List[str]:
        """Generate keywords for a card using AI and Golden Dawn knowledge"""
        prompt = f"""
        Generate 3-5 keywords for {card['name']} considering:
        - Element: {card['element']}
        - Astrological: {card['astrological']}
        - Kabbalistic: {card['kabbalistic']}
        - Golden Dawn Symbolism: {golden_dawn.get('symbolism', [])}
        - Traditional Meanings: {golden_dawn.get('traditional_meanings', [])}
        
        Return as JSON list.
        """
        return await self.ai_client.json_prompt(prompt)
