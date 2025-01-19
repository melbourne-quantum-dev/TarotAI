#!/usr/bin/env python3
"""Generate card meanings from Golden Dawn correspondences."""

import json
from pathlib import Path
import logging
import sys
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_golden_dawn_data() -> Dict[str, Any]:
    """Load Golden Dawn correspondences from JSON."""
    data_path = Path(__file__).parent.parent.parent / 'data' / 'golden_dawn.json'
    try:
        with open(data_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Golden Dawn data file not found at: {data_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in Golden Dawn data file")
        sys.exit(1)

def generate_base_meanings() -> Dict[str, Any]:
    """Generate base meanings for all cards."""
    gd_data = load_golden_dawn_data()
    meanings = {}
    
    # Process Major Arcana
    for card in gd_data['major_arcana']:
        meanings[card['name']] = {
            'title': card['title'],
            'hebrew_letter': card['hebrew_letter'],
            'astrological': card['astrological'],
            'element': card.get('element'),
            'path': card['path'],
            'meanings': {
                'upright': card['meanings']['upright'],
                'reversed': card['meanings']['reversed']
            }
        }
    
    # Process Minor Arcana
    for suit in gd_data['minor_arcana']:
        for card in suit['cards']:
            meanings[f"{card['rank']} of {suit['name']}"] = {
                'element': suit['element'],
                'decan': card.get('decan'),
                'planetary': card.get('planetary'),
                'zodiacal': card.get('zodiacal'),
                'meanings': {
                    'upright': card['meanings']['upright'],
                    'reversed': card['meanings']['reversed']
                }
            }
    
    return meanings

def save_meanings(meanings: Dict[str, Any]) -> None:
    """Save generated meanings to JSON file."""
    output_path = Path(__file__).parent.parent.parent / 'data' / 'cards_ordered.json'
    try:
        with open(output_path, 'w') as f:
            json.dump(meanings, f, indent=2)
        logger.info(f"Card meanings saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save meanings: {str(e)}")
        sys.exit(1)

def main() -> int:
    """Main entry point."""
    try:
        logger.info("Generating card meanings from Golden Dawn correspondences...")
        meanings = generate_base_meanings()
        save_meanings(meanings)
        logger.info("✨ Card meanings generated successfully!")
        return 0
    except Exception as e:
        logger.error(f"Failed to generate meanings: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())