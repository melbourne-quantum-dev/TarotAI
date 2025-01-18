import os
from typing import Dict, Any, List, Optional, Union
from voyageai import AsyncClient
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt
from tarotai.core.errors import EnrichmentError
from tarotai.ai.clients.base import BaseAIClient

load_dotenv()

class VoyageClient(BaseAIClient):
    """Client for interacting with Voyage AI's embedding API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        if not self.api_key:
            raise EnrichmentError("Voyage API key not found in environment variables.")
        
        self.client = AsyncClient(api_key=self.api_key, max_retries=5)
        self.model = "voyage-large-2"
        self.embedding_dim = 1024
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_characters": 0,
            "image_pixels": 0,
            "errors": 0
        }

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get detailed usage statistics"""
        return {
            **self.usage_tracker,
            "estimated_cost": self._calculate_cost()
        }

    def _calculate_cost(self) -> float:
        """Calculate estimated API costs"""
        # Pricing based on VoyageAI's current rates
        text_cost = self.usage_tracker["text_tokens"] / 1000 * 0.0001
        image_cost = self.usage_tracker["image_pixels"] / 1000000 * 0.01
        return text_cost + image_cost

    async def generate_multimodal_embedding(
        self,
        content: List[Dict[str, Any]],
        input_type: Optional[str] = None
    ) -> List[float]:
        """Generate embeddings for mixed text/image content"""
        try:
            result = await self.client.embed_multimodal(
                content,
                model="voyage-multimodal-3",
                input_type=input_type
            )
            
            # Update usage tracking
            self.usage_tracker["requests"] += 1
            for item in content:
                if item["type"] == "text":
                    self.usage_tracker["text_tokens"] += len(item["text"].split())
                elif item["type"] == "image_url":
                    self.usage_tracker["image_pixels"] += 1000000  # Estimate based on typical image size
                    
            return result.embeddings[0]
        except Exception as e:
            raise EnrichmentError(f"Multimodal embedding failed: {str(e)}")

    async def rerank_documents(
        self,
        query: str,
        documents: List[str],
        model: str = "rerank-2",
        top_k: Optional[int] = None,
        return_documents: bool = False
    ) -> List[Dict[str, Any]]:
        """Rerank documents based on relevance to query"""
        try:
            params = {
                "query": query,
                "documents": documents,
                "model": model,
                "return_documents": return_documents
            }
            if top_k:
                params["top_k"] = top_k
                
            response = await self.session.post(
                f"{self.base_url}/rerank",
                json=params
            )
            response.raise_for_status()
            
            # Update usage tracking
            self.usage_tracker["requests"] += 1
            self.usage_tracker["text_tokens"] += len(query.split())
            self.usage_tracker["text_tokens"] += sum(len(doc.split()) for doc in documents)
            
            return response.json()["data"]
        except Exception as e:
            raise EnrichmentError(f"Reranking failed: {str(e)}")

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

    async def generate_embedding(
        self, 
        text: str, 
        input_type: Optional[str] = None,
        truncate: bool = True,
        dimensions: Optional[int] = None,
        dtype: str = "float"
    ) -> List[float]:
        """Generate embedding with advanced options"""
        try:
            result = await self.client.embed(
                [text],
                model=self.model,
                input_type=input_type,
                truncate=truncate,
                output_dimension=dimensions,
                output_dtype=dtype
            )
            
            # Update usage tracking
            self.usage_tracker["total_tokens"] += len(text.split())
            self.usage_tracker["requests"] += 1
            self.usage_tracker["total_characters"] += len(text)
            
            return result.embeddings[0]
        except Exception as e:
            raise EnrichmentError(f"Voyage embedding request failed: {str(e)}")

    async def generate_batch_embeddings(
        self, 
        texts: List[str], 
        include_metadata: bool = False,
        input_type: Optional[str] = None,
        truncate: bool = True,
        dimensions: Optional[int] = None,
        dtype: str = "float"
    ) -> Union[List[List[float]], List[Dict[str, Any]]]:
        """Generate batch embeddings with advanced options"""
        try:
            result = await self.client.embed(
                texts,
                model=self.model,
                input_type=input_type,
                truncate=truncate,
                output_dimension=dimensions,
                output_dtype=dtype
            )
            
            # Update usage tracking
            total_tokens = sum(len(text.split()) for text in texts)
            self.usage_tracker["total_tokens"] += total_tokens
            self.usage_tracker["requests"] += 1
            self.usage_tracker["total_characters"] += sum(len(text) for text in texts)
            
            if include_metadata:
                return [{"embedding": emb, "metadata": {}} for emb in result.embeddings]
            return result.embeddings
        except Exception as e:
            raise EnrichmentError(f"Voyage batch embedding request failed: {str(e)}")

    async def generate_quantized_embedding(
        self, 
        text: str, 
        dtype: str = "int8",
        input_type: Optional[str] = None,
        truncate: bool = True
    ) -> List[float]:
        """Generate quantized embedding"""
        try:
            params = {
                "model": self.model,
                "input": text,
                "output_dtype": dtype,
                "truncation": truncate
            }
            
            if input_type:
                params["input_type"] = input_type
                
            response = await self.session.post(
                f"{self.base_url}/embeddings",
                json=params
            )
            response.raise_for_status()
            
            # Update usage tracking
            self.usage_tracker["total_tokens"] += len(text.split())
            self.usage_tracker["requests"] += 1
            self.usage_tracker["total_characters"] += len(text)
            
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            raise EnrichmentError(f"Voyage quantized embedding request failed: {str(e)}")

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
