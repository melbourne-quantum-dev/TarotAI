from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.box import DOUBLE
from .core.types import Reading

class TarotDisplay:
    def __init__(self):
        self.console = Console()
        self.color_scheme = {
            'system': 'cyan',     # Core infrastructure
            'energy': 'magenta',  # Mystical elements
            'status': 'green',    # System states
            'border': 'white'     # Boundaries
        }

    def display_welcome(self):
        """Render the cyberpunk-hermetic welcome interface."""
        # ASCII Banner
        banner = Text(
            "╔═══ TAROT.SYS ═══╗\n"
            "║  Neural Matrix  ║\n"
            "║  Quantum Core   ║\n"
            "║  Arcane Proto   ║\n"
            "╚════════════════╝",
            style=f"bold {self.color_scheme['system']}"
        )

        # Status Matrix
        status_table = Table(
            box=DOUBLE,
            border_style=self.color_scheme['border'],
            header_style=f"bold {self.color_scheme['system']}"
        )
        status_table.add_column("STATUS", justify="left")
        status_table.add_row(f"▰ Neural   : [bold {self.color_scheme['status']}]ONLINE")
        status_table.add_row(f"▰ Quantum  : [bold {self.color_scheme['status']}]STABLE")
        status_table.add_row(f"▰ Arcane   : [bold {self.color_scheme['status']}]ACTIVE")

        # Boot Sequence
        boot_steps = [
            f"[{self.color_scheme['energy']}]Neural Pathways[/]",
            f"[{self.color_scheme['energy']}]Quantum Harmonics[/]",
            f"[{self.color_scheme['energy']}]Arcane Protocols[/]"
        ]
        boot_panel = Panel(
            "\n".join(boot_steps),
            title="[bold]BOOT SEQUENCE[/]",
            border_style=self.color_scheme['border'],
            title_align="left"
        )

        # Render Components
        self.console.print(banner, justify="center")
        self.console.print(status_table, justify="center")
        self.console.print(boot_panel, justify="center")
        self.console.print(
            f"[bold {self.color_scheme['system']}]TAROT.SYS READY[/]",
            justify="center"
        )

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
