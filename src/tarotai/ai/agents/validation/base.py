from typing import Dict, List
from .base import BaseAgent

class ValidationAgent(BaseAgent):
    """Agent responsible for validating card data and interpretations."""
    
    async def process(self, data: Dict) -> Dict:
        """Validate the provided data."""
        validation_result = await self._validate_data(data)
        if not validation_result['is_valid']:
            return await self._get_corrections(data, validation_result['errors'])
        return validation_result

    async def _validate_data(self, data: Dict) -> Dict:
        """Validate data against schema and rules."""
        template = self.prompt_manager.get_template("validation.j2")
        prompt = template.render(data=data)
        return await self.ai_client.validate(prompt)

    async def _get_corrections(self, data: Dict, errors: List[str]) -> Dict:
        """Get specific corrections for invalid data."""
        template = self.prompt_manager.get_template("correction.j2")
        prompt = template.render(data=data, errors=errors)
        return await self.ai_client.generate(prompt)