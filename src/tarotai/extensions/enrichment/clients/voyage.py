import os
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from ..exceptions import EnrichmentError
from .base import BaseAIClient

load_dotenv()

class VoyageClient(BaseAIClient):
    """Client for interacting with Voyage AI's embedding API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        if not self.api_key:
            raise EnrichmentError("Voyage API key not found in environment variables.")
        
        self.base_url = "https://api.voyageai.com/v1"
        self.model = "voyage-01"
        self.embedding_dim = 1024

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from Voyage AI."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={"prompt": prompt, **kwargs}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise EnrichmentError(f"Voyage API request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings for the given text."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/embeddings",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "input": text
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"Voyage embedding request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from Voyage AI."""
        try:
            response = await self.generate_response(
                prompt,
                response_format={"type": "json_object"}
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"Voyage JSON request failed: {str(e)}")

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
            response = await self.generate_response(
                model=self.model,
                messages=messages
            )
            if no_prefix:
                return response["choices"][0]["message"]["content"]
            return prefix + response["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"Voyage prefix request failed: {str(e)}")

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
            response = await self.generate_response(
                model=self.model,
                messages=messages
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"Voyage conversational request failed: {str(e)}")
