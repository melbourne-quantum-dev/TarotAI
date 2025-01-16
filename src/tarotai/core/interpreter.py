from pathlib import Path
import logging
from typing import List, Tuple, Dict, Optional, Generator, Any, cast
from .types import CardMeaning, SpreadType, Reading, SpreadPosition
from .prompts import MultiStagePrompt, PromptStage
from .reading import ReadingInput
from .config import get_config

class TarotInterpreter:
    def __init__(self, config_path: Path = Path("config/interpreter.yaml")):
        self.interpretation_cache: Dict[str, Any] = {}
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.prompt_templates = self._load_prompt_templates()

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
        question: Optional[str]
    ) -> MultiStagePrompt:
        return MultiStagePrompt([
            PromptStage(
                name="context_analysis",
                system_message="Analyze the reading context and identify key themes",
                user_message=f"""
                Spread Type: {spread_type}
                Question: {question}
                Cards: {[c.name for c in cards]}
                Identify 3-5 key themes in this reading.
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

    def _generate_interpretation(
        self,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str] = None
    ) -> str:
        """Generate interpretation for a reading"""
        self.logger.info("Starting interpretation")
        
        try:
            # Build structured prompt
            prompt = self._create_interpretation_prompt("custom", cards, question)
            self.logger.debug(f"Using prompt: {prompt}")
            
            # Generate interpretation
            interpretation = []
            
            for i, (card, is_reversed) in enumerate(cards, start=1):
                meaning = card.reversed_meaning if is_reversed else card.upright_meaning
                interpretation.append(
                    f"Position {i} ({card.name}): {meaning}"
                )
                
            result = "\n".join(interpretation)
            self.logger.info("Interpretation completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Interpretation failed: {str(e)}")
            raise
