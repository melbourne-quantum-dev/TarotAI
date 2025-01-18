#!/usr/bin/env python3
"""
Data Validation Script
"""
import json
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from tarotai.core.models.card import TarotCard
from tarotai.core.models.deck import TarotDeck
from tarotai.core.models.types import CardSuit
from tarotai.core.logging import setup_logging

# Setup logging
logger = setup_logging()
console = Console()

REQUIRED_CARD_FIELDS = [
    "name", "number", "suit", 
    "keywords", "upright_meaning", 
    "reversed_meaning", "golden_dawn", 
    "embeddings"
]

def validate_card(card_data: Dict) -> List[str]:
    """Validate a single card's data"""
    errors = []
    
    # Check required fields
    for field in REQUIRED_CARD_FIELDS:
        if field not in card_data:
            errors.append(f"Missing required field: {field}")
            
    # Validate suit
    if "suit" in card_data:
        try:
            CardSuit(card_data["suit"])
        except ValueError:
            errors.append(f"Invalid suit: {card_data['suit']}")
            
    # Validate number range
    if "number" in card_data:
        number = card_data["number"]
        if not isinstance(number, int):
            errors.append("Card number must be integer")
        elif number < 0 or number > 21:
            errors.append("Card number must be between 0 and 21")
            
    # Validate golden_dawn structure
    if "golden_dawn" in card_data:
        gd = card_data["golden_dawn"]
        if not isinstance(gd, dict):
            errors.append("golden_dawn must be a dictionary")
        else:
            required_gd_fields = ["title", "symbolism", "reading_methods"]
            for field in required_gd_fields:
                if field not in gd:
                    errors.append(f"Missing golden_dawn field: {field}")
                    
    # Validate embeddings structure
    if "embeddings" in card_data:
        emb = card_data["embeddings"]
        if not isinstance(emb, dict):
            errors.append("embeddings must be a dictionary")
        else:
            required_emb_fields = ["upright", "reversed"]
            for field in required_emb_fields:
                if field not in emb:
                    errors.append(f"Missing embeddings field: {field}")
                    
    return errors

def validate_deck(deck_path: Path) -> Dict[str, List[str]]:
    """Validate an entire deck file"""
    validation_results = {
        "cards": {},
        "deck_errors": []
    }
    
    try:
        # Load and validate deck
        deck = TarotDeck(deck_path)
        
        # Check card count
        if len(deck.cards) != 78:
            validation_results["deck_errors"].append(
                "Deck should contain exactly 78 cards"
            )
            
        # Validate each card
        for card in deck.cards:
            errors = validate_card(card.dict())
            if errors:
                validation_results["cards"][card.name] = errors
                
    except Exception as e:
        validation_results["deck_errors"].append(
            f"Failed to load deck: {str(e)}"
        )
        
    return validation_results

def display_results(results: Dict, deck_path: Path) -> None:
    """Display validation results"""
    table = Table(title=f"Validation Results for {deck_path.name}", show_header=True)
    table.add_column("Card", style="cyan")
    table.add_column("Errors", style="red")
    
    # Show card errors
    for card_name, errors in results["cards"].items():
        table.add_row(card_name, "\n".join(errors))
        
    # Show deck errors
    if results["deck_errors"]:
        console.print("\n[bold red]Deck-Level Errors:[/]")
        for error in results["deck_errors"]:
            console.print(f"  - {error}")
            
    console.print(table)
    
    # Summary
    total_errors = sum(len(errors) for errors in results["cards"].values())
    total_errors += len(results["deck_errors"])
    console.print(f"\n[bold]Total Errors Found:[/] {total_errors}")

def main():
    """Main validation function"""
    try:
        deck_path = Path("data/cards_ordered.json")
        if not deck_path.exists():
            raise FileNotFoundError(f"Deck file not found at {deck_path}")
            
        # Run validation
        results = validate_deck(deck_path)
        
        # Display results
        display_results(results, deck_path)
        
        # Save results
        results_path = Path("data/validation_results.json")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved validation results to {results_path}")
        
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
