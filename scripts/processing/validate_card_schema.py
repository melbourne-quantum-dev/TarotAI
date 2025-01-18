"""Validate card data against the CardMeaning schema and processing stages"""
import json
from pathlib import Path
from typing import Dict, List, Tuple

from tarotai.core.models.types import CardMeaning
from tarotai.core.errors import ValidationError

def validate_card_data(card_data: Dict) -> Tuple[List[str], List[str]]:
    """Validate a single card's data against the schema and processing stages
    
    Returns:
        Tuple of (errors, warnings) where:
        - errors are schema violations that must be fixed
        - warnings are for empty fields that will be populated in processing
    """
    errors = []
    warnings = []
    
    try:
        # Normalize suit to lowercase if present
        if 'suit' in card_data and isinstance(card_data['suit'], str):
            card_data['suit'] = card_data['suit'].lower()
            
        # Try to create a CardMeaning instance
        CardMeaning(**card_data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(f"{error['loc']}: {error['msg']}")
    
    # Check for empty fields that will be populated in processing
    processing_fields = {
        'keywords': 'generate-cards',
        'upright_meaning': 'generate-cards', 
        'reversed_meaning': 'generate-cards',
        'golden_dawn': 'process-golden-dawn',
        'embeddings': 'update-embeddings'
    }
    
    for field, stage in processing_fields.items():
        if not card_data.get(field):
            warnings.append(f"{field} will be populated by {stage}")
            
    # Validate Golden Dawn structure if present
    if 'golden_dawn' in card_data and isinstance(card_data['golden_dawn'], dict):
        gd = card_data['golden_dawn']
        if not gd.get('title'):
            warnings.append("golden_dawn.title will be populated by process-golden-dawn")
        if not gd.get('symbolism'):
            warnings.append("golden_dawn.symbolism will be populated by process-golden-dawn")
        if not gd.get('reading_methods'):
            warnings.append("golden_dawn.reading_methods will be populated by process-golden-dawn")
            
    # Validate embeddings structure if present
    if 'embeddings' in card_data and isinstance(card_data['embeddings'], dict):
        emb = card_data['embeddings']
        if not emb.get('upright'):
            warnings.append("embeddings.upright will be populated by update-embeddings")
        if not emb.get('reversed'):
            warnings.append("embeddings.reversed will be populated by update-embeddings")
    
    return errors, warnings

def validate_card_file(file_path: Path) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Validate all cards in a JSON file
    
    Returns:
        Tuple of (errors, warnings) where:
        - errors is dict of card name to list of schema errors
        - warnings is dict of card name to list of processing warnings
    """
    errors = {}
    warnings = {}
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'cards' in data:
            cards = data['cards']
        else:
            cards = data
            
        for idx, card in enumerate(cards):
            card_errors, card_warnings = validate_card_data(card)
            card_name = card.get('name', f'Card {idx}')
            
            if card_errors:
                errors[card_name] = card_errors
            if card_warnings:
                warnings[card_name] = card_warnings
                
    return errors, warnings

def main():
    """Main validation function"""
    file_path = Path("data/cards_ordered.json")
    print(f"Validating card data in {file_path}...")
    
    errors, warnings = validate_card_file(file_path)
    
    if errors:
        print("\nValidation errors found (must be fixed):")
        for card, card_errors in errors.items():
            print(f"\n{card}:")
            for error in card_errors:
                print(f"  - {error}")
    else:
        print("\nNo schema validation errors found!")
        
    if warnings:
        print("\nProcessing warnings (will be populated):")
        for card, card_warnings in warnings.items():
            print(f"\n{card}:")
            for warning in card_warnings:
                print(f"  - {warning}")
    else:
        print("\nAll fields are populated!")

if __name__ == "__main__":
    main()
