# Add at the top of interpreter.py
from pathlib import Path

import logging
from typing import Any, Dict, List, Tuple

from tarotai.ai.clients.providers.voyage import VoyageClient
from tarotai.ai.clients.unified import UnifiedAIClient
from tarotai.ai.prompts.templates import PromptTemplateManager
from tarotai.ai.rag.manager import RAGManager as RAGSystem
from tarotai.config.schemas.config import AISettings, get_config
from tarotai.core.models.types import CardMeaning, QuestionContext


class ModelRouter:
    """Routes requests to appropriate models"""
    def __init__(self, config: AISettings):
        self.config = config
        self.clients = UnifiedAIClient(config)
        
    async def route_request(self, task_type: str, **kwargs) -> Any:
        """Route requests to appropriate model"""
        if task_type == "embedding":
            return await self.clients.generate_embedding(kwargs["text"])
        elif task_type == "interpretation":
            return await self.clients.generate_response(
                kwargs["prompt"],
                model=self.config.interpretation_model
            )
        elif task_type == "enrichment":
            return await self.clients.generate_response(
                kwargs["prompt"],
                model=self.config.enrichment_model
            )

class TarotInterpreter:
    def __init__(self, config: AISettings):
        self.interpretation_cache: Dict[str, Any] = {}
        self.logger = self._setup_logging()
        self.config = config
        self.stage_limits = config.interpretation_limits
        self.prompt_templates = PromptTemplateManager()
        self.model_router = ModelRouter(config)
        self.rag = RAGSystem(
            voyage_client=VoyageClient(config.voyage_model),
            ai_client=UnifiedAIClient(config)
        )

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
        """Generate interpretation using PromptTemplateManager"""
        try:
            # Get the interpretation template
            template = self.prompt_templates.get_template("tarot_interpretation")
            
            # Format cards for template
            formatted_cards = "\n".join(
                f"{i+1}. {card.name} ({'Reversed' if reversed else 'Upright'})"
                for i, (card, reversed) in enumerate(cards)
            )
            
            # Build context summary
            context_summary = self._build_context_summary(context)
            
            # Get Golden Dawn context
            gd_context = "\n".join(
                f"{card[0].name} Golden Dawn Symbolism: {card[0].golden_dawn.get('symbolism', [])}"
                for card in cards
            )
            
            # Fill template with variables
            filled_template = template.fill(
                cards=formatted_cards,
                question=question or "General reading",
                context=context_summary,
                golden_dawn_context=gd_context
            )
            
            # Get RAG context
            card_names = [card[0].name for card in cards]
            rag_context = await self.rag.retrieve_context(
                f"Interpret this tarot reading using Golden Dawn methods: {', '.join(card_names)}"
            )
            
            # Generate interpretation
            response = await self.model_router.route_request(
                "interpretation",
                prompt=f"{filled_template}\n\nAdditional Context:\n{rag_context}"
            )
            
            return response if isinstance(response, str) else str(response)
            
        except Exception as e:
            self.logger.error(f"Interpretation failed: {str(e)}")
            raise
