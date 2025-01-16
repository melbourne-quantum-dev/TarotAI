import os
import json
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv
from openai import OpenAI
from ..exceptions import EnrichmentError
from .base import BaseAIClient

load_dotenv()

class DeepSeekClient(BaseAIClient):
    """Client for interacting with DeepSeek Chat API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise EnrichmentError("DeepSeek API key not found in environment variables.")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-chat"

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from DeepSeek Chat."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise EnrichmentError(f"DeepSeek API request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from DeepSeek."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise EnrichmentError(f"DeepSeek JSON request failed: {str(e)}")

    async def prefix_prompt(
        self, 
        prompt: str, 
        prefix: str, 
        no_prefix: bool = False
    ) -> str:
        """Generate a response with a prefix constraint."""
        try:
            messages = [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": prefix, "prefix": True},
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            if no_prefix:
                return response.choices[0].message.content
            return prefix + response.choices[0].message.content
        except Exception as e:
            raise EnrichmentError(f"DeepSeek prefix request failed: {str(e)}")

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                *messages,
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise EnrichmentError(f"DeepSeek conversational request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using DeepSeek (if supported)."""
        raise NotImplementedError("DeepSeek does not currently support embeddings.")
