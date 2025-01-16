import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
import anthropic
from voyageai import get_embedding

from tarotai.core.types import (
    CardMeaning, 
    Reading, 
    CardSuit,
    SpreadPosition,
    QuestionContext
)
from tarotai.core.exceptions import EnrichmentError, EmbeddingError
from tarotai.core.reading_history import ReadingHistoryManager

load_dotenv()

class TarotEnricher:
    def __init__(self, cards_file: Path = Path("data/cards_ordered.json")):
        self.cards_file = cards_file
        self.cards: List[CardMeaning] = self._load_cards()
        self.reading_manager = ReadingHistoryManager()
        self.embeddings_file = Path("data/embeddings.json")
        
        # Initialize AI clients
        self.claude = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.voyage_key = os.getenv("VOYAGE_API_KEY")

    def _load_cards(self) -> List[CardMeaning]:
        """Load cards from JSON file and validate against CardMeaning model."""
        try:
            with open(self.cards_file, 'r', encoding='utf-8') as f:
                raw_cards = json.load(f)["cards"]
            return [CardMeaning(**card) for card in raw_cards]
        except Exception as e:
            raise EnrichmentError(f"Failed to load cards: {str(e)}")

    def _save_cards(self) -> None:
        """Save enriched cards back to JSON file."""
        try:
            cards_dict = {"cards": [card.dict() for card in self.cards]}
            with open(self.cards_file, 'w', encoding='utf-8') as f:
                json.dump(cards_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise EnrichmentError(f"Failed to save cards: {str(e)}")

    def _save_embeddings(self, embeddings: Dict[str, List[float]]) -> None:
        """Save card embeddings to file."""
        try:
            with open(self.embeddings_file, 'w', encoding='utf-8') as f:
                json.dump(embeddings, f, indent=2)
        except Exception as e:
            raise EmbeddingError(f"Failed to save embeddings: {str(e)}")

    def record_reading(self, reading: Reading) -> None:
        """Record a new reading for future enrichment."""
        try:
            self.reading_manager.add_reading(reading)
        except Exception as e:
            raise EnrichmentError(f"Failed to record reading: {str(e)}")

    async def learn_from_readings(self, card_name: str) -> Dict[str, Any]:
        """Update card meanings based on reading history."""
        try:
            readings = self.reading_manager.get_readings_for_card(card_name)
            stats = self.reading_manager.get_card_statistics(card_name)
            
            if not readings:
                return {}
            
            return await self._analyze_reading_patterns(readings, card_name, stats)
        except Exception as e:
            raise EnrichmentError(f"Failed to learn from readings: {str(e)}")

    async def _analyze_reading_patterns(self, readings: List[Reading], card_name: str, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Use Claude to analyze patterns in readings for a specific card."""
        if not readings:
            return {}
            
        try:
            prompt = f"""
            Analyze these {len(readings)} tarot readings where the card '{card_name}' appeared.
            Consider:
            - Position patterns in spreads
            - Question contexts and themes
            - Interpretation effectiveness (based on feedback)
            - Correlations with other cards
            
            Card statistics:
            {json.dumps(stats, indent=2)}
            
            Provide a structured analysis with:
            1. Most common themes and contexts
            2. Position-specific meanings
            3. Successful interpretation patterns
            4. Suggested meaning refinements
            5. Notable card combinations and their significance
            
            Readings data:
            {json.dumps([r.dict() for r in readings], indent=2)}
            """
            
            response = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content)
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze readings: {str(e)}")

    async def analyze_temporal_patterns(self, card_name: str, time_range: str) -> Dict[str, Any]:
        """Analyze reading patterns for a card over a specified time range."""
        try:
            readings = self.reading_manager.get_readings_for_card(card_name, time_range)
            stats = self.reading_manager.get_card_statistics(card_name, time_range)
            
            prompt = f"""
            Analyze temporal patterns for the card '{card_name}' over the {time_range} time range.
            Consider:
            - Frequency of appearance
            - Changes in interpretation or significance
            - Seasonal or cyclical patterns
            
            Provide insights on:
            1. Overall trends
            2. Notable shifts in meaning or context
            3. Recommendations for future interpretations based on temporal patterns
            
            Card statistics:
            {json.dumps(stats, indent=2)}
            
            Readings data:
            {json.dumps([r.dict() for r in readings], indent=2)}
            """
            
            response = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content)
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze temporal patterns: {str(e)}")

    async def generate_reading_insights(self, reading: Reading) -> Dict[str, Any]:
        """Generate insights for a specific reading."""
        try:
            prompt = f"""
            Analyze this tarot reading and provide insights:
            {json.dumps(reading.dict(), indent=2)}
            
            Consider:
            1. Overall theme and energy of the reading
            2. Significant card combinations and their meanings
            3. How the cards interact with the question context
            4. Potential areas for further exploration or clarification
            
            Provide a structured analysis with:
            1. Key insights
            2. Suggested follow-up questions
            3. Potential action items for the querent
            """
            
            response = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content)
        except Exception as e:
            raise EnrichmentError(f"Failed to generate reading insights: {str(e)}")

    async def analyze_card_combinations(self, card_names: List[str]) -> Dict[str, Any]:
        """Analyze synergies and meanings for specific card combinations."""
        try:
            readings = self.reading_manager.get_readings_with_cards(card_names)
            
            prompt = f"""
            Analyze the combination of these tarot cards: {', '.join(card_names)}
            
            Consider:
            1. Frequency of this combination in readings
            2. Common themes or contexts when these cards appear together
            3. How the cards' energies interact and influence each other
            4. Unique insights provided by this specific combination
            
            Provide a structured analysis with:
            1. Overall significance of the combination
            2. Potential interpretations in different contexts
            3. Advice for reading this combination effectively
            
            Relevant readings data:
            {json.dumps([r.dict() for r in readings], indent=2)}
            """
            
            response = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return json.loads(response.content)
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze card combinations: {str(e)}")

    async def _base_enrichment(self, card: CardMeaning) -> CardMeaning:
        """Initial AI-based enrichment of card."""
        try:
            prompt = f"""
            Enrich this tarot card with detailed meanings and correspondences:
            {json.dumps(card.dict(), indent=2)}
            
            Provide:
            1. Keywords (max 7)
            2. Upright meaning (concise)
            3. Reversed meaning (concise)
            4. Astrological correspondence
            5. Kabbalistic attribution
            6. Elemental association
            7. Decan (if applicable)
            
            Format as JSON matching the input structure.
            """
            
            response = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            enriched_data = json.loads(response.content)
            return CardMeaning(**enriched_data)
        except Exception as e:
            raise EnrichmentError(f"Failed base enrichment: {str(e)}")

    async def generate_embeddings(self, card: CardMeaning) -> List[float]:
        """Generate embeddings for a card using VoyageAI."""
        try:
            # Combine relevant card attributes for embedding
            text_to_embed = f"{card.name} {' '.join(card.keywords)} {card.upright_meaning} {card.reversed_meaning}"
            embedding = await get_embedding(
                text_to_embed,
                model="voyage-2",
                api_key=self.voyage_key
            )
            return embedding
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")

    async def enrich_card(self, card: CardMeaning) -> CardMeaning:
        """Enrich a single card with AI-generated content and reading history."""
        try:
            # Base enrichment
            enriched = await self._base_enrichment(card)
            
            # Additional enrichment from reading history
            reading_insights = await self.learn_from_readings(card.name)
            
            # Merge insights if available
            if reading_insights:
                enriched.keywords.extend(reading_insights.get('additional_keywords', []))
                # Add other insight merging logic as needed
            
            return enriched
        except Exception as e:
            raise EnrichmentError(f"Failed to enrich card {card.name}: {str(e)}")

    async def process_all_cards(self) -> None:
        """Process all cards with both enrichment and embeddings."""
        embeddings = {}
        
        for card in self.cards:
            try:
                print(f"Processing {card.name}...")
                enriched_card = await self.enrich_card(card)
                embedding = await self.generate_embeddings(enriched_card)
                embeddings[card.name] = embedding
                
                # Update card in list
                idx = next(i for i, c in enumerate(self.cards) if c.name == card.name)
                self.cards[idx] = enriched_card
                
            except Exception as e:
                print(f"Error processing {card.name}: {str(e)}")
                continue
            
        self._save_cards()
        self._save_embeddings(embeddings)

async def main():
    enricher = TarotEnricher()
    await enricher.process_all_cards()

if __name__ == "__main__":
    asyncio.run(main())