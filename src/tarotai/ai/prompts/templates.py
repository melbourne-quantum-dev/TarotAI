from pathlib import Path
import yaml
from .manager import MultiStagePrompt, PromptStage

# Tarot Meaning Generation Prompts
UPRIGHT_PROMPT = """
Generate an upright meaning for the {card_name} tarot card. 
The card is associated with {element} and represents {keywords}.
The astrological correspondence is {astrological}, and the Kabbalistic path is {kabbalistic}.
Provide a concise, modern interpretation.
"""

REVERSED_PROMPT = """
Generate a reversed meaning for the {card_name} tarot card.
The upright meaning is: {upright_meaning}.
Provide a concise, modern interpretation of the reversed energy.
"""

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
