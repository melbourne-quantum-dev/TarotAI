from pathlib import Path
from typing import Dict, List, Optional
import yaml
from pydantic import BaseModel, Field, validator

class PromptTemplate(BaseModel):
    """Base class for prompt templates"""
    name: str
    version: str = "1.0.0"
    description: str
    template: str
    variables: List[str]
    examples: List[Dict[str, str]] = Field(default_factory=list)
    constraints: Dict[str, str] = Field(default_factory=dict)
    
    @validator('template')
    def validate_template(cls, v):
        if not v.strip():
            raise ValueError("Template cannot be empty")
        return v
        
    def render(self, **kwargs) -> str:
        """Render template with variables"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable: {str(e)}")

class PromptTemplateManager:
    """Manages prompt templates with version control"""
    
    def __init__(self, template_dir: Path = Path("prompts")):
        self.template_dir = template_dir
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, PromptTemplate]:
        """Load templates from YAML files"""
        templates = {}
        for file in self.template_dir.glob("*.yaml"):
            with open(file) as f:
                data = yaml.safe_load(f)
                templates[data["name"]] = PromptTemplate(**data)
        return templates
        
    def get_template(self, name: str, version: Optional[str] = None) -> PromptTemplate:
        """Get template by name and optional version"""
        template = self.templates.get(name)
        if not template:
            raise ValueError(f"Template {name} not found")
            
        if version and template.version != version:
            raise ValueError(
                f"Version mismatch: requested {version}, found {template.version}"
            )
            
        return template
