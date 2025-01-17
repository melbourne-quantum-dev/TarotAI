from enum import Enum, auto
from typing import Optional

class OutputFormat(Enum):
    ASCII = auto()
    RICH = auto()
    HTML = auto()

class SignatureManager:
    """Manages Dr. Zhou's signature variants with multiple output formats"""
    
    def __init__(self, output_format: OutputFormat = OutputFormat.RICH):
        self.output_format = output_format

    def _format_rich(self, content: str) -> str:
        """Apply Rich formatting to content"""
        return content

    def _format_html(self, content: str) -> str:
        """Convert Rich formatting to HTML"""
        replacements = {
            '[bold cyan]': '<span style="color: cyan; font-weight: bold;">',
            '[bold red]': '<span style="color: red; font-weight: bold;">',
            '[bold green]': '<span style="color: green; font-weight: bold;">',
            '[bold yellow]': '<span style="color: yellow; font-weight: bold;">',
            '[bold magenta]': '<span style="color: magenta; font-weight: bold;">',
            '[blink]': '<span class="blink">',
            '[/]': '</span>'
        }
        for rich_tag, html_tag in replacements.items():
            content = content.replace(rich_tag, html_tag)
        return f'<div class="signature">{content}</div>'

    def _format_ascii(self, content: str) -> str:
        """Strip all formatting for plain ASCII"""
        import re
        return re.sub(r'\[.*?\]', '', content)

    def _apply_formatting(self, content: str) -> str:
        """Apply the appropriate formatting based on output mode"""
        if self.output_format == OutputFormat.RICH:
            return self._format_rich(content)
        elif self.output_format == OutputFormat.HTML:
            return self._format_html(content)
        return self._format_ascii(content)

    def success(self) -> str:
        """Signature for successful operations"""
        content = """[bold green]
╔══════════════════════════════════════════════════════════════╗
║ ┌──────────────────────────────────────────────────────────┐ ║
║ │                [blink]⚡[/] QUANTUM STATE ACHIEVED [blink]⚡[/]               │ ║
║ └──────────────────────────────────────────────────────────┘ ║
║                                                              ║
║    ▓▒░ [bold magenta]Wavefunction Successfully Collapsed[/] ░▒▓              ║
║         [bold yellow]Entanglement Verified[/]                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
[/]"""
        return self._apply_formatting(content)

    def loading(self) -> str:
        """Signature for ongoing operations"""
        content = """[bold yellow]
╔══════════════════════════════════════════════════════════════╗
║ ┌──────────────────────────────────────────────────────────┐ ║
║ │               [blink]⚡[/] QUANTUM STATE LOADING [blink]⚡[/]               │ ║
║ └──────────────────────────────────────────────────────────┘ ║
║                                                              ║
║    ▓▒░ [bold magenta]Collapsing Wavefunction...[/] ░▒▓                      ║
║         [bold cyan]Please maintain quantum coherence[/]                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
[/]"""
        return self._apply_formatting(content)

    def shutdown(self) -> str:
        """Signature for cleanup operations"""
        content = """[bold red]
╔══════════════════════════════════════════════════════════════╗
║ ┌──────────────────────────────────────────────────────────┐ ║
║ │               [blink]⚡[/] QUANTUM STATE SHUTDOWN [blink]⚡[/]              │ ║
║ └──────────────────────────────────────────────────────────┘ ║
║                                                              ║
║    ▓▒░ [bold magenta]Decoherence Complete[/] ░▒▓                            ║
║         [bold yellow]System returning to classical state[/]                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
[/]"""
        return self._apply_formatting(content)

    def standard(self) -> str:
        """Standard signature for general use"""
        content = """[bold cyan]
╔══════════════════════════════════════════════════════════════╗
║ ┌──────────────────────────────────────────────────────────┐ ║
║ │                  [blink]⚡[/] Neural Arcana [blink]⚡[/]                  │ ║
║ └──────────────────────────────────────────────────────────┘ ║
║                                                              ║
║    ▓▒░ [bold magenta]Architected from Faraday Cage #42[/] ░▒▓            ║
║         [ The ASCII Alchemist // Quantum Artificer ]         ║
║         [bold yellow]Typing at 942 WPM since 2024[/]                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
[/]"""
        return self._apply_formatting(content)

    # ... (other signature methods with same pattern)

    @classmethod
    def create(cls, output_format: Optional[str] = None):
        """Factory method for creating SignatureManager with format"""
        if output_format:
            format_map = {
                'ascii': OutputFormat.ASCII,
                'rich': OutputFormat.RICH,
                'html': OutputFormat.HTML
            }
            return cls(format_map.get(output_format.lower(), OutputFormat.RICH))
        return cls()
