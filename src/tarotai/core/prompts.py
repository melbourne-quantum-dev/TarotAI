from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class PromptStage(BaseModel):
    name: str
    system_message: str
    user_message: str
    output_format: Optional[Dict[str, str]] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None

class MultiStagePrompt:
    def __init__(self, stages: List[PromptStage]):
        self.stages = stages
        self.results: List[Dict[str, Any]] = []
        
    async def execute(self, ai_client, initial_context: Dict = {}):
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
