from pathlib import Path
from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

class PromptTemplateManager:
    """Manages prompt templates for AI interactions"""
    
    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or Path(__file__).parent / "templates"
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.templates: Dict[str, str] = {}

    def get_template(self, name: str) -> str:
        """Get a rendered template by name"""
        if name not in self.templates:
            template = self.env.get_template(f"{name}.j2")
            self.templates[name] = template
        return self.templates[name]

    def render(self, template_name: str, **kwargs) -> str:
        """Render a template with provided context"""
        template = self.get_template(template_name)
        return template.render(**kwargs)
