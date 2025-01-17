import typer
import questionary
from typing import Optional, Callable, List
from pathlib import Path
from rich.panel import Panel
from .display import TarotDisplay
from .core.voice import TarotVoice
from .core.deck import TarotDeck
from .core.reading import RandomDrawInput, ManualInput
from .core.interpreter import TarotInterpreter

app = typer.Typer(
    help="TarotAI - Neural-Enhanced Tarot Reading System",
    rich_markup_mode="markdown",
    no_args_is_help=True
)

@app.callback()
def main_callback():
    """
    ## TarotAI CLI
    
    A modern tarot reading system combining traditional divination with AI-powered insights.
    """

@app.command()
def read(
    spread_type: Optional[str] = typer.Option(
        None,
        help="Type of spread to use (e.g. 'Celtic Cross', 'Three Card', 'Horseshoe')",
        prompt="What spread would you like to use?"
    ),
    focus: Optional[str] = typer.Option(
        None,
        help="Focus area for the reading (e.g. 'Career', 'Relationships', 'Personal Growth')",
        prompt="What is the focus of your reading?"
    ),
    question: Optional[str] = typer.Option(
        None,
        help="Your specific question or area of inquiry",
        prompt="What is your question or area of focus?"
    )
):
    """
    Perform a tarot reading with the specified parameters.
    """
    display = TarotDisplay()
    
    try:
        with display.display_loading("Initializing quantum divination matrix..."):
            interpreter = TarotInterpreter()
            
            # Validate inputs
            if not all([spread_type, focus, question]):
                display.display_error("Missing required parameters")
                raise typer.Exit(code=1)
                
            # Create reading input
            deck = TarotDeck(Path("data/cards_ordered.json"))
            input_method = RandomDrawInput(deck, count=3)
            
            # Execute reading
            interpreter = TarotInterpreter()
            results = list(interpreter.interpret_reading(
                input_method,
                question=question,
                show_static=True
            ))
            
            # Display results with new theme
            display.console.print("\n[bold magenta]✨ THE CARDS SPEAK ✨[/bold magenta]")
            for result in results:
                if result["type"] == "static_meanings":
                    display.console.print(Panel(
                        result["content"],
                        title="[bold cyan]ARCANE KNOWLEDGE[/bold cyan]",
                        border_style="magenta"
                    ))
                else:
                    display.console.print(Panel(
                        result["content"],
                        title="[bold magenta]QUANTUM INTERPRETATION[/bold magenta]",
                        border_style="cyan"
                    ))
            
    except Exception as e:
        display.display_error("Reading failed", str(e))
        raise typer.Exit(code=1)

@app.command()
def interactive():
    """Start interactive tarot session"""
    display = TarotDisplay()
    deck = TarotDeck(Path("data/cards_ordered.json"))
    interpreter = TarotInterpreter()
    
    try:
        display.display_welcome()
        
        # Welcome message
        display.console.print(Panel(
            "Welcome to TarotAI's interactive reading mode.\n"
            "I will guide you through the process of performing a tarot reading.\n\n"
            "Do you have a physical tarot deck in front of you? If so, I can guide you\n"
            "through selecting and interpreting your own cards.\n\n"
            "If not, I can perform a virtual reading for you.",
            title="[bold magenta]Welcome to TarotAI[/]",
            border_style="blue"
        ))
        
        while True:
            # Choose reading method
            reading_method = questionary.select(
                "How would you like to perform your reading?",
                choices=[
                    {"name": "Use my own tarot deck", "value": "manual"},
                    {"name": "Perform a virtual reading", "value": "virtual"},
                    {"name": "Exit", "value": "exit"}
                ]
            ).ask()
            
            if reading_method == "exit":
                break
                
            # Manual reading flow
            if reading_method == "manual":
                display.console.print(Panel(
                    "Wonderful! Let's perform a reading with your physical deck.\n\n"
                    "I'll guide you through each step:\n"
                    "1. Select your spread type\n"
                    "2. Shuffle and draw your cards\n"
                    "3. Enter each card and its orientation\n"
                    "4. Receive your interpretation\n\n"
                    "Let's begin!",
                    title="[bold cyan]Manual Reading Guide[/]",
                    border_style="green"
                ))
                
                # Get spread type
                spread_type = questionary.select(
                    "What spread would you like to use?",
                    choices=[
                        {"name": "Single Card", "value": "single"},
                        {"name": "Three Card (Past/Present/Future)", "value": "three_card"},
                        {"name": "Celtic Cross", "value": "celtic_cross"},
                        {"name": "Horseshoe", "value": "horseshoe"}
                    ]
                ).ask()
                
                spread_size = {
                    "single": 1,
                    "three_card": 3,
                    "celtic_cross": 10,
                    "horseshoe": 7
                }[spread_type]
                
                # Guide through card selection
                cards = []
                for i in range(spread_size):
                    display.console.print(Panel(
                        f"Step {i+1} of {spread_size}:\n"
                        "1. Shuffle your deck while focusing on your question\n"
                        "2. Draw a card from the top\n"
                        "3. Note whether it's upright or reversed\n"
                        "4. Enter the card details below",
                        title=f"[bold]Card {i+1} Selection[/]",
                        border_style="blue"
                    ))
                    
                    card_name = questionary.text(
                        f"Enter the name of card #{i+1}:",
                        validate=lambda text: len(text) > 0
                    ).ask()
                    
                    reversed = questionary.confirm(
                        "Is this card reversed?",
                        default=False
                    ).ask()
                    
                    cards.append((card_name, reversed))
                
                # Create manual input
                input_method = ManualInput(deck, cards)
                
            # Virtual reading flow
            else:
                input_method = RandomDrawInput(deck, count=3)
                
            # Get reading context
            if questionary.confirm("Would you like guidance on framing your question?").ask():
                display.console.print(Panel(
                    "Try to focus on open-ended questions that explore possibilities rather than yes/no answers.\n"
                    "Examples:\n"
                    "- What should I focus on in my career?\n" 
                    "- How can I improve my relationships?\n"
                    "- What lessons can I learn from my current situation?",
                    title="Question Guidance",
                    border_style="blue"
                ))

            focus = questionary.text("What is the focus of your reading?").ask()
            question = questionary.text("What is your question or area of focus?").ask()

            # Execute reading with loading indicators
            try:
                with display.display_loading("Shuffling cards..."):
                    deck.shuffle()
                
                with display.display_loading("Interpreting reading..."):
                    interpreter = TarotInterpreter()
                    results = list(interpreter.interpret_reading(
                        input_method,
                        question=question,
                        show_static=True
                    ))
                    
                # Display results
                display.console.print("\n[bold magenta]✨ THE CARDS SPEAK ✨[/bold magenta]")
                for result in results:
                    if result["type"] == "static_meanings":
                        display.console.print(Panel(
                            result["content"],
                            title="[bold cyan]ARCANE KNOWLEDGE[/bold cyan]",
                            border_style="magenta"
                        ))
                    else:
                        display.console.print(Panel(
                            result["content"],
                            title="[bold magenta]QUANTUM INTERPRETATION[/bold magenta]",
                            border_style="cyan"
                        ))
                        
            except Exception as e:
                display.display_error("Reading failed", str(e))
                if not questionary.confirm("Try again?").ask():
                    break
                continue
                
            if not questionary.confirm(
                "Perform another reading?",
                default=False
            ).ask():
                break
                
    except KeyboardInterrupt:
        display.console.print("\n[bold red]✘ Session ended[/]")
        raise typer.Abort()

