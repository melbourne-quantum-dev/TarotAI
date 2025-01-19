from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from ..clients.unified import UnifiedAIClient
from ..prompts.manager import PromptManager

class BaseAgent(ABC):
    """Base class for all AI agents in the system."""
    
    def __init__(self, ai_client: Optional[UnifiedAIClient] = None):
        self.ai_client = ai_client or UnifiedAIClient()
        self.prompt_manager = PromptManager()

    @abstractmethod
    async def process(self, *args, **kwargs):
        """Main processing method to be implemented by specific agents."""
        pass