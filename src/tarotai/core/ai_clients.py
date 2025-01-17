"""
Centralized AI client initialization

Handles:
- Client setup
- API key management
- Client configuration

Version: 2.0.0
Last Updated: 2025-01-17
"""

from src.tarotai.ai.clients.deepseek_v3 import DeepSeekClient
from src.tarotai.ai.clients.claude import ClaudeClient
from src.tarotai.ai.embeddings.voyage import VoyageClient
from src.tarotai.config.schemas.config import get_config

def initialize_ai_clients():
    """Initialize and configure all AI clients"""
    config = get_config()
    
    clients = {
        "deepseek": DeepSeekClient(
            api_key=config.ai_providers["deepseek"].api_key,
            model=config.ai_providers["deepseek"].model,
            temperature=config.ai_providers["deepseek"].temperature,
            max_tokens=config.ai_providers["deepseek"].max_tokens,
            timeout=config.ai_providers["deepseek"].timeout
        ),
        "claude": ClaudeClient(
            api_key=config.ai_providers["anthropic"].api_key,
            model=config.ai_providers["anthropic"].model,
            temperature=config.ai_providers["anthropic"].temperature,
            max_tokens=config.ai_providers["anthropic"].max_tokens,
            timeout=config.ai_providers["anthropic"].timeout
        ),
        "voyage": VoyageClient(
            api_key=config.ai_providers["voyage"].api_key
        )
    }
    
    return clients