@app.command()
def manual(
    cards: List[str] = typer.Argument(..., help="List of card names"),
    reversed: List[bool] = typer.Option([], "--reversed", "-r", help="Which cards are reversed"),
    focus: Optional[str] = typer.Option(None, help="Focus area for the reading"),
    question: Optional[str] = typer.Option(None, help="Your specific question")
):
    """Perform a reading with manually selected cards"""
    display = TarotDisplay()
    
    try:
        with display.display_loading("Preparing manual reading..."):
            # Create manual input
            deck = TarotDeck(Path("data/cards_ordered.json"))
            input_method = ManualInput(
                deck,
                cards=list(zip(cards, reversed))
            )
            
            # Execute reading
            interpreter = TarotInterpreter()
            results = list(interpreter.interpret_reading(
                input_method,
                question=question,
                show_static=True
            ))
            
            # Display results
            display.console.print("\n[bold magenta]✨ THE CARDS SPEAK ✨[/bold magenta]")
            for result in results:
                if result["type"] == "static_meanings":
                    display.console.print(Panel(
                        result["content"],
                        title="[bold cyan]ARCANE KNOWLEDGE[/bold cyan]",
                        border_style="magenta"
                    ))
                else:
                    display.console.print(Panel(
                        result["content"],
                        title="[bold magenta]QUANTUM INTERPRETATION[/bold magenta]",
                        border_style="cyan"
                    ))
            
    except Exception as e:
        display.display_error("Reading failed", str(e))
        raise typer.Exit(code=1)

@app.command()
def voice(
    spread_type: Optional[str] = typer.Option(None, help="Type of spread to use"),
    focus: Optional[str] = typer.Option(None, help="Temporal focus of reading"),
    question: Optional[str] = typer.Option(None, help="Question for the reading")
):
    """Perform a tarot reading using voice commands"""
    display = TarotDisplay()
    interpreter = TarotInterpreter()
    voice = TarotVoice()

    try:
        # Display welcome sequence
        display.display_welcome()
        
        def process_voice_command(text: str):
            display.console.print(f"\n[bold cyan]🎤 Heard:[/] {text}")
            
            # Process commands
            if "start reading" in text.lower():
                # Execute reading
                reading = reader.execute_reading(spread_type, focus, question)
                display.show_reading(reading)
                
                # Speak interpretation
                voice.speak(reading.interpretation)
                
            elif "stop" in text.lower():
                voice.stop_listening()
                raise typer.Exit()
                
        display.console.print("\n[bold green]🎤 Speak now... (say 'stop' to exit)[/]")
        voice.start_listening(process_voice_command)
        
    except KeyboardInterrupt:
        display.console.print("\n[bold red]✘ Voice session ended[/]")
        raise typer.Abort()

if __name__ == "__main__":
    app()
