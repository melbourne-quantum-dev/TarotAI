#!/usr/bin/env python3
"""
Card Schema Validation Script
Ensures all cards in cards_ordered.json follow the required schema.
"""
import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, ValidationError, Field

class GoldenDawnSection(BaseModel):
    title: str
    symbolism: List[str]
    reading_methods: List[str]
    reversed_notes: str
    shadow_aspects: List[str]

class CardEmbeddings(BaseModel):
    upright: List[float]
    reversed: List[float]

class CardMetadata(BaseModel):
    last_updated: str
    source: str
    confidence: float

class TarotCard(BaseModel):
    number: Optional[int]
    suit: Optional[str]
    name: str
    element: str
    astrological: str
    kabbalistic: str
    decan: Optional[str]
    keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
    golden_dawn: GoldenDawnSection
    embeddings: CardEmbeddings
    metadata: CardMetadata

def validate_card(card: Dict) -> List[str]:
    """Validate a single card against schema"""
    errors = []
    try:
        TarotCard(**card)
    except ValidationError as e:
        errors = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
    return errors

def validate_all_cards(cards_data: Dict) -> Dict[str, List[str]]:
    """Validate all cards in the dataset"""
    results = {}
    for card in cards_data["cards"]:
        errors = validate_card(card)
        if errors:
            results[card.get("name", "Unknown")] = errors
    return results

def main():
    """Main validation routine"""
    cards_path = Path("data/cards_ordered.json")
    
    try:
        with open(cards_path) as f:
            cards_data = json.load(f)
            
        validation_results = validate_all_cards(cards_data)
        
        if validation_results:
            print("Validation errors found:")
            for card_name, errors in validation_results.items():
                print(f"\n{card_name}:")
                for error in errors:
                    print(f"  - {error}")
            raise SystemExit(1)
        else:
            print("All cards validated successfully!")
            
    except Exception as e:
        print(f"Validation failed: {str(e)}")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
