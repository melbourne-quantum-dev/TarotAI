import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from .clients.base import BaseAIClient

from tarotai.core.types import CardMeaning, Reading, CardSuit, SpreadPosition, QuestionContext
from tarotai.core.exceptions import EnrichmentError, EmbeddingError
from tarotai.extensions.enrichment.reading_history import ReadingHistoryManager
from tarotai.extensions.enrichment.clients.claude import ClaudeClient
from tarotai.extensions.enrichment.clients.voyage import VoyageClient
from tarotai.extensions.enrichment.clients.deepseek import DeepSeekClient
from tarotai.extensions.enrichment.analyzers.temporal import TemporalAnalyzer
from tarotai.extensions.enrichment.analyzers.combinations import CombinationAnalyzer
from tarotai.extensions.enrichment.analyzers.insights import InsightGenerator

load_dotenv()

class TarotEnricher:
    def __init__(
        self,
        cards_file: Path = Path("data/cards_ordered.json"),
        ai_client: BaseAIClient = None,
        golden_dawn_path: Path = Path("data/golden_dawn.pdf")
    ):
        self.cards_file = cards_file
        self.cards: List[CardMeaning] = self._load_cards()
        self.reading_manager = ReadingHistoryManager()
        self.embeddings_file = Path("data/embeddings.json")
        
        # Initialize AI client
        if ai_client is None:
            self.ai_client = DeepSeekClient(api_key=os.getenv("DEEPSEEK_API_KEY"))
        else:
            self.ai_client = ai_client
        
        # Voyage is still used for embeddings
        self.voyage = VoyageClient(api_key=os.getenv("VOYAGE_API_KEY"))
        
        # Initialize analyzers
        self.temporal_analyzer = TemporalAnalyzer()
        self.combination_analyzer = CombinationAnalyzer()
        self.insight_generator = InsightGenerator()
        
        # Initialize Golden Dawn knowledge base
        self.golden_dawn = GoldenDawnKnowledgeBase(str(golden_dawn_path))

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

    async def _analyze_reading_patterns(self, readings: List[Reading], card_name: str) -> Dict[str, Any]:
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
            
            Provide a structured analysis with:
            1. Most common themes and contexts
            2. Position-specific meanings
            3. Successful interpretation patterns
            4. Suggested meaning refinements
            
            Readings data:
            {json.dumps([r.dict() for r in readings], indent=2)}
            """
            
            response = await self.claude.analyze(prompt)
            
            return json.loads(response)
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze readings: {str(e)}")

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
            
            response = await self.claude.analyze(prompt)
            
            enriched_data = json.loads(response)
            return CardMeaning(**enriched_data)
        except Exception as e:
            raise EnrichmentError(f"Failed base enrichment: {str(e)}")

    async def generate_embeddings(self, card: CardMeaning) -> List[float]:
        """Generate embeddings for a card using VoyageAI."""
        try:
            # Combine relevant card attributes for embedding
            text_to_embed = f"{card.name} {' '.join(card.keywords)} {card.upright_meaning} {card.reversed_meaning}"
            embedding = await self.voyage.get_embedding(text_to_embed)
            return embedding
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embeddings: {str(e)}")

    async def enrich_card(self, card: CardMeaning) -> CardMeaning:
        """Enrich card meanings using AI and Golden Dawn context"""
        try:
            # Get Golden Dawn context
            card_embedding = await self.voyage.generate_embedding(
                f"{card.name} {' '.join(card.keywords)}"
            )
            relevant_sections = self.golden_dawn.find_relevant_sections(card_embedding)
            context = "\n\n".join(
                f"Page {s['metadata']['page']}:\n{s['content']}" 
                for s in relevant_sections
            )
            
            # Build prompt with Golden Dawn context
            prompt = f"""
            You are an expert tarot interpreter with deep knowledge of:
            - Golden Dawn traditions
            - Astrological correspondences
            - Psychological archetypes
            - Modern applications

            Relevant Golden Dawn Context:
            {context}

            Card Details:
            - Name: {card.name}
            - Element: {card.element}
            - Keywords: {', '.join(card.keywords)}

            Provide interpretation considering:
            1. Traditional Golden Dawn meanings
            2. Modern psychological insights
            3. Practical applications

            Format your response as JSON with these fields:
            - expanded_keywords: List of 5-7 keywords
            - upright_meaning: 2-3 sentence interpretation
            - reversed_meaning: 2-3 sentence interpretation
            - astrological_correspondences: List of astrological associations
            - elemental_associations: List of elemental associations
            - golden_dawn_insights: Key insights from Golden Dawn context
            """
            
            # Get enhanced meaning
            enhanced_meaning = await self.ai_client.json_prompt(prompt)
            
            # Update card with enriched data
            card.ai_enhanced_meaning = enhanced_meaning
            card.golden_dawn_context = context
            
            return card
        except Exception as e:
            raise EnrichmentError(f"Failed to enrich card: {str(e)}")

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
