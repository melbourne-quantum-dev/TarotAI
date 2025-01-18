# Add at the top of interpreter.py
from pathlib import Path

import logging
from typing import Any, Dict, List, Tuple, Optional

from tarotai.ai.clients.unified import UnifiedAIClient
from .agents import AgentManager, InterpretationError
from tarotai.config.schemas.config import AISettings, get_config
from tarotai.core.models.types import CardMeaning, QuestionContext


class ModelRouter:
    """Routes requests to appropriate models"""
    def __init__(self, config: AISettings):
        self.config = config
        self.clients = UnifiedAIClient(config)
        self.model_map = {
            "embedding": "voyage-2",
            "interpretation": config.interpretation_model,
            "enrichment": config.enrichment_model
        }
        
    async def route_request(self, task_type: str, **kwargs) -> Any:
        """Route requests to appropriate model"""
        model = self.model_map.get(task_type)
        if not model:
            raise ValueError(f"Unknown task type: {task_type}")
            
        if task_type == "embedding":
            return await self.clients.generate_embedding(kwargs["text"])
        else:
            return await self.clients.generate_response(
                kwargs["prompt"],
                model=model
            )

class TarotInterpreter:
    def __init__(self, config: AISettings):
        self.interpretation_cache: Dict[str, Any] = {}
        self.logger = self._setup_logging()
        self.config = config
        self.stage_limits = config.interpretation_limits
        self.agent_manager = AgentManager(config)

    def _setup_logging(self) -> logging.Logger:
        """Configure logging system using module name"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load interpreter configuration"""
        try:
            config = get_config()
            return {
                'interpretation_style': config.tarot.interpretation.style,
                'max_cache_size': config.tarot.interpretation.max_cache_size,
                'prompt_template_dir': config.tarot.interpretation.prompt_template_dir,
                'include_reversed': config.tarot.interpretation.include_reversed
            }
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            return {
                'interpretation_style': 'standard',
                'max_cache_size': 100,
                'prompt_template_dir': 'prompts',
                'include_reversed': True
            }
        
    def _build_context_summary(self, context: Optional[QuestionContext]) -> str:
        """Build a summary of the reading context"""
        if not context:
            return "No additional context provided"
            
        summary = []
        
        if context.user_profile:
            profile = context.user_profile
            summary.append(
                f"Reading for {profile.name or 'querent'} "
                f"who prefers {profile.reading_style} interpretations "
                f"with {profile.detail_level} detail level"
            )
            
        if context.temporal_context:
            summary.append(
                f"Current temporal context: {context.temporal_context}"
            )
            
        if context.reading_history:
            recent_readings = len(context.reading_history)
            summary.append(
                f"Querent has {recent_readings} recent readings in history"
            )
            
        return "\n".join(summary)
        
    async def interpret_reading(
        self,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str] = None,
        context: Optional[QuestionContext] = None
    ) -> str:
        """Generate interpretation using agent system and prompt templates"""
        try:
            # Get prompt template
            from tarotai.ai.clients.registry import ProviderRegistry
            prompt = ProviderRegistry.render_prompt(
                "tarot_interpretation",
                cards=[{
                    "name": card.name,
                    "reversed": reversed,
                    "golden_dawn": card.golden_dawn
                } for card, reversed in cards],
                question=question or "General reading",
                context=self._build_context_summary(context)
            )
            
            result = await self.agent_manager.interpret_reading(
                cards=[{
                    "name": card.name,
                    "reversed": reversed,
                    "golden_dawn": card.golden_dawn
                } for card, reversed in cards],
                context={
                    "question": question or "General reading",
                    "user_context": self._build_context_summary(context),
                    "prompt": prompt
                }
            )
            
            if not result["validation"]["valid"]:
                raise InterpretationError(
                    "Invalid interpretation",
                    errors=result["validation"]["errors"]
                )
                
            return result["interpretation"]["cards"]
            
        except Exception as e:
            self.logger.error(f"Interpretation failed: {str(e)}")
            raise
