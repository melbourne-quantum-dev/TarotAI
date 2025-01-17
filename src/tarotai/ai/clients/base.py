from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, AsyncGenerator
import logging

class BaseAIClient(ABC):
    """Base interface for all AI clients"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"ai_client.{self.__class__.__name__}")
        
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the AI model"""
        pass
        
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for text"""
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
        
    @abstractmethod
    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from the AI model"""
        pass
