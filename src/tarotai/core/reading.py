from typing import List, Tuple, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from .types import CardMeaning, CardEmbeddings, ReadingEmbeddings
from .deck import TarotDeck


class ReadingInput:
    """Base class for reading input methods"""
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        raise NotImplementedError
        
    async def analyze_combinations(self, ai_client) -> Dict[str, Any]:
        """Analyze card combinations using tool calling"""
        tools = [
            {
                "name": "analyze_card_combinations",
                "description": "Analyze interactions between cards",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cards": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        ]
        
        card_names = [card[0].name for card in self.get_cards()]
        return await ai_client.generate_response(
            f"Analyze these card combinations: {', '.join(card_names)}",
            tools=tools,
            tool_choice="auto"
        )
        
    async def generate_embeddings(self, voyage_client) -> Optional[ReadingEmbeddings]:
        """Generate hierarchical embeddings for the reading"""
        cards = self.get_cards()
        
        # Generate text embeddings for cards
        text_embeddings = await voyage_client.generate_batch_embeddings(
            [card[0].upright_meaning for card in cards]
        )
        
        # Generate multimodal embeddings if images are available
        card_embeddings = []
        for card, text_embedding in zip(cards, text_embeddings):
            embeddings = CardEmbeddings(text_embedding=text_embedding)
            
            if card[0].image_url:
                content = [
                    {"type": "text", "text": card[0].upright_meaning},
                    {"type": "image_url", "image_url": card[0].image_url}
                ]
                embeddings.multimodal_embedding = await voyage_client.generate_multimodal_embedding(content)
                
            card_embeddings.append(embeddings)
        
        # Generate position embeddings
        position_embeddings = await voyage_client.generate_batch_embeddings(
            [f"Position {i}" for i in range(len(cards))]
        )
        
        # Generate context embedding
        context = " ".join(card[0].upright_meaning for card in cards)
        context_embedding = await voyage_client.generate_embedding(context)
        
        return ReadingEmbeddings(
            card_embeddings=card_embeddings,
            position_embeddings=position_embeddings,
            context_embedding=context_embedding
        )

class RandomDrawInput(ReadingInput):
    """Input method using random card draw"""
    def __init__(self, deck: TarotDeck, count: int):
        self.deck = deck
        self.count = count
        
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        return self.deck.draw(self.count)

class ManualInput(ReadingInput):
    """Input method for manual card entry"""
    def __init__(self, deck: TarotDeck, cards: List[Tuple[str, bool]]):
        self.deck = deck
        self.card_names = [name for name, _ in cards]
        self.reversed = [rev for _, rev in cards]
        
    def get_cards(self) -> List[Tuple[CardMeaning, bool]]:
        return [
            (self.deck.get_card_by_name(card_name), is_reversed)
            for card_name, is_reversed in zip(self.card_names, self.reversed)
        ]
