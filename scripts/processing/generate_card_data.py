"""Generate complete card data structure from raw inputs"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from tarotai.core.models.types import CardMeaning

def generate_card_template() -> Dict:
    """Generate a template for new card data"""
    return {
        "name": "",
        "number": None,
        "suit": "",
        "keywords": [],
        "upright_meaning": "",
        "reversed_meaning": "",
        "element": None,
        "astrological": None,
        "kabbalistic": None,
        "decan": None,
        "golden_dawn": {
            "title": "",
            "symbolism": [],
            "reading_methods": [],
            "reversed_notes": "",
            "shadow_aspects": []
        },
        "embeddings": {
            "upright": [],
            "reversed": []
        },
        "metadata": {
            "last_updated": datetime.now().isoformat(),
            "source": "generated",
            "confidence": 1.0
        }
    }

def process_card(card_data: Dict) -> Dict:
    """Process and validate a single card's data"""
    template = generate_card_template()
    
    # Update template with provided data
    for key, value in card_data.items():
        if key in template:
            template[key] = value
            
    # Validate the card
    try:
        CardMeaning(**template)
        return template
    except Exception as e:
        print(f"Error processing card {card_data.get('name')}: {str(e)}")
        return None

def generate_card_data(input_file: Path, output_file: Path) -> None:
    """Generate complete card data from input file"""
    with open(input_file, 'r') as f:
        raw_data = json.load(f)
        
    processed_cards = []
    for card in raw_data.get('cards', []):
        processed = process_card(card)
        if processed:
            processed_cards.append(processed)
            
    output_data = {
        "version": "2.0.0",
        "last_updated": datetime.now().isoformat(),
        "schema_version": "1.0",
        "cards": processed_cards
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

def main():
    """Main function for generating card data"""
    input_file = Path("data/cards_ordered.json")  # Changed from raw_cards.json
    output_file = Path("data/cards_ordered.json")  # Output to the same file
    
    print(f"Generating card data from {input_file}...")
    generate_card_data(input_file, output_file)
    print(f"Saved processed card data to {output_file}")

if __name__ == "__main__":
    main()
