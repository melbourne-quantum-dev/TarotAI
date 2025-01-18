from ..imports import *
import json
import httpx
from ..base import BaseChatClient
from ..registry import ProviderRegistry

@ProviderRegistry.register("deepseek")
class DeepSeekClient(BaseChatClient):
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
        
        # Initialize usage tracking
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_characters": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "errors": 0
        }
        
        # Conversation history and caching
        self.conversation_history = []
        self.usage_stats = {
            'cache_hit_tokens': 0,
            'cache_miss_tokens': 0,
            'total_requests': 0
        }
        
        # System prompt for consistent caching
        self.system_prompt = """
        You are a tarot interpretation assistant. Always provide:
        - Upright meaning
        - Reversed meaning
        - Keywords
        - Elemental association
        """
        
        self.session = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-DeepSeek-Precision": self.precision,
                "X-DeepSeek-MTP": str(self.mtp_enabled).lower()
            }
        )

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = None,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate a response from DeepSeek with MTP support and conversation history."""
        try:
            # Add system prompt if not already in history
            if not any(msg["role"] == "system" for msg in self.conversation_history):
                self.conversation_history.insert(0, {
                    "role": "system",
                    "content": self.system_prompt
                })
            
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": prompt})
            
            params = {
                "model": self.model,
                "messages": self.conversation_history,
                "temperature": temperature,
                "top_p": top_p,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                **kwargs
            }
            
            if tools:
                params["tools"] = tools
            if tool_choice:
                params["tool_choice"] = tool_choice
            
            if self.mtp_enabled:
                response = await self._generate_with_mtp(prompt, **params)
            else:
                response = await self.session.post(
                    f"{self.base_url}/chat/completions",
                    json=params
                )
                response.raise_for_status()
                response = response.json()
            
            # Update cache statistics
            usage = response.get("usage", {})
            self.usage_stats['cache_hit_tokens'] += usage.get('prompt_cache_hit_tokens', 0)
            self.usage_stats['cache_miss_tokens'] += usage.get('prompt_cache_miss_tokens', 0)
            self.usage_stats['total_requests'] += 1
            
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

    async def chain_of_thought(self, question: str) -> str:
        """Generate a response using chain-of-thought prompting."""
        prompt = f"""
        Let's think step by step:
        
        Question: {question}
        
        First, analyze the key components of the question.
        Then, consider the relevant tarot symbolism.
        Finally, provide a detailed interpretation.
        """
        return await self.generate_response(prompt)

    async def json_prompt(self, prompt: str) -> Dict[str, Any]:
        """Generate a JSON response from DeepSeek with structured output."""
        try:
            # Add JSON-specific system prompt
            json_system_prompt = self.system_prompt + """
            Always output in JSON format.
            Example output: {"meaning": "...", "keywords": ["...", "..."]}
            """
            
            # Add system prompt if not already in history
            if not any(msg["role"] == "system" for msg in self.conversation_history):
                self.conversation_history.insert(0, {
                    "role": "system",
                    "content": json_system_prompt
                })
            
            response = await self.generate_response(
                prompt,
                response_format={"type": "json_object"}
            )
            return json.loads(response["choices"][0]["message"]["content"])
        except Exception as e:
            raise EnrichmentError(f"DeepSeek JSON request failed: {str(e)}")

    async def evaluate_response(self, response: str) -> Dict[str, float]:
        """Evaluate a tarot interpretation response."""
        evaluation_prompt = f"""
        Evaluate this tarot interpretation:
        
        {response}
        
        Provide scores for:
        - Accuracy (0-1)
        - Relevance (0-1)
        - Depth (0-1)
        - Clarity (0-1)
        """
        return await self.json_prompt(evaluation_prompt)

    async def stream_response(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Stream response from DeepSeek API"""
        try:
            async with self.session.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": True,
                    **kwargs
                }
            ) as response:
                async for chunk in response.aiter_text():
                    if chunk:
                        yield chunk
        except Exception as e:
            raise EnrichmentError(f"DeepSeek streaming failed: {str(e)}")

    async def generate_meaning_from_correspondences(
        self,
        card: Dict[str, Any],
        gd_knowledge: Dict[str, Any],
        reversed: bool = False
    ) -> str:
        """Generate meaning using DeepSeek's chain-of-thought"""
        context = {
            "card_name": card["name"],
            "element": card["element"],
            "astrological": card["astrological"],
            "kabbalistic": card["kabbalistic"],
            "position": "reversed" if reversed else "upright"
        }
        
        prompt = f"""
        Generate a {context['position']} meaning for {context['card_name']} considering:
        - Element: {context['element']}
        - Astrological: {context['astrological']}
        - Kabbalistic: {context['kabbalistic']}
        - Golden Dawn Symbolism: {gd_knowledge.get('symbolism', [])}
        """
        
        return await self.chain_of_thought(prompt)

    async def conversational_prompt(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None
    ) -> str:
        """Generate a conversational response with load balancing and context management."""
        try:
            # Use default system prompt if not provided
            if system_prompt is None:
                system_prompt = self.system_prompt
            
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
                self.conversation_history.insert(0, {
                    "role": "system",
                    "content": system_prompt
                })
            
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
            
            # Update cache statistics
            usage = response_data.get("usage", {})
            self.usage_stats['cache_hit_tokens'] += usage.get('prompt_cache_hit_tokens', 0)
            self.usage_stats['cache_miss_tokens'] += usage.get('prompt_cache_miss_tokens', 0)
            self.usage_stats['total_requests'] += 1
            
            # Add assistant response to history
            if response_data.get("choices"):
                self.conversation_history.append(response_data["choices"][0]["message"])
            
            return response_data["choices"][0]["message"]["content"]
        except Exception as e:
            raise EnrichmentError(f"DeepSeek conversational request failed: {str(e)}")
