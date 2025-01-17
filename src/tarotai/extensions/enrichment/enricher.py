import json
import os
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from .clients.base import BaseAIClient
from .knowledge.golden_dawn import GoldenDawnKnowledgeBase
from tarotai.core.prompts import MultiStagePrompt, PromptStage

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
        
        # Initialize Golden Dawn knowledge base
        self.golden_dawn = GoldenDawnKnowledgeBase(golden_dawn_path)
        
        # Cache for processed cards
        self.processed_cards: Dict[str, Dict[str, Any]] = {}

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

    async def analyze_reading_patterns(self, card_name: str) -> Dict[str, Any]:
        """Analyze reading patterns using AI client directly"""
        try:
            readings = self.get_readings_for_card(card_name)
            stats = self.get_card_statistics(card_name)
            
            return await self.ai_client.analyze_reading_patterns(
                card_name=card_name,
                readings=readings,
                statistics=stats
            )
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze reading patterns: {str(e)}")

    async def _base_enrichment(self, card: CardMeaning, context: str = "") -> CardMeaning:
        try:
            prompt = MultiStagePrompt([
                PromptStage(
                    name="initial_analysis",
                    system_message="Analyze the core symbolism of this tarot card",
                    user_message=f"""
                    Card: {card.name}
                    Current Keywords: {card.keywords}
                    Provide:
                    1. 3-5 additional keywords
                    2. Core archetypal meaning
                    3. Psychological significance
                    """
                ),
                PromptStage(
                    name="correspondences",
                    system_message="Identify esoteric correspondences",
                    user_message="""
                    For this card, provide:
                    1. Astrological correspondence
                    2. Elemental association
                    3. Kabbalistic path
                    4. Numerological significance
                    """
                ),
                PromptStage(
                    name="practical_application",
                    system_message="Provide practical interpretations",
                    user_message="""
                    For this card, provide:
                    1. Upright meaning (concise)
                    2. Reversed meaning (concise)
                    3. 3 practical applications
                    4. Common misinterpretations
                    """
                )
            ])
            
            results = await prompt.execute(self.ai_client)
            return CardMeaning(**{**card.dict(), **results})
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

    async def enrich_card(self, card: CardMeaning, use_rag: bool = True) -> CardMeaning:
        """Enrich a single card with AI-generated content and reading history."""
        try:
            # Retrieve relevant context if RAG is enabled
            context = ""
            if use_rag:
                card_embedding = await self.voyage.generate_embedding(
                    f"{card.name} {' '.join(card.keywords)}"
                )
                relevant_sections = self.golden_dawn.find_relevant_sections(card_embedding)
                context = "\n\n".join(
                    f"Page {s['metadata']['page']}:\n{s['content']}" 
                    for s in relevant_sections
                )
            
            # Base enrichment with context
            enriched = await self._base_enrichment(card, context)
            
            # Additional enrichment from reading history
            reading_insights = await self.learn_from_readings(card.name)
            
            # Get Golden Dawn context
            card_embedding = await self.voyage.generate_embedding(
                f"{card.name} {' '.join(card.keywords)}"
            )
            relevant_sections = self.golden_dawn.find_relevant_sections(card_embedding)
            context = "\n\n".join(
                f"Page {s['metadata']['page']}:\n{s['content']}" 
                for s in relevant_sections
            )
            
            # Merge insights if available
            if reading_insights:
                enriched.keywords.extend(reading_insights.get('additional_keywords', []))
                # Add other insight merging logic as needed
            
            # Update Golden Dawn context
            enriched.golden_dawn_context = context
            
            return enriched
        except Exception as e:
            raise EnrichmentError(f"Failed to enrich card: {str(e)}")

    async def process_all_cards(self, batch_size: int = 5) -> None:
        """Process all cards with both enrichment and embeddings in batches."""
        embeddings = {}
        total_cards = len(self.cards)
        
        for i in range(0, total_cards, batch_size):
            batch = self.cards[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1} of {total_cards//batch_size + 1}")
            
            # Process cards in parallel
            tasks = []
            for card in batch:
                tasks.append(self._process_card(card))
            
            # Wait for all tasks in batch to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Update cards and embeddings
            for result in results:
                if isinstance(result, Exception):
                    print(f"Error processing card: {str(result)}")
                    continue
                
                card_name, enriched_card, embedding = result
                embeddings[card_name] = embedding
                
                # Update card in list
                idx = next(i for i, c in enumerate(self.cards) if c.name == card_name)
                self.cards[idx] = enriched_card
                
            # Save progress after each batch
            self._save_cards()
            self._save_embeddings(embeddings)
            
        print("All cards processed successfully!")

    async def _process_card(self, card: CardMeaning) -> Tuple[str, CardMeaning, List[float]]:
        """Process a single card and return enriched data."""
        try:
            print(f"Processing {card.name}...")
            
            # Get Golden Dawn context
            card_embedding = await self.voyage.generate_embedding(card.name)
            relevant_sections = self.golden_dawn.find_relevant_sections(card_embedding)
            context = "\n\n".join(
                f"Page {s['metadata']['page']}:\n{s['content']}" 
                for s in relevant_sections
            )
            
            # Enrich card with AI
            enriched = await self._base_enrichment(card, context)
            
            # Generate embeddings
            embedding = await self.generate_embeddings(enriched)
            
            return card.name, enriched, embedding
            
        except Exception as e:
            raise EnrichmentError(f"Failed to process card {card.name}: {str(e)}")

async def main():
    enricher = TarotEnricher()
    await enricher.process_all_cards()

if __name__ == "__main__":
    asyncio.run(main())
