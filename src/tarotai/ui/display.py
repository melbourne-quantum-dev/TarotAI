from dataclasses import dataclass
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.align import Align
from rich.columns import Columns
from rich.text import Text

from tarotai.core.models.types import Reading
from tarotai.config.schemas.config import UnifiedSettings as Settings

@dataclass
class TarotASCII:
    """ASCII art and symbol management"""
    
    HERMETIC_SYMBOLS = {
        'sun': '☉', 'moon': '☽', 'mercury': '☿',
        'venus': '♀', 'mars': '♂', 'jupiter': '♃',
        'saturn': '♄', 'uranus': '♅', 'neptune': '♆',
        'pluto': '♇', 'air': '🜁', 'fire': '🜂',
        'water': '🜄', 'earth': '🜃'
    }

    CYBERPUNK_ELEMENTS = {
        'connection': '◊', 'data': '◈',
        'matrix': '█', 'circuit': '▒',
        'signal': '▓', 'byte': '░'
    }

    CARD_FRAME = """
┌────────────────────────┐
│ {symbols[0]}  ▓▒░      ░▒▓  {symbols[1]} │
├────────────────────────┤
│     ╭──[ {number} ]──╮     │
│     │  {name}  │     │
│     ╰──────────╯     │
│                      │
│    {art_line1}     │
│    {art_line2}     │
│    {art_line3}     │
│                      │
│ ◈                  ◈ │
└────────────────────────┘"""

    @classmethod
    def render_card(cls, number: str, name: str, 
                   symbols: List[str], art_lines: List[str]) -> str:
        """Render a single tarot card with cyberpunk/hermetic styling"""
        return cls.CARD_FRAME.format(
            number=number.zfill(2),
            name=name.center(16),
            symbols=symbols,
            art_line1=art_lines[0].center(16),
            art_line2=art_lines[1].center(16),
            art_line3=art_lines[2].center(16)
        )

