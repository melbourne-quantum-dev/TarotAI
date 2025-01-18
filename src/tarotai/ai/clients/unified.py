from typing import Dict, Any, Optional, List
from ...config import AISettings
from .base import BaseAIClient
from ...ai.clients.providers.voyage import VoyageClient
from .providers.deepseek import DeepSeekClient
from .providers.anthropic import AnthropicClient
from .providers.openai import OpenAIClient

class UnifiedAIClient:
    """Unified interface for multiple AI providers"""
    
    def __init__(self, config: AISettings):
        self.clients = {
            "voyage": VoyageClient(config.voyage_model),
            "deepseek": DeepSeekClient(config.deepseek_model),
            "anthropic": AnthropicClient(config.anthropic_model),
            "openai": OpenAIClient(config.openai_model)
        }
        self.default_client = self.clients[config.default_provider]
        
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        return await self.default_client.generate_response(prompt, **kwargs)
        
    async def generate_embedding(self, text: str) -> List[float]:
        return await self.clients["voyage"].generate_embedding(text)
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        return await self.default_client.json_prompt(prompt)