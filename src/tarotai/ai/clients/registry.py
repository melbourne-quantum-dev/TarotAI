"""Provider registry for AI clients"""
from typing import Dict, Type
from .base import BaseAIClient

class ProviderRegistry:
    _providers: Dict[str, Type[BaseAIClient]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(provider_class: Type[BaseAIClient]):
            cls._providers[name] = provider_class
            return provider_class
        return decorator

    @classmethod
    def get_provider(cls, name: str) -> Type[BaseAIClient]:
        if name not in cls._providers:
            raise ValueError(f"Provider {name} not registered")
        return cls._providers[name]
