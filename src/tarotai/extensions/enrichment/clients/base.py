# src/tarotai/extensions/enrichment/clients/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAIClient(ABC):
    """Base interface for AI clients"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model."""
        
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        
    @abstractmethod
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from the AI model."""
        
    @abstractmethod
    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response."""
