"""Provider registry for AI clients and prompt templates"""
from typing import Dict, Type, Any
from .base import BaseAIClient
from ..prompts.manager import PromptTemplateManager

class ProviderRegistry:
    _providers: Dict[str, Type[BaseAIClient]] = {}
    _prompt_manager: PromptTemplateManager = None

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

    @classmethod
    def get_prompt_manager(cls) -> PromptTemplateManager:
        if cls._prompt_manager is None:
            cls._prompt_manager = PromptTemplateManager()
        return cls._prompt_manager

    @classmethod
    def render_prompt(cls, template_name: str, **kwargs) -> str:
        """Render a prompt using the template manager"""
        manager = cls.get_prompt_manager()
        template = manager.get_template(template_name)
        return template.render(**kwargs)
