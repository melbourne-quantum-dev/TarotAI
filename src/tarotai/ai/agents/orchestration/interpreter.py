from typing import Dict, List, Optional, Tuple, Any
from logging import Logger
import asyncio

from ..config import AISettings
from ..types import CardMeaning, QuestionContext
from ...ai.agents import InterpretationAgent, KnowledgeAgent, ValidationAgent
from ...ai.rag.manager import RAGManager
from ..cache import CacheManager

class TarotInterpreter:
    """High-level service for tarot reading interpretation."""

    def __init__(self, config: AISettings):
        self.config = config
        self.cache_manager = CacheManager()
        self.logger = self._setup_logging()
        
        # Initialize AI agents
        self.interpretation_agent = InterpretationAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.validation_agent = ValidationAgent()
        
        # Initialize RAG
        self.rag_manager = RAGManager()

    async def interpret_reading(
        self,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str] = None,
        context: Optional[QuestionContext] = None
    ) -> str:
        """
        Coordinate the interpretation of a tarot reading.
        
        Args:
            cards: List of (card, reversed) tuples
            question: Optional question being asked
            context: Additional context about the reading
        """
        cache_key = self._generate_cache_key(cards, question, context)
        
        # Check cache first
        if cached := await self.cache_manager.get(cache_key):
            self.logger.info(f"Cache hit for reading: {cache_key}")
            return cached

        try:
            # Prepare card data
            card_data = self._prepare_card_data(cards)
            
            # Validate card data
            validation_result = await self.validation_agent.process(card_data)
            if not validation_result['is_valid']:
                self.logger.warning(f"Card validation issues: {validation_result['errors']}")
                
            # Enrich with knowledge context
            knowledge_context = await self.knowledge_agent.process(
                cards=card_data,
                question=question
            )
            
            # Generate interpretation
            interpretation = await self.interpretation_agent.process(
                cards=card_data,
                question=question,
                context=self._build_context(context, knowledge_context)
            )
            
            # Cache successful interpretation
            await self.cache_manager.set(
                cache_key,
                interpretation,
                ttl=self.config.cache_ttl
            )
            
            return interpretation

        except Exception as e:
            self.logger.error(f"Interpretation failed: {str(e)}", exc_info=True)
            return await self._handle_interpretation_error(e)

    async def _handle_interpretation_error(self, error: Exception) -> str:
        """Handle interpretation errors gracefully."""
        try:
            # Attempt fallback interpretation
            return await self.interpretation_agent.process(
                error=error,
                template="error_handling.j2"
            )
        except Exception as e:
            self.logger.error(f"Fallback interpretation failed: {str(e)}")
            raise InterpretationError("Unable to generate reading interpretation")

    def _prepare_card_data(self, cards: List[Tuple[CardMeaning, bool]]) -> List[Dict]:
        """Prepare card data for AI processing."""
        return [
            {
                "name": card.name,
                "meaning": card.meaning,
                "reversed": reversed,
                "keywords": card.keywords,
                "position": idx + 1
            }
            for idx, (card, reversed) in enumerate(cards)
        ]

    def _build_context(self, user_context: Optional[QuestionContext], 
                      knowledge_context: Dict) -> Dict:
        """Build complete context for interpretation."""
        return {
            "user_context": user_context.dict() if user_context else {},
            "knowledge_context": knowledge_context,
            "system_context": {
                "confidence": knowledge_context.get("confidence", 0.0),
                "sources": knowledge_context.get("sources", []),
                "timestamp": datetime.now().isoformat()
            }
        }

    def _generate_cache_key(self, cards: List[Tuple[CardMeaning, bool]],
                          question: Optional[str],
                          context: Optional[QuestionContext]) -> str:
        """Generate unique cache key for reading."""
        card_hash = "-".join(f"{card.name}{'R' if rev else 'U'}" 
                           for card, rev in cards)
        return f"{card_hash}:{hash(question)}:{hash(str(context))}"

    def _setup_logging(self) -> Logger:
        """Setup service-specific logging."""
        logger = logging.getLogger(__name__)
        # Add service-specific handlers and formatting
        return logger

class InterpretationError(Exception):
    """Custom exception for interpretation failures."""
    pass