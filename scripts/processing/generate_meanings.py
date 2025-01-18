import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from tarotai.extensions.enrichment.clients import DeepSeekClient, VoyageClient
from tarotai.extensions.enrichment.knowledge.golden_dawn import GoldenDawnKnowledgeBase

SYSTEM_ROLE = """
You are an expert tarot interpreter with deep knowledge of:
- Golden Dawn traditions
- Astrological correspondences
- Psychological archetypes
- Modern applications
- Kabbalistic symbolism
- Elemental associations
- Decanic influences
"""

INSTRUCTIONS = """
1. Provide concise, modern interpretations
2. Include psychological insights
3. Relate to common life situations
4. Use clear, accessible language
5. Incorporate traditional symbolism
6. Consider elemental influences
7. Include practical advice
8. Maintain consistency with Golden Dawn tradition
"""

FORMAT = """
Provide output as plain text with:
- 2-3 sentence meaning
- 1-2 practical applications
- 1 psychological insight
- 1 traditional symbolism reference
- 1 elemental influence note
"""

UPRIGHT_PROMPT = """
You are an expert tarot interpreter with deep knowledge of Golden Dawn traditions.

Generate an upright meaning for the {card_name} tarot card considering:

- Element: {element}
- Astrological: {astrological}
- Kabbalistic: {kabbalistic}
- Golden Dawn Title: {golden_dawn_title}
- Traditional Symbolism: {symbolism}

Provide:
1. A concise modern interpretation
2. Practical applications
3. Psychological insights
4. Traditional symbolism references
5. Elemental influences

Format as plain text with clear sections.
"""

REVERSED_PROMPT = """
Generate a reversed meaning for {card_name} considering:

- Upright Meaning: {upright_meaning}
- Golden Dawn Reversed Interpretation: {reversed_notes}
- Shadow Aspects: {shadow_aspects}

Provide:
1. Blocked or distorted energy analysis
2. Shadow aspects
3. Growth opportunities
4. Practical advice for integration
"""

ERROR_HANDLING = """
If unsure about interpretation:
1. Focus on core card symbolism
2. Provide multiple perspectives
3. Suggest further research areas
"""

async def generate_keywords(card: Dict, ai_client, gd_info: Dict) -> List[str]:
    """Generate keywords for a card using AI and Golden Dawn knowledge"""
    prompt = f"""
    Generate 3-5 keywords for {card['name']} considering:
    - Element: {card['element']}
    - Astrological: {card['astrological']}
    - Kabbalistic: {card['kabbalistic']}
    - Golden Dawn Symbolism: {gd_info.get('symbolism', [])}
    - Traditional Meanings: {gd_info.get('traditional_meanings', [])}
    
    Return as JSON list.
    """
    return await ai_client.json_prompt(prompt)

async def generate_meanings(card: Dict[str, Any], ai_client: DeepSeekClient, golden_dawn: GoldenDawnKnowledgeBase) -> Dict[str, Any]:
    """Generate upright and reversed meanings for a card."""
    # Prepare context variables
    context = {
        "ROLE_CONTEXT": SYSTEM_ROLE,
        "INSTRUCTIONS": INSTRUCTIONS,
        "FORMAT": FORMAT,
        **card
    }
    
    # Generate keywords if missing
    if not card.get("keywords"):
        keywords_prompt = f"""
        Generate 3-5 keywords for {card['name']} considering:
        - Element: {card['element']}
        - Astrological: {card['astrological']}
        - Kabbalistic: {card['kabbalistic']}
        - Decan: {card.get('decan', 'N/A')}
        Return as JSON list.
        """
        card["keywords"] = await ai_client.json_prompt(keywords_prompt)
    
    # Generate meanings if missing
    if not card.get("upright_meaning"):
        prompt = UPRIGHT_PROMPT.format(**context)
        card["upright_meaning"] = await ai_client.generate_response(prompt)
    
    if not card.get("reversed_meaning"):
        prompt = REVERSED_PROMPT.format(**context)
        card["reversed_meaning"] = await ai_client.generate_response(prompt)
    
    # Add metadata
    card["metadata"] = {
        "last_updated": datetime.now().isoformat(),
        "source": "generated",
        "confidence": 0.95
    }
    
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

DEFAULT_KNOWLEDGE = {
    "reading_methods": {
        "Celtic Cross": {
            "description": "A classic 10-card spread for comprehensive readings.",
            "steps": ["Shuffle", "Draw 10 cards", "Interpret positions"],
            "positions": ["Present", "Challenge", "Past", "Future", "Above", "Below", "Advice", "External", "Hopes", "Outcome"]
        }
    },
    "historical_approaches": {
        "Waite": {
            "era": "Early 20th Century",
            "approach": "Symbolic and intuitive",
            "key_insights": ["Focus on imagery", "Blend of esoteric traditions"]
        }
    },
    "lore": {
        "Major Arcana": {
            "topic": "Major Arcana",
            "description": "The 22 cards representing life's spiritual journey.",
            "symbolism": ["Fool's Journey", "Archetypes"],
            "references": ["Book T", "Golden Dawn teachings"]
        }
    }
}

async def process_all_cards(skip_pdf_processing: bool = False):
    # Initialize components
    ai_client = DeepSeekClient()
    
    # Load Golden Dawn knowledge
    if skip_pdf_processing:
        print("Using default knowledge base")
        golden_dawn = DEFAULT_KNOWLEDGE
    else:
        golden_dawn_path = Path("data/processed/golden_dawn/golden_dawn_knowledge.json")
        if not golden_dawn_path.exists():
            raise FileNotFoundError(
                f"Golden Dawn knowledge file not found at {golden_dawn_path}. "
                "You must run process_golden_dawn.py first to create this file."
            )
        golden_dawn = GoldenDawnKnowledgeBase(str(golden_dawn_path))
    
    # Load cards
    with open("data/cards_ordered.json") as f:
        cards = json.load(f)["cards"]
    
    # Process in batches
    for i in range(0, len(cards), 5):
        batch = cards[i:i+5]
        for card in batch:
            try:
                # Get Golden Dawn knowledge
                gd_info = golden_dawn.get_card_info(card["name"])
                
                # Generate keywords if missing
                if not card["keywords"]:
                    card["keywords"] = await generate_keywords(card, ai_client, gd_info)
                
                # Generate meanings if missing
                if not card["upright_meaning"]:
                    meanings = await generate_meanings(card, ai_client, golden_dawn)
                    card.update(meanings)
                
                # Add Golden Dawn references
                card["golden_dawn"] = {
                    "title": gd_info.get("title"),
                    "symbolism": gd_info.get("symbolism"),
                    "reading_methods": golden_dawn.get_reading_methods(card["name"])
                }
            
            except Exception as e:
                print(f"Error processing {card['name']}: {str(e)}")
                continue
        
        # Save progress
        with open("data/cards_ordered.json", "w") as f:
            json.dump({"cards": cards}, f, indent=2)

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-pdf-processing",
        action="store_true",
        help="Skip PDF processing and use pre-processed data"
    )
    args = parser.parse_args()
    
    await process_all_cards(skip_pdf_processing=args.skip_pdf_processing)

if __name__ == "__main__":
    asyncio.run(main())
