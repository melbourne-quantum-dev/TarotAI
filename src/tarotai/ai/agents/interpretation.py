from typing import Dict, List
from .base import BaseAgent
from ..rag.manager import RAGManager

class InterpretationAgent(BaseAgent):
    """Agent responsible for tarot card interpretation."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rag_manager = RAGManager()

    async def process(self, cards: List[Dict], context: Optional[str] = None) -> Dict:
        """Generate interpretation for given cards."""
        enriched_context = await self._enrich_context(cards, context)
        return await self._generate_interpretation(cards, enriched_context)

    async def _enrich_context(self, cards: List[Dict], user_context: Optional[str]) -> str:
        """Enrich interpretation context with RAG data."""
        card_names = [card['name'] for card in cards]
        rag_context = await self.rag_manager.get_context(card_names)
        return f"{rag_context}\n{user_context}" if user_context else rag_context

    async def _generate_interpretation(self, cards: List[Dict], context: str) -> Dict:
        """Generate the final interpretation."""
        template = self.prompt_manager.get_template("reading_interpretation.j2")
        prompt = template.render(cards=cards, context=context)
        return await self.ai_client.generate(prompt)