class TarotDisplay:
    """Handles all display-related functionality"""
    
    def __init__(self, console: Optional[Console] = None, config: Optional[Settings] = None):
        self.console = console or Console()
        self.config = config or Settings()  # Changed from get_config()
        self.ascii = TarotASCII()
        self.color_scheme = {
            'system': 'cyan',
            'energy': 'magenta',
            'status': 'green',
            'border': 'white',
            'error': 'red',
            'debug': 'yellow'
        }
        
        if self.config.dev_mode:
            self.color_scheme.update({
                'debug': 'yellow',
                'warning': 'orange3',
                'info': 'blue'
            })

    def welcome_banner(self) -> str:
        """Generate welcome banner with cyberpunk styling"""
        return """[bold cyan]
╔═══════════════════════  TAROT-AI  ══════════════════════════╗
║ ┌─────────────────────────────────────────────────────────┐ ║
║ │  ▀█▀ ▄▀█ █▀█ █▀█ ▀█▀    ▄▀█ █    ▓▒░                  │ ║
║ │   █  █▀█ █▀▄ █▄█  █     █▀█ █    ░▒▓                  │ ║
║ │                                      v2.0               │ ║
║ └─────────────────────────────────────────────────────────┘ ║
║           ◈  Neural  Divination  Interface  ◈               ║
║     ╭───────────────────  ⚡  ───────────────────╮         ║
║     │    QUANTUM-ENHANCED HERMETIC PATTERNS      │         ║
║     ╰────────────────────────────────────────────╯         ║
╚══════════════════════════════════════════════════════════════╝"""

    def system_status(self) -> Panel:
        """Generate system status display"""
        status_text = "\n".join([
            "[white]╭──────────── SYSTEM STATUS ────────────╮[/]",
            "[white]│[/] [green]◉[/green] Neural Matrix    : [cyan]ONLINE[/cyan]       [white]│[/]",
            "[white]│[/] [green]◉[/green] Quantum Core     : [cyan]STABLE[/cyan]       [white]│[/]",
            "[white]│[/] [green]◉[/green] Arcane Protocols : [cyan]ACTIVATED[/cyan]    [white]│[/]",
            "[white]╰───────────────────────────────────────╯[/]"
        ])
        return Panel(status_text, border_style="cyan")

    def display_welcome(self):
        """Display welcome sequence"""
        self.console.print(self.welcome_banner())
        self.console.print(self.system_status())
        self.console.print(Panel(
            "[bold magenta]READY FOR DIVINATION SEQUENCE[/]\n"
            "[cyan]Enter your query to access the quantum-enhanced pattern matrix[/]",
            border_style="magenta",
            title="[bold cyan]≺ SYSTEM READY ≻[/]"
        ))

    def display_error(self, message: str, details: Optional[str] = None, 
                    exception: Optional[Exception] = None) -> None:
        """Display an error message with optional details and stack trace"""
        error_content = f"⛔ {message}"
        
        if details:
            error_content += f"\n\n{details}"
            
        if exception and self.config.dev_mode:
            import traceback
            error_content += "\n\n[bold]Stack Trace:[/]\n"
            error_content += "".join(traceback.format_exception(
                type(exception), exception, exception.__traceback__
            ))
            
        error_panel = Panel(
            Text(error_content, style=self.color_scheme['error']),
            title="[bold]ERROR[/]",
            border_style=self.color_scheme['error'],
            title_align="left"
        )
        self.console.print(error_panel)

    def display_loading(self, message: str) -> Status:
        """Display a loading spinner with message"""
        if self.config.dev_mode:
            message = f"[debug]DEV MODE: {message}[/]"
        return self.console.status(
            f"[{self.color_scheme['energy']}]{message}[/]",
            spinner="dots",
            spinner_style=self.color_scheme['energy']
        )

    def display_success(self, message: str) -> None:
        """Display a success message"""
        success_panel = Panel(
            Text(f"✅ {message}", style=self.color_scheme['status']),
            border_style=self.color_scheme['status']
        )
        self.console.print(success_panel)

    def display_voice_status(self, status: str) -> None:
        """Display voice interface status"""
        status_map = {
            "listening": "[bold green]🎤 Listening...[/]",
            "processing": "[bold yellow]🤖 Processing...[/]",
            "speaking": "[bold cyan]🗣 Speaking...[/]"
        }
        self.console.print(status_map.get(status, "[bold red]❌ Unknown status[/]"))

    def display_card(self, card: dict) -> Panel:
        """Display a single card with ASCII art"""
        card_ascii = self.ascii.render_card(
            number=str(card['number']),
            name=card['name'],
            symbols=[self.ascii.HERMETIC_SYMBOLS.get(s, s) for s in card['symbols']],
            art_lines=card['art_lines']
        )
        return Panel(card_ascii, border_style="cyan", style="bold white")

    def display_spread(self, cards: List[dict]):
        """Display a full spread of cards"""
        panels = [self.display_card(card) for card in cards]
        self.console.print(Align.center(Columns(panels)))

    def show_reading(self, reading: Reading) -> None:
        """Display the reading results"""
        if self.config.dev_mode:
            self.console.print(Panel(
                f"[debug]Reading ID: {reading.id}\n"
                f"Timestamp: {reading.timestamp}\n"
                f"Model: {reading.model}[/]",
                title="[bold yellow]DEV INFO[/]",
                border_style="yellow"
            ))
            
        # Convert reading cards to format needed for ASCII display
        cards_for_display = [
            {
                'number': idx + 1,
                'name': card[0],
                'symbols': ['moon', 'sun'],  # These could be determined by card type
                'art_lines': self._get_card_art(card[0])
            }
            for idx, card in enumerate(reading.cards)
        ]
        
        # Display ASCII art cards
        self.display_spread(cards_for_display)
        
        # Display interpretation
        self.console.print(Panel(
            reading.interpretation,
            title="[bold magenta]MYSTICAL INTERPRETATION[/bold magenta]",
            border_style="magenta"
        ))

    def _get_card_art(self, card_name: str) -> List[str]:
        """Generate ASCII art for a specific card"""
        # This could be expanded with custom art for each card
        return ["⚡ △ ⚡", "▲ ▼ ▲", "⚡ △ ⚡"]
