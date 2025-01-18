"""Update embeddings for cards when schema changes"""
import json
from pathlib import Path
from typing import Any, Dict, List

from tarotai.ai.embeddings.manager import EmbeddingManager

def update_card_embeddings(card_data: Dict, embedding_manager: EmbeddingManager) -> Dict:
    """Update embeddings for a single card"""
    if "embeddings" not in card_data:
        card_data["embeddings"] = {}
        
    # Generate new embeddings if needed
    if "upright_meaning" in card_data and not card_data["embeddings"].get("upright"):
        card_data["embeddings"]["upright"] = embedding_manager.generate_embedding(
            card_data["upright_meaning"]
        )
        
    if "reversed_meaning" in card_data and not card_data["embeddings"].get("reversed"):
        card_data["embeddings"]["reversed"] = embedding_manager.generate_embedding(
            card_data["reversed_meaning"]
        )
        
    return card_data

def update_embeddings_file(file_path: Path, embedding_manager: EmbeddingManager) -> Dict[str, Any]:
    """Update embeddings for all cards in a file with progress tracking"""
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    updated_cards = []
    stats = {
        'total_cards': 0,
        'cards_updated': 0,
        'cards_skipped': 0,
        'errors': 0
    }
    
    for card in data.get('cards', []):
        stats['total_cards'] += 1
        try:
            updated_card = update_card_embeddings(card, embedding_manager)
            if any(updated_card['embeddings'].values()):
                stats['cards_updated'] += 1
            else:
                stats['cards_skipped'] += 1
            updated_cards.append(updated_card)
        except Exception as e:
            stats['errors'] += 1
            print(f"Error updating embeddings for {card.get('name')}: {str(e)}")
        
    # Update the file with new embeddings
    data['cards'] = updated_cards
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    """Main function for updating embeddings"""
    file_path = Path("data/cards_ordered.json")
    data_dir = Path("data/embeddings")  # Add this line
    
    # Create embeddings directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)
    
    embedding_manager = EmbeddingManager(data_dir)  # Pass data_dir here
    
    print(f"Updating embeddings in {file_path}...")
    update_embeddings_file(file_path, embedding_manager)
    print("Embeddings updated successfully!")

if __name__ == "__main__":
    main()
