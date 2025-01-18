"""
AI client implementations and initialization for various providers
"""
from .base import BaseAIClient  # Changed from ..core
from .unified import UnifiedAIClient
from .providers.deepseek_v3 import DeepSeekClient  # Updated path
from .providers.claude import ClaudeClient    # Updated path
from .providers.voyage import VoyageClient
from ...config.schemas.config import get_config  # Use relative import

__all__ = [
    'BaseAIClient',
    'DeepSeekClient',
    'VoyageClient',
    'ClaudeClient',
    'UnifiedAIClient',
    'initialize_ai_clients'
]

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
