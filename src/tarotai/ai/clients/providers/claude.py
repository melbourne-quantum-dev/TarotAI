import os
import anthropic
from typing import Dict, Any, List, Optional, AsyncGenerator
from dotenv import load_dotenv
from ..exceptions import EnrichmentError
from ...ai.clients.base import BaseAIClient

load_dotenv()

class ClaudeClient(BaseAIClient):
    """Client for interacting with Claude 3.5 Sonnet API using official SDK."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnrichmentError("Anthropic API key not found in environment variables.")
        
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-latest"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnrichmentError("Anthropic API key not found in environment variables.")
        
        self.client = anthropic.AsyncAnthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-latest"
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_characters": 0,
            "errors": 0
        }

    async def generate_response(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from Claude 3.5 Sonnet."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            
            # Update usage stats
            self.usage_stats["total_requests"] += 1
            self.usage_stats["total_tokens"] += response.usage.input_tokens + response.usage.output_tokens
            self.usage_stats["total_characters"] += len(prompt)
            
            return response.dict()
        except anthropic.APIConnectionError as e:
            self.usage_stats["errors"] += 1
            raise EnrichmentError(
                f"Connection error: {e}",
                detail={
                    "type": "connection_error",
                    "message": str(e),
                    "retryable": True
                }
            )
        except anthropic.RateLimitError as e:
            self.usage_stats["errors"] += 1
            raise EnrichmentError(
                f"Rate limit exceeded: {e}",
                detail={
                    "type": "rate_limit",
                    "message": str(e),
                    "retryable": True,
                    "retry_after": e.response.headers.get("Retry-After", 60)
                }
            )
        except anthropic.APIStatusError as e:
            self.usage_stats["errors"] += 1
            raise EnrichmentError(
                f"API error: {e.status_code} - {e.response}",
                detail={
                    "type": "api_error",
                    "status_code": e.status_code,
                    "response": str(e.response),
                    "retryable": e.status_code >= 500
                }
            )
        except Exception as e:
            self.usage_stats["errors"] += 1
            raise EnrichmentError(
                f"Claude API request failed: {str(e)}",
                detail={
                    "type": "unknown_error",
                    "message": str(e),
                    "retryable": False
                }
            )

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get detailed usage statistics"""
        return {
            **self.usage_stats,
            "estimated_cost": self._calculate_cost()
        }

    def _calculate_cost(self) -> float:
        """Calculate estimated API costs based on Anthropic pricing"""
        # Pricing as of 2025-01-17
        input_cost = (self.usage_stats["total_tokens"] / 1000) * 0.01  # $0.01 per 1k tokens
        return input_cost

    async def generate_batch_responses(self, prompts: List[str]) -> List[Dict[str, Any]]:
        """Generate responses for multiple prompts in a batch."""
        try:
            batch = await self.client.beta.messages.batches.create(
                requests=[
                    {
                        "custom_id": f"prompt-{i}",
                        "params": {
                            "model": self.model,
                            "max_tokens": 4096,
                            "messages": [{"role": "user", "content": prompt}]
                        }
                    }
                    for i, prompt in enumerate(prompts)
                ]
            )
            
            results = []
            async for entry in self.client.beta.messages.batches.results(batch.id):
                if entry.result.type == "succeeded":
                    results.append(entry.result.message.dict())
            return results
        except Exception as e:
            raise EnrichmentError(f"Batch processing failed: {str(e)}")

    async def generate_structured_response(
        self, 
        prompt: str, 
        tools: List[Dict[str, Any]],
        tool_choice: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a structured response using tool calling."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
                tools=tools,
                tool_choice=tool_choice
            )
            return response.dict()
        except Exception as e:
            raise EnrichmentError(f"Structured response failed: {str(e)}")

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Claude 3.5 Sonnet."""
        try:
            # Claude doesn't have native embeddings, use text-to-embedding via messages
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": f"Generate an embedding vector for this text: {text}"}],
                response_format={"type": "json_object"}
            )
            return list(response.content[0].text.values())
        except Exception as e:
            raise EnrichmentError(f"Claude embedding request failed: {str(e)}")

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from Claude."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return response.content[0].text
        except Exception as e:
            raise EnrichmentError(f"Claude JSON request failed: {str(e)}")

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "You are a helpful assistant."
    ) -> str:
        """Generate a conversational response."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {"role": "system", "content": system_prompt},
                    *messages
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise EnrichmentError(f"Claude conversational request failed: {str(e)}")

    async def stream_response(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream response from Claude."""
        try:
            async with self.client.messages.stream(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                async for chunk in stream:
                    yield chunk.text
        except Exception as e:
            raise EnrichmentError(f"Streaming failed: {str(e)}")

    async def extract_structured_knowledge(
        self,
        pdf_content: str
    ) -> Dict[str, Any]:
        """Extract structured knowledge using Claude's JSON capabilities"""
        prompt = f"""
        Extract Golden Dawn knowledge from this content:
        {pdf_content[:10000]}  # First 10k chars
        
        Return structured JSON with:
        - astrological_correspondences
        - kabbalistic_paths
        - elemental_attributions
        - card_symbolism
        """
        
        return await self.json_prompt(prompt)
