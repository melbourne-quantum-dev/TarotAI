from rich.table import Table
from rich.panel import Panel
from .core.types import Reading

class TarotDisplay:
    def __init__(self):
        from rich.console import Console
        self.console = Console()

    def display_welcome(self):
        """Display welcome banner"""
        self.console.print("[bold magenta]✨ Welcome to TarotAI ✨[/]")
        self.console.print("[cyan]Your neural-enhanced tarot experience[/]")

    def show_reading(self, reading: Reading) -> None:
        """Display the reading results"""
        table = Table(
            title=f"[bold magenta]{reading.spread} Reading[/]",
            border_style="cyan",
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Position", style="cyan")
        table.add_column("Card", style="green")
        table.add_column("Orientation", style="yellow")
        
        for position, (card, orientation) in enumerate(reading.cards, start=1):
            table.add_row(
                f"Position {position}",
                card,
                "Reversed" if orientation else "Upright"
            )
        
        self.console.print(table)
        self.console.print(Panel(
            reading.interpretation,
            title="[bold cyan]Interpretation[/]",
            border_style="magenta"
        ))
