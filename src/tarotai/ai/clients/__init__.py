"""AI client implementations and initialization"""
from .base import BaseAIClient
from .providers.claude import ClaudeClient
from .providers.deepseek_v3 import DeepSeekClient
from .providers.voyage import VoyageClient
from .unified import UnifiedAIClient


def initialize_ai_clients():
    """Initialize and configure all AI clients"""
    from tarotai.config.schemas.config import get_config
    config = get_config()
    return UnifiedAIClient(config).clients

__all__ = [
    'BaseAIClient',
    'DeepSeekClient',
    'VoyageClient',
    'ClaudeClient',
    'UnifiedAIClient',
    'initialize_ai_clients'
]