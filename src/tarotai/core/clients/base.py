from typing import Dict, Any, List, Optional, AsyncGenerator
from abc import ABC, abstractmethod

class BaseAIClient(ABC):
    """Base interface for AI clients"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model"""
        pass
        
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the input text"""
        pass
        
    @abstractmethod
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a structured JSON response"""
        pass
        
    @abstractmethod
    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response"""
        pass
