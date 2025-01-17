import os
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt
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
        self.model = "voyage-large-2"
        self.embedding_dim = 1024
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        )
        self.usage_tracker = {
            "total_tokens": 0,
            "requests": 0,
            "total_characters": 0
        }

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(5)
    )

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from Voyage AI."""
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
            raise EnrichmentError(f"Voyage API request failed: {str(e)}")

    async def generate_embedding(self, text: str, dimensions: Optional[int] = None) -> List[float]:
        """Generate embedding with optional dimension reduction"""
        try:
            params = {
                "model": self.model,
                "input": text
            }
            if dimensions:
                params["dimensions"] = dimensions
                
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json=params
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"Voyage embedding request failed: {str(e)}")

    async def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in a single request"""
        try:
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": texts
                }
            )
            response.raise_for_status()
            return [item["embedding"] for item in response.json()["data"]]
        except Exception as e:
            raise EnrichmentError(f"Voyage batch embedding request failed: {str(e)}")

    async def generate_embedding_with_metadata(self, text: str) -> Dict[str, Any]:
        """Generate embedding with metadata"""
        try:
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": text,
                    "include_metadata": True
                }
            )
            response.raise_for_status()
            
            # Update usage tracking
            self.usage_tracker["total_tokens"] += len(text.split())
            self.usage_tracker["requests"] += 1
            self.usage_tracker["total_characters"] += len(text)
            
            return response.json()["data"][0]
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
            
            # Update usage tracking
            total_tokens = sum(len(msg["content"].split()) for msg in messages)
            self.usage_tracker["total_tokens"] += total_tokens
            self.usage_tracker["requests"] += 1
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"Voyage conversational request failed: {str(e)}")

    def get_usage_stats(self) -> Dict[str, int]:
        """Get current usage statistics"""
        return self.usage_tracker
