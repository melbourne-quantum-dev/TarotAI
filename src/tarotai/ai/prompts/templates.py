from pathlib import Path
import yaml
from .manager import MultiStagePrompt, PromptStage

class PromptTemplateManager:
    def __init__(self, template_dir: Path = Path("prompts")):
        self.template_dir = template_dir
        self.templates = self._load_templates()
        
    def _load_templates(self):
        templates = {}
        for file in self.template_dir.glob("*.yaml"):
            with open(file) as f:
                templates[file.stem] = yaml.safe_load(f)
        return templates
        
    def get_template(self, name: str) -> MultiStagePrompt:
        template = self.templates.get(name)
        if not template:
            raise ValueError(f"Template {name} not found")
            
        return MultiStagePrompt([
            PromptStage(**stage) for stage in template["stages"]
        ])
