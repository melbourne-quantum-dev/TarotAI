from pathlib import Path
import logging
import httpx
from typing import List, Tuple, Dict, Optional, Generator, Any, cast
from abc import ABC, abstractmethod
from .types import CardMeaning, SpreadType, Reading, SpreadPosition, QuestionContext
from .prompts import MultiStagePrompt, PromptStage
from .reading import ReadingInput
from .config import get_config, AISettings
from .clients.voyage import VoyageClient
from .clients.deepseek import DeepSeekClient
from .clients.anthropic import AnthropicClient
from .clients.openai import OpenAIClient
from .rag import RAGSystem

class BaseAIClient(ABC):
    """Base interface for AI clients"""
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]: ...
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]: ...
    
    @abstractmethod
    async def json_prompt(self, prompt: str) -> Dict[str, Any]: ...

class OllamaClient(BaseAIClient):
    """Client for local Ollama models"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = httpx.AsyncClient(base_url=base_url)
        
    async def generate_response(self, prompt: str, model: str = "llama2", **kwargs) -> Dict[str, Any]:
        response = await self.session.post(
            "/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                **kwargs
            }
        )
        return response.json()
        
    async def generate_embedding(self, text: str, model: str = "llama2") -> List[float]:
        response = await self.session.post(
            "/api/embeddings",
            json={
                "model": model,
                "prompt": text
            }
        )
        return response.json()["embedding"]
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        response = await self.generate_response(
            f"Return JSON only for: {prompt}",
            format="json"
        )
        return response

class UnifiedAIClient:
    """Unified interface for multiple AI providers"""
    
    def __init__(self, config: AISettings):
        self.clients = {
            "voyage": VoyageClient(config.voyage_model),
            "deepseek": DeepSeekClient(config.deepseek_model),
            "anthropic": AnthropicClient(config.anthropic_model),
            "openai": OpenAIClient(config.openai_model),
            "ollama": OllamaClient() if config.ollama_enabled else None
        }
        self.default_client = self.clients[config.default_provider]
        
    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        return await self.default_client.generate_response(prompt, **kwargs)
        
    async def generate_embedding(self, text: str) -> List[float]:
        return await self.clients["voyage"].generate_embedding(text)
        
    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        return await self.default_client.json_prompt(prompt)

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
        self.prompt_templates = self._load_prompt_templates()
        self.model_router = ModelRouter(config)
        self.rag = RAGSystem(
            voyage_client=VoyageClient(config.voyage_model),
            ai_client=UnifiedAIClient(config)
        )

    def _setup_logging(self) -> logging.Logger:
        """Configure logging system"""
        logger = logging.getLogger("tarot_interpreter")
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter and add to handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(ch)
        return logger
        
    def _load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load interpreter configuration"""
        try:
            return {
                'interpretation_style': get_config("tarot.interpretation.style"),
                'max_cache_size': get_config("tarot.interpretation.max_cache_size"),
                'prompt_template_dir': get_config("tarot.interpretation.prompt_template_dir"),
                'include_reversed': get_config("tarot.interpretation.include_reversed")
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
        
        # User profile
        if context.user_profile:
            profile = context.user_profile
            summary.append(
                f"Reading for {profile.name or 'querent'} "
                f"who prefers {profile.reading_style} interpretations "
                f"with {profile.detail_level} detail level"
            )
            
        # Temporal context
        if context.temporal_context:
            summary.append(
                f"Current temporal context: {context.temporal_context}"
            )
            
        # Reading history
        if context.reading_history:
            recent_readings = len(context.reading_history)
            summary.append(
                f"Querent has {recent_readings} recent readings in history"
            )
            
        return "\n".join(summary)

    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates from XML files"""
        # TODO: Implement template loading
        return {
            'interpretation': """<interpretation>
                <spread>{spread_type}</spread>
                <cards>{cards}</cards>
                <question>{question}</question>
            </interpretation>"""
        }
        
    def _create_interpretation_prompt(
        self, 
        spread_type: str,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str],
        context: Optional[QuestionContext] = None,
        chain_of_thought: bool = True
    ) -> MultiStagePrompt:
        """Create context-aware interpretation prompt"""
        # Build context summary
        context_summary = self._build_context_summary(context)
        
        # Format cards with positions
        formatted_cards = "\n".join(
            f"{i+1}. {card.name} ({'Reversed' if reversed else 'Upright'})"
            for i, (card, reversed) in enumerate(cards)
        )
        stages = []
        
        if chain_of_thought:
            stages.append(PromptStage(
                name="chain_of_thought",
                system_message="Think step by step about the reading",
                user_message=f"""
                Let's analyze this reading step by step:
                
                1. First, identify the key components of the question: {question}
                2. Then, consider the spread type: {spread_type}
                3. Analyze each card's meaning in context:
                   {formatted_cards}
                4. Consider the overall context:
                   {context_summary}
                5. Finally, synthesize the interpretation
                """
            ))
            
        stages.extend([
            PromptStage(
                name="context_analysis",
                system_message="Analyze the reading context and identify key themes",
                user_message=f"""
                Spread Type: {spread_type}
                Question: {question}
                Cards: {formatted_cards}
                
                Context Summary:
                {context_summary}
                
                Identify 3-5 key themes in this reading considering:
                1. The specific question and context
                2. Patterns from previous readings
                3. Card combinations and positions
                4. User's stated focus area
                """
            ),
            PromptStage(
                name="card_analysis",
                system_message="Analyze each card's meaning in context",
                user_message="""
                For each card, provide:
                - Core meaning
                - Position significance
                - Relation to other cards
                - Practical implications
                """
            ),
            PromptStage(
                name="synthesis",
                system_message="Synthesize the reading into a coherent interpretation",
                user_message="""
                Combine the card analyses into a unified interpretation.
                Focus on practical advice and actionable insights.
                """
            )
        ])

    def show_static_meanings(self, cards: List[Tuple[CardMeaning, bool]]) -> str:
        """Display static card meanings before interpretation"""
        meanings = []
        for card, is_reversed in cards:
            meaning = card.reversed_meaning if is_reversed else card.upright_meaning
            meanings.append(
                f"{card.name} ({'Reversed' if is_reversed else 'Upright'}):\n{meaning}"
            )
        return "\n\n".join(meanings)

    def interpret_reading(
        self,
        input_method: ReadingInput,
        question: Optional[str] = None,
        show_static: bool = True
    ) -> Generator[Dict[str, Any], None, None]:
        """Enhanced interpretation flow"""
        # Get cards from input method
        cards = input_method.get_cards()
        
        # Show static meanings if requested
        if show_static:
            static_meanings = self.show_static_meanings(cards)
            yield {"type": "static_meanings", "content": static_meanings}
            
        # Generate interpretation
        interpretation = self._generate_interpretation(cards, question)
        yield {"type": "interpretation", "content": interpretation}

    async def _generate_interpretation(
        self,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str] = None
    ) -> str:
        """Generate interpretation for a reading using model router and RAG"""
        self.logger.info("Starting interpretation")
        
        try:
            # Build structured prompt
            prompt = self._create_interpretation_prompt("custom", cards, question)
            self.logger.debug(f"Using prompt: {prompt}")
            
            # Retrieve relevant context using RAG
            card_names = [card[0].name for card in cards]
            context = await self.rag.retrieve_context(
                f"Interpret this tarot reading: {', '.join(card_names)}"
            )
            
            # Generate interpretation using model router with RAG context
            response = await self.model_router.route_request(
                "interpretation",
                prompt=f"{prompt}\n\nContext:\n{context}"
            )
            
            # Process response
            if isinstance(response, dict):
                return response.get("text", str(response))
            return str(response)
            
        except Exception as e:
            self.logger.error(f"Interpretation failed: {str(e)}")
            raise
