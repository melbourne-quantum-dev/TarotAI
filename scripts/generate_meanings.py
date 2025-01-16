import json
import asyncio
from pathlib import Path
from tarotai.extensions.enrichment.clients import DeepSeekClient, VoyageClient
from typing import Dict, Any, List

SYSTEM_ROLE = """
You are an expert tarot interpreter with deep knowledge of:
- Golden Dawn traditions
- Astrological correspondences
- Psychological archetypes
- Modern applications
"""

INSTRUCTIONS = """
1. Provide concise, modern interpretations
2. Include psychological insights
3. Relate to common life situations
4. Use clear, accessible language
"""

FORMAT = """
Provide output as plain text with:
- 2-3 sentence meaning
- 1-2 practical applications
- 1 psychological insight
"""

UPRIGHT_PROMPT = """
{ROLE_CONTEXT}
{INSTRUCTIONS}
{FORMAT}

Generate an upright meaning for:
- Card: {card_name}
- Element: {element}
- Keywords: {keywords}
- Astrological: {astrological}
- Kabbalistic: {kabbalistic}
"""

REVERSED_PROMPT = """
{ROLE_CONTEXT}
{INSTRUCTIONS}
{FORMAT}

Generate a reversed meaning for:
- Card: {card_name}
- Upright Meaning: {upright_meaning}

Consider:
1. How the energy is blocked or distorted
2. Potential shadow aspects
3. Opportunities for growth
"""

ERROR_HANDLING = """
If unsure about interpretation:
1. Focus on core card symbolism
2. Provide multiple perspectives
3. Suggest further research areas
"""

async def generate_meanings(card: Dict[str, Any], ai_client: DeepSeekClient) -> Dict[str, Any]:
    """Generate upright and reversed meanings for a card."""
    # Prepare context variables
    context = {
        "ROLE_CONTEXT": SYSTEM_ROLE,
        "INSTRUCTIONS": INSTRUCTIONS,
        "FORMAT": FORMAT,
        **card
    }
    
    if not card.get("upright_meaning"):
        prompt = UPRIGHT_PROMPT.format(**context)
        card["upright_meaning"] = await ai_client.generate_response(prompt)
    
    if not card.get("reversed_meaning"):
        prompt = REVERSED_PROMPT.format(**context)
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
