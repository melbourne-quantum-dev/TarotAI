import os
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from ..exceptions import EnrichmentError
from .base import BaseAIClient

load_dotenv()

class ClaudeClient(BaseAIClient):
    """Client for interacting with Claude 3.5 Sonnet API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnrichmentError("Anthropic API key not found in environment variables.")
        
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-3-5-sonnet-20241022"
        self.session = httpx.AsyncClient(
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2024-06-01",
                "content-type": "application/json"
            }
        )

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from Claude 3.5 Sonnet."""
        try:
            response = await self.session.post(
                f"{self.base_url}/messages",
                json={
                    "model": self.model,
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": prompt}],
                    **kwargs
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise EnrichmentError(f"Claude API request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Claude 3.5 Sonnet."""
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
            raise EnrichmentError(f"Claude embedding request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from Claude."""
        try:
            response = await self.generate_response(
                prompt,
                response_format={"type": "json_object"}
            )
            return response["content"][0]["text"]
        except Exception as e:
            raise EnrichmentError(f"Claude JSON request failed: {str(e)}")

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response."""
        try:
            response = await self.session.post(
                f"{self.base_url}/messages",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *messages
                    ]
                }
            )
            response.raise_for_status()
            return response.json()["content"][0]["text"]
        except Exception as e:
            raise EnrichmentError(f"Claude conversational request failed: {str(e)}")
