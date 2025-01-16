import json
import asyncio
from pathlib import Path
from tarotai.extensions.enrichment.clients import DeepSeekClient, VoyageClient
from typing import Dict, Any, List

UPRIGHT_PROMPT = """
Generate an upright meaning for the {card_name} tarot card. 
The card is associated with {element} and represents {keywords}.
The astrological correspondence is {astrological}, and the Kabbalistic path is {kabbalistic}.
Provide a concise, modern interpretation.
"""

REVERSED_PROMPT = """
Generate a reversed meaning for the {card_name} tarot card.
The upright meaning is: {upright_meaning}.
Provide a concise, modern interpretation of the reversed energy.
"""

async def generate_meanings(card: Dict[str, Any], ai_client: DeepSeekClient) -> Dict[str, Any]:
    """Generate upright and reversed meanings for a card."""
    if not card.get("upright_meaning"):
        prompt = UPRIGHT_PROMPT.format(**card)
        card["upright_meaning"] = await ai_client.generate_response(prompt)
    
    if not card.get("reversed_meaning"):
        prompt = REVERSED_PROMPT.format(**card)
        card["reversed_meaning"] = await ai_client.generate_response(prompt)
    
    return card

async def generate_embeddings(card: Dict[str, Any], voyage_client: VoyageClient) -> Dict[str, Any]:
    """Generate embeddings for a card's meanings."""
    if not card.get("embeddings"):
        card["embeddings"] = {}
    
    if not card["embeddings"].get("upright"):
        card["embeddings"]["upright"] = await voyage_client.generate_embedding(card["upright_meaning"])
    
    if not card["embeddings"].get("reversed"):
        card["embeddings"]["reversed"] = await voyage_client.generate_embedding(card["reversed_meaning"])
    
    return card

async def process_cards(cards: List[Dict[str, Any]], ai_client: DeepSeekClient, voyage_client: VoyageClient) -> List[Dict[str, Any]]:
    """Process all cards to generate meanings and embeddings."""
    processed_cards = []
    for card in cards:
        try:
            card = await generate_meanings(card, ai_client)
            card = await generate_embeddings(card, voyage_client)
            processed_cards.append(card)
        except Exception as e:
            print(f"Error processing card {card.get('name')}: {str(e)}")
            processed_cards.append(card)  # Keep the original card data
    return processed_cards

def save_cards(cards: List[Dict[str, Any]], file_path: str) -> None:
    """Save processed cards to a JSON file."""
    with open(file_path, "w") as f:
        json.dump({"cards": cards}, f, indent=2)

async def main():
    # Load existing cards
    with open("data/cards_ordered.json") as f:
        cards = json.load(f)["cards"]
    
    # Initialize AI clients
    ai_client = DeepSeekClient()
    voyage_client = VoyageClient()
    
    # Process cards
    processed_cards = await process_cards(cards, ai_client, voyage_client)
    
    # Save updated cards
    save_cards(processed_cards, "data/cards_ordered.json")

if __name__ == "__main__":
    asyncio.run(main())
