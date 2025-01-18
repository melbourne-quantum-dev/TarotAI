from typing import Any, Dict, List

from tarotai.ai.clients.base import BaseAIClient
from tarotai.ai.clients.providers.claude import ClaudeClient
from tarotai.ai.clients.providers.deepseek_v3 import DeepSeekClient
from tarotai.ai.clients.providers.voyage import VoyageClient
from tarotai.config.schemas.config import AISettings


class UnifiedAIClient:
    """Unified interface for multiple AI providers"""
    
    def __init__(self, config: AISettings):
        self.clients = {
            "voyage": VoyageClient(config.voyage_model),
            "deepseek": DeepSeekClient(config.deepseek_model),
            "anthropic": ClaudeClient(config.anthropic_model)
        }
        self.default_client = self.clients[config.default_provider]
        
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        return await self.default_client.generate_response(prompt, **kwargs)
        
    async def generate_embedding(self, text: str) -> List[float]:
        return await self.clients["voyage"].generate_embedding(text)
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        return await self.default_client.json_prompt(prompt)
