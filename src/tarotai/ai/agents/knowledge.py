from typing import Dict, List, Optional
from .base import BaseAgent
from ..rag.manager import RAGManager
from ..embeddings.manager import EmbeddingManager

class KnowledgeAgent(BaseAgent):
    """Agent responsible for knowledge retrieval and enrichment."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rag_manager = RAGManager()
        self.embedding_manager = EmbeddingManager()

    async def process(self, query: str) -> Dict:
        """Process a knowledge query."""
        context = await self._get_rag_context(query)
        return await self._generate_response(query, context)

    async def _get_rag_context(self, query: str) -> str:
        """Get relevant context from RAG system."""
        return await self.rag_manager.get_context(query)

    async def _generate_response(self, query: str, context: str) -> Dict:
        """Generate a response using the AI client."""
        template = self.prompt_manager.get_template("knowledge_response.j2")
        prompt = template.render(query=query, context=context)
        return await self.ai_client.generate(prompt)