# src/tarotai/extensions/enrichment/clients/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIClient(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model."""
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        pass