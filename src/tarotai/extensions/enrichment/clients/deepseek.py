import os
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from ..exceptions import EnrichmentError
from .base import BaseAIClient

load_dotenv()

class DeepSeekClient(BaseAIClient):
    """Client for interacting with DeepSeek API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise EnrichmentError("DeepSeek API key not found in environment variables.")
        
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat-4"
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from DeepSeek."""
        try:
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise EnrichmentError(f"DeepSeek API request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using DeepSeek."""
        try:
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": text
                }
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek embedding request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from DeepSeek."""
        try:
            response = await self.generate_response(
                prompt,
                response_format={"type": "json_object"}
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek JSON request failed: {str(e)}")

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response."""
        try:
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *messages
                    ]
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek conversational request failed: {str(e)}")
