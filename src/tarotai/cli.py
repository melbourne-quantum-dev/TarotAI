import typer
import questionary
from typing import Optional, Callable
from pathlib import Path
from .display import TarotDisplay
from .interface import TarotInterface
from .reader import TarotReader
from .core.voice import TarotVoice

app = typer.Typer()

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
    """Perform a tarot reading"""
    display = TarotDisplay()
    interface = TarotInterface()
    reader = TarotReader(display)
    
    try:
        # Display welcome sequence
        display.display_welcome()
        
        # Validate inputs
        if not spread_type:
            raise typer.BadParameter("Spread type is required")
        if not focus:
            raise typer.BadParameter("Focus area is required")
        if not question:
            raise typer.BadParameter("Question is required")
            
        # Normalize inputs
        spread_type = spread_type.strip().title()
        focus = focus.strip().title()
            
        # Execute reading
        reading = reader.execute_reading(spread_type, focus, question)
        
        # Display results
        display.show_reading(reading)
        
    except KeyboardInterrupt:
        display.console.print("\n[bold red]✘ Reading cancelled[/]")
        raise typer.Abort()

@app.command()
def interactive():
    """Start interactive tarot session"""
    display = TarotDisplay()
    interface = TarotInterface()
    reader = TarotReader(display)
    
    try:
        display.display_welcome()
        while True:
            spread_type, focus, question = interface.gather_context()
            reading = reader.execute_reading(spread_type, focus, question)
            display.show_reading(reading)
            
            if not questionary.confirm(
                "Perform another reading?",
                default=False
            ).ask():
                break
                
    except KeyboardInterrupt:
        display.console.print("\n[bold red]✘ Session ended[/]")
        raise typer.Abort()

@app.command()
def voice(
    spread_type: Optional[str] = typer.Option(None, help="Type of spread to use"),
    focus: Optional[str] = typer.Option(None, help="Temporal focus of reading"),
    question: Optional[str] = typer.Option(None, help="Question for the reading")
):
    """Perform a tarot reading using voice commands"""
    display = TarotDisplay()
    interface = TarotInterface()
    reader = TarotReader(display)
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
