# src/tarotai/extensions/enrichment/clients/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAIClient(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model."""
        pass

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        pass

    @abstractmethod
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from the AI model."""
        pass

    @abstractmethod
    async def prefix_prompt(
        self, 
        prompt: str, 
        prefix: str, 
        no_prefix: bool = False
    ) -> str:
        """Generate a response with a prefix constraint."""
        pass

    @abstractmethod
    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str
    ) -> str:
        """Generate a conversational response."""
        pass
