"""Validate card data against the CardMeaning schema"""
import json
from pathlib import Path
from typing import Dict, List

from tarotai.core.models.types import CardMeaning
from tarotai.core.errors import ValidationError

def validate_card_data(card_data: Dict) -> List[str]:
    """Validate a single card's data against the schema"""
    errors = []
    
    try:
        # Try to create a CardMeaning instance
        CardMeaning(**card_data)
    except ValidationError as e:
        for error in e.errors():
            errors.append(f"{error['loc']}: {error['msg']}")
    
    return errors

def validate_card_file(file_path: Path) -> Dict[str, List[str]]:
    """Validate all cards in a JSON file"""
    results = {}
    
    with open(file_path, 'r') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'cards' in data:
            cards = data['cards']
        else:
            cards = data
            
        for idx, card in enumerate(cards):
            errors = validate_card_data(card)
            if errors:
                card_name = card.get('name', f'Card {idx}')
                results[card_name] = errors
                
    return results

def main():
    """Main validation function"""
    file_path = Path("data/cards_ordered.json")
    print(f"Validating card data in {file_path}...")
    
    validation_results = validate_card_file(file_path)
    
    if validation_results:
        print("\nValidation errors found:")
        for card, errors in validation_results.items():
            print(f"\n{card}:")
            for error in errors:
                print(f"  - {error}")
    else:
        print("\nAll cards validated successfully!")

if __name__ == "__main__":
    main()
