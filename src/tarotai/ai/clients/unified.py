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
                api_key=config.ai_providers["voyage"].api_key
            ),
            "deepseek": DeepSeekClient(
                api_key=config.ai_providers["deepseek"].api_key,
                model=config.ai_providers["deepseek"].model,
                temperature=config.ai_providers["deepseek"].temperature,
                max_tokens=config.ai_providers["deepseek"].max_tokens,
                timeout=config.ai_providers["deepseek"].timeout
            ),
            "anthropic": ClaudeClient(
                api_key=config.ai_providers["anthropic"].api_key,
                model=config.ai_providers["anthropic"].model,
                temperature=config.ai_providers["anthropic"].temperature,
                max_tokens=config.ai_providers["anthropic"].max_tokens,
                timeout=config.ai_providers["anthropic"].timeout
            )
        }
        self.default_client = self.clients[config.default_provider]

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using the default client"""
        return await self.default_client.generate_response(prompt, **kwargs)
        
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using the Voyage client"""
        return await self.clients["voyage"].generate_embedding(text)
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate structured JSON response using the default client"""
        return await self.default_client.json_prompt(prompt)