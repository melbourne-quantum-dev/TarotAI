import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from typing import Dict, Any

from tarotai.ai.clients.unified import UnifiedAIClient
from tarotai.config.schemas.config import AISettings
from tarotai.ai.prompts.manager import PromptTemplateManager

class CardGenerator:
    def __init__(self, ai_client: UnifiedAIClient):
        self.ai_client = ai_client
        self.prompt_manager = PromptTemplateManager()
        
    async def generate_card_data(self, card_data: Dict) -> Dict:
        """Generate complete card data using templates"""
        try:
            # Render the template with card data
            template = self.prompt_manager.get_template("card_generation")
            context = {
                "card": card_data,
                "system_role": SYSTEM_ROLE,
                "instructions": INSTRUCTIONS
            }
            
            # Get AI-generated content
            generated_data = await self.ai_client.json_prompt(
                template.render(**context)
            )
            
            # Merge with base data
            card_data.update(generated_data)
            
            # Add metadata
            card_data["metadata"] = {
                "last_updated": datetime.now().isoformat(),
                "source": "generated",
                "confidence": 0.95
            }
            
            # Validate the generated data
            CardMeaning(**card_data)
            
            return card_data
            
        except Exception as e:
            print(f"Error generating data for {card_data.get('name')}: {str(e)}")
            return None

async def generate_base_deck(ai_client: UnifiedAIClient) -> List[Dict]:
    """Generate the base 78-card deck structure using templates"""
    generator = CardGenerator(ai_client)
    deck = []
    
    # Major Arcana
    for i in range(22):
        card_data = {
            "name": f"Major Arcana {i}",
            "number": i,
            "suit": "Major",
            "element": None,
            "astrological": None,
            "kabbalistic": None
        }
        deck.append(await generator.generate_card_template(card_data))
        
    # Minor Arcana
    suits = ["Wands", "Cups", "Swords", "Pentacles"]
    for suit in suits:
        # Numbered cards
        for i in range(1, 11):
            card_data = {
                "name": f"{i} of {suit}",
                "number": i,
                "suit": suit,
                "element": _get_element(suit),
                "astrological": None,
                "kabbalistic": None
            }
            deck.append(await generator.generate_card_template(card_data))
            
        # Court cards
        court = ["Page", "Knight", "Queen", "King"]
        for rank in court:
            card_data = {
                "name": f"{rank} of {suit}",
                "number": None,
                "suit": suit,
                "element": _get_element(suit),
                "astrological": None,
                "kabbalistic": None
            }
            deck.append(await generator.generate_card_template(card_data))
            
    return deck

def _get_element(suit: str) -> str:
    """Get element for a suit"""
    elements = {
        "Wands": "Fire",
        "Cups": "Water",
        "Swords": "Air",
        "Pentacles": "Earth"
    }
    return elements.get(suit)

async def merge_golden_dawn_data(cards_path: Path, golden_dawn_path: Path):
    """Merge Golden Dawn data with existing cards"""
    with open(cards_path) as f:
        cards = json.load(f)["cards"]
        
    with open(golden_dawn_path) as f:
        golden_dawn = json.load(f)
        
    for card in cards:
        gd_info = golden_dawn.get(card["name"], {})
        if gd_info:
            card["golden_dawn"] = {
                "title": gd_info.get("title"),
                "symbolism": gd_info.get("symbolism"),
                "reading_methods": gd_info.get("reading_methods")
            }
            
    with open(cards_path, "w") as f:
        json.dump({"cards": cards}, f, indent=2)

async def main():
    """Main function for generating card meanings"""
    # Initialize components
    config = AISettings.create_default()
    ai_client = UnifiedAIClient(config)
    
    # Load existing cards
    with open("data/cards_ordered.json") as f:
        cards = json.load(f)["cards"]
    
    # Process cards in batches
    processed_cards = await process_cards(cards, ai_client)
    
    # Save results
    output = {
        "version": "2.0.0",
        "last_updated": datetime.now().isoformat(),
        "schema_version": "1.0",
        "cards": processed_cards
    }
    
    with open("data/cards_ordered.json", "w") as f:
        json.dump(output, f, indent=2)

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
    """Generate keywords for a card using AI"""
    prompt = f"""
    Generate 3-5 keywords for {card['name']} considering:
    - Element: {card['element']}
    - Suit: {card['suit']}
    - Number: {card['number']}
    
    Return as JSON list.
    """
    return await ai_client.json_prompt(prompt)

async def generate_meanings(card: Dict[str, Any], ai_client: UnifiedAIClient, golden_dawn: Dict) -> Dict[str, Any]:
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

async def generate_embeddings(card: Dict[str, Any], ai_client: UnifiedAIClient) -> Dict[str, Any]:
    """Generate embeddings for a card's meanings."""
    if not card.get("embeddings"):
        card["embeddings"] = {}
    
    if not card["embeddings"].get("upright"):
        card["embeddings"]["upright"] = await ai_client.generate_embedding(card["upright_meaning"])
    
    if not card["embeddings"].get("reversed"):
        card["embeddings"]["reversed"] = await ai_client.generate_embedding(card["reversed_meaning"])
    
    return card

async def process_cards(cards: List[Dict[str, Any]], ai_client: UnifiedAIClient) -> List[Dict[str, Any]]:
    """Process all cards to generate meanings and embeddings"""
    generator = CardGenerator(ai_client)
    processed_cards = []
    
    for card in cards:
        try:
            # Generate complete card data
            processed_card = await generator.generate_card_data(card)
            if processed_card:
                processed_cards.append(processed_card)
                
            # Generate embeddings if needed
            if not processed_card.get("embeddings", {}).get("upright"):
                processed_card["embeddings"]["upright"] = await ai_client.generate_embedding(
                    processed_card["upright_meaning"]
                )
                
            if not processed_card.get("embeddings", {}).get("reversed"):
                processed_card["embeddings"]["reversed"] = await ai_client.generate_embedding(
                    processed_card["reversed_meaning"]
                )
                
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

async def process_all_cards(skip_pdf_processing: bool = True):
    # Initialize components
    config = AISettings.create_default()
    ai_client = UnifiedAIClient(config)
    
    # Use default knowledge instead of Golden Dawn
    print("Using default knowledge base")
    golden_dawn = DEFAULT_KNOWLEDGE
    
    # Load cards
    with open("data/cards_ordered.json") as f:
        cards = json.load(f)["cards"]
    
    # Process in batches
    for i in range(0, len(cards), 5):
        batch = cards[i:i+5]
        for card in batch:
            try:
                # Generate keywords if missing
                if not card["keywords"]:
                    card["keywords"] = await generate_keywords(card, ai_client, golden_dawn)
                
                # Generate meanings if missing
                if not card["upright_meaning"]:
                    meanings = await generate_meanings(card, ai_client, golden_dawn)
                    card.update(meanings)
                
                # Add default references
                card["golden_dawn"] = {
                    "title": card.get("name"),
                    "symbolism": [],
                    "reading_methods": DEFAULT_KNOWLEDGE["reading_methods"]
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
