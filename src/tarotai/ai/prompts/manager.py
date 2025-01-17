from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from ..types import CardMeaning

class PromptStage(BaseModel):
    """Represents a single stage in a multi-stage prompt"""
    name: str
    system_message: str
    user_message: str
    output_format: Optional[Dict[str, str]] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None

class MultiStagePrompt(BaseModel):
    """Container for multi-stage prompts"""
    stages: List[PromptStage]
    results: List[Dict[str, Any]] = []
    
    async def execute(self, ai_client, initial_context: Dict = {}) -> Dict[str, Any]:
        """Execute all stages of the prompt"""
        context = initial_context.copy()
        
        for stage in self.stages:
            # Format messages with current context
            system_msg = stage.system_message.format(**context)
            user_msg = stage.user_message.format(**context)
            
            # Execute stage
            response = await ai_client.generate_response(
                system_message=system_msg,
                user_message=user_msg,
                temperature=stage.temperature,
                max_tokens=stage.max_tokens
            )
            
            # Update context
            context.update(response)
            self.results.append(response)
            
        return context

class PromptTemplates:
    """Centralized prompt templates for the system"""
    
    @staticmethod
    def card_meaning(card: CardMeaning, golden_dawn_content: Dict[str, str], is_reversed: bool = False) -> str:
        """Generate prompt for card meaning interpretation with Golden Dawn context"""
        orientation = "reversed" if is_reversed else "upright"
        gd_description = golden_dawn_content.get(card.name, "No Golden Dawn description available.")
        
        return f"""
        Analyze the {orientation} meaning of the {card.name} tarot card.
        Consider:
        - Traditional symbolism: {gd_description}
        - Elemental associations: {card.element}
        - Astrological correspondences: {card.astrological}
        - Kabbalistic path: {card.kabbalistic}
        - Practical applications
        Provide a concise, modern interpretation that aligns with the Golden Dawn tradition.
        """
        
    @staticmethod
    def reading_interpretation(cards: List[CardMeaning], question: str) -> str:
        """Generate prompt for reading interpretation"""
        card_names = ", ".join(c.name for c in cards)
        return f"""
        Interpret this tarot reading:
        Cards: {card_names}
        Question: {question}
        Provide:
        1. Overall theme
        2. Card interactions
        3. Practical advice
        4. Potential outcomes
        """
