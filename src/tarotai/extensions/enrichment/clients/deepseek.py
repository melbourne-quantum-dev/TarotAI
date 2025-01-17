import os
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv
from ..exceptions import EnrichmentError
from .base import BaseAIClient

load_dotenv()

class DeepSeekClient(BaseAIClient):
    """Client for interacting with DeepSeek API with V3 features."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise EnrichmentError("DeepSeek API key not found in environment variables.")
        
        self.base_url = "https://api.deepseek.com/v1"
        self.beta_url = "https://api.deepseek.com/beta"  # For experimental features
        self.model = "deepseek-v3"
        self.mtp_enabled = True  # Enable Multi-Token Prediction by default
        self.precision = "fp8"  # Default to FP8 precision
        self.load_balancing = "auxiliary-free"  # New load balancing strategy
        self.conversation_history = []  # Track conversation context
        
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-DeepSeek-Precision": self.precision,
                "X-DeepSeek-MTP": str(self.mtp_enabled).lower()
            }
        )

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from DeepSeek with MTP support and conversation history."""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            
            if self.mtp_enabled:
                response = await self._generate_with_mtp(prompt, **kwargs)
            else:
                response = await self.session.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": self.conversation_history,
                        **kwargs
                    }
                )
                response.raise_for_status()
                response = response.json()
            
            # Add assistant response to history
            if response.get("choices"):
                self.conversation_history.append(response["choices"][0]["message"])
            
            return response
        except Exception as e:
            raise EnrichmentError(f"DeepSeek API request failed: {str(e)}")

    async def _generate_with_mtp(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response using Multi-Token Prediction."""
        try:
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "mtp": True,
                    "mtp_window": 4,  # Default window size
                    **kwargs
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise EnrichmentError(f"DeepSeek MTP request failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using DeepSeek with FP8 support and context tracking."""
        try:
            # Add embedding request to conversation history
            self.conversation_history.append({
                "role": "system",
                "content": f"Embedding request for text: {text[:100]}..."
            })
            
            if self.precision == "fp8":
                return await self._generate_fp8_embedding(text)
                
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": text,
                    "precision": self.precision
                }
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek embedding request failed: {str(e)}")

    async def _generate_fp8_embedding(self, text: str) -> List[float]:
        """Generate FP8 precision embeddings."""
        try:
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json={
                    "model": self.model,
                    "input": text,
                    "precision": "fp8",
                    "quantization": "e4m3"  # FP8 format
                }
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek FP8 embedding request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from DeepSeek with structured output."""
        try:
            system_prompt = """
            You are a tarot interpretation assistant. Always output in JSON format.
            Example output: {"meaning": "...", "keywords": ["...", "..."]}
            """
            
            # Add system prompt if not already in history
            if not any(msg["role"] == "system" for msg in self.conversation_history):
                self.conversation_history.insert(0, {"role": "system", "content": system_prompt})
            
            response = await self.generate_response(
                prompt,
                response_format={"type": "json_object"}
            )
            return json.loads(response["choices"][0]["message"]["content"])
        except Exception as e:
            raise EnrichmentError(f"DeepSeek JSON request failed: {str(e)}")

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response with load balancing and context management."""
        try:
            # Configure load balancing
            if self.load_balancing == "auxiliary-free":
                load_balancing_config = {
                    "strategy": "auxiliary-free",
                    "capacity_factor": 1.25,
                    "router_type": "learned"
                }
            else:
                load_balancing_config = {
                    "strategy": self.load_balancing
                }
            
            # Add system prompt if not already in history
            if not any(msg["role"] == "system" for msg in self.conversation_history):
                self.conversation_history.insert(0, {"role": "system", "content": system_prompt})
            
            # Add new messages to conversation history
            self.conversation_history.extend(messages)
                
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": self.conversation_history,
                    "load_balancing": load_balancing_config
                }
            )
            response.raise_for_status()
            response_data = response.json()
            
            # Add assistant response to history
            if response_data.get("choices"):
                self.conversation_history.append(response_data["choices"][0]["message"])
            
            return response_data["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek conversational request failed: {str(e)}")
