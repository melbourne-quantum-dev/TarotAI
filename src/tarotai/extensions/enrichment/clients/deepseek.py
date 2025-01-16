import os
import json
from typing import Dict, Any, Optional, List
import httpx
from dotenv import load_dotenv
from ..exceptions import EnrichmentError

load_dotenv()

class DeepSeekClient:
    """Client for interacting with DeepSeek Chat API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise EnrichmentError("DeepSeek API key not found in environment variables.")
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from DeepSeek Chat."""
        try:
            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                **kwargs
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            raise EnrichmentError(f"DeepSeek API request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using DeepSeek (if supported)."""
        raise NotImplementedError("DeepSeek does not currently support embeddings.")
