import logging
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, List, Optional


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
    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from the AI model"""
        pass


class BaseEmbeddingClient(BaseAIClient):
    """Base class for clients that primarily handle embeddings"""
    
    def __init__(self):
        super().__init__()
        self.embedding_dim = 1024
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_characters": 0,
            "errors": 0
        }

    async def generate_batch_embeddings(
        self, 
        texts: List[str], 
        **kwargs
    ) -> List[List[float]]:
        """Default batch embedding implementation"""
        return [await self.generate_embedding(text, **kwargs) for text in texts]

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return self.usage_stats


class BaseChatClient(BaseAIClient):
    """Base class for chat-based AI clients"""
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.system_prompt = "You are a helpful assistant."
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """Handle conversation history and system prompts"""
        if system_prompt is None:
            system_prompt = self.system_prompt
            
        messages.insert(0, {"role": "system", "content": system_prompt})
        return await self.generate_response(messages)

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        return self.usage_stats
