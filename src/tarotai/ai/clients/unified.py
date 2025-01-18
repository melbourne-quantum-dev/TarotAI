"""Unified AI client interface"""
from typing import Any, Dict, List

from tarotai.config.schemas.config import AISettings

from .providers.claude import ClaudeClient
from .providers.deepseek_v3 import DeepSeekClient
from .providers.voyage import VoyageClient


class UnifiedAIClient:
    """Unified interface for multiple AI providers"""
    
    def __init__(self, config: AISettings):
        """Initialize with configuration settings"""
        self.clients = {
            "voyage": VoyageClient(
                api_key=config.api_key
            ),
            "deepseek": DeepSeekClient(
                api_key=config.api_key,
                model=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout
            ),
            "anthropic": ClaudeClient(
                api_key=config.api_key,
                model=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                timeout=config.timeout
            )
        }
        self.default_client = self.clients["deepseek"]

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using the default client"""
        return await self.default_client.generate_response(prompt, **kwargs)
        
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using the Voyage client"""
        return await self.clients["voyage"].generate_embedding(text)
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate structured JSON response using the default client"""
        return await self.default_client.json_prompt(prompt)
