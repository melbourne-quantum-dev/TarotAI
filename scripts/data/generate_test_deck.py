import json
from pathlib import Path
from typing import List, Dict
from tarotai.core.models.types import CardSuit
from tarotai.ai.clients import UnifiedAIClient
from tarotai.config.schemas.config import get_config

class TestDeckGenerator:
    """Generates a complete test deck following Golden Dawn order"""
    
    def __init__(self):
        self.config = get_config()
        self.ai_client = UnifiedAIClient(self.config)
        self.deck_structure = [
            # Aces
            (CardSuit.WANDS, [1]),
            (CardSuit.CUPS, [1]),
            (CardSuit.SWORDS, [1]),
            (CardSuit.PENTACLES, [1]),
            # Pips by decan
            (CardSuit.WANDS, range(5, 8)),
            (CardSuit.PENTACLES, range(8, 11)),
            (CardSuit.SWORDS, range(2, 5)),
            (CardSuit.CUPS, range(5, 8)),
            (CardSuit.WANDS, range(8, 11)),
            (CardSuit.PENTACLES, range(2, 5)),
            (CardSuit.SWORDS, range(5, 8)),
            (CardSuit.CUPS, range(8, 11)),
            (CardSuit.WANDS, range(2, 5)),
            (CardSuit.PENTACLES, range(5, 8)),
            (CardSuit.SWORDS, range(8, 11)),
            (CardSuit.CUPS, range(2, 5)),
            # Courts (Knight=11, Queen=12, King=13, Princess=14)
            (CardSuit.WANDS, range(11, 15)),
            (CardSuit.CUPS, range(11, 15)),
            (CardSuit.SWORDS, range(11, 15)),
            (CardSuit.PENTACLES, range(11, 15)),
            # Majors (0-XXI)
            (CardSuit.MAJOR, range(0, 22))
        ]
    
    async def generate_card_data(self, suit: CardSuit, number: int) -> Dict:
        """Generate card data using AI"""
        card_type = "Major Arcana" if suit == CardSuit.MAJOR else "Minor Arcana"
        prompt = f"""
        Generate tarot card data for a {card_type} card.
        Suit: {suit.value if suit != CardSuit.MAJOR else 'Major'}
        Number: {number}
        Include:
        - Name
        - Keywords
        - Upright meaning
        - Reversed meaning
        - Element
        - Astrological correspondence
        - Kabbalistic path
        - Golden Dawn symbolism
        - Embeddings (generate placeholders for now)
        Return as JSON.
        """
        card_data = await self.ai_client.json_prompt(prompt)
        
        # Add placeholder embeddings
        card_data['embeddings'] = {
            'upright': [0.0] * 768,
            'reversed': [0.0] * 768,
            'symbolism': [0.0] * 768
        }
        
        return card_data
    
    async def generate_deck(self) -> List[Dict]:
        """Generate complete deck following Golden Dawn order"""
        cards = []
        for suit, numbers in self.deck_structure:
            for number in numbers:
                card_data = await self.generate_card_data(suit, number)
                card_data.update({
                    "suit": suit.value,
                    "number": number,
                    "metadata": {
                        "source": "generated",
                        "version": "1.0"
                    }
                })
                cards.append(card_data)
        return cards
    
    async def save_deck(self, output_path: Path) -> None:
        """Generate and save complete deck"""
        deck = await self.generate_deck()
        with open(output_path, "w") as f:
            json.dump({"cards": deck}, f, indent=2)

async def main():
    generator = TestDeckGenerator()
    output_path = Path("data/test_deck.json")
    await generator.save_deck(output_path)
    print(f"Test deck generated at {output_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
