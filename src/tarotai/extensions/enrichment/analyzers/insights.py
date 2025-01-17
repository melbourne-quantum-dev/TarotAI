from typing import Dict, List, Optional
from ..exceptions import EnrichmentError
from ..clients.base import BaseAIClient

class InsightGenerator:
    """Generates insights and evaluates reading quality"""
    
    def __init__(self, ai_client: BaseAIClient):
        self.ai_client = ai_client
        
    async def evaluate_reading(self, interpretation: str) -> Dict[str, float]:
        """Evaluate the quality of a reading interpretation"""
        try:
            evaluation_prompt = f"""
            Evaluate this tarot interpretation:
            
            {interpretation}
            
            Provide scores for:
            - Accuracy (0-1)
            - Relevance (0-1)
            - Depth (0-1)
            - Clarity (0-1)
            """
            return await self.ai_client.json_prompt(evaluation_prompt)
        except Exception as e:
            raise EnrichmentError(f"Evaluation failed: {str(e)}")
            
    async def generate_insights(self, reading_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate insights from reading history"""
        try:
            prompt = f"""
            Analyze this reading history:
            
            {json.dumps(reading_history, indent=2)}
            
            Identify:
            1. Common patterns
            2. Emerging themes
            3. Potential biases
            4. Areas for improvement
            """
            return await self.ai_client.json_prompt(prompt)
        except Exception as e:
            raise EnrichmentError(f"Insight generation failed: {str(e)}")
