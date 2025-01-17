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
        
        # Initialize analyzers
        self.temporal_analyzer = TemporalAnalyzer()
        self.combination_analyzer = CombinationAnalyzer()
        self.insight_generator = InsightGenerator()
        
        # Initialize Golden Dawn knowledge base with specific PDF path
        self.golden_dawn = GoldenDawnKnowledgeBase(
            "/home/fuar/projects/TarotAI/data/I.Regardie_Complete_Golden_Dawn_(II ed.deluxe).pdf"
        )

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

    async def analyze_reading_patterns(self, card_name: str):
        try:
            readings = self.get_readings_for_card(card_name)
            stats = self.get_card_statistics(card_name)
            
            prompt = MultiStagePrompt([
                PromptStage(
                    name="pattern_identification",
                    system_message="Identify patterns in tarot readings",
                    user_message=f"""
                    Analyze {len(readings)} readings for card {card_name}.
                    Identify:
                    1. Common themes
                    2. Position patterns
                    3. Interpretation effectiveness
                    4. Notable combinations
                    """
                ),
                PromptStage(
                    name="meaning_refinement",
                    system_message="Refine card meanings based on reading patterns",
                    user_message="""
                    Based on the identified patterns:
                    1. Suggest updated keywords
                    2. Refine upright meaning
                    3. Refine reversed meaning
                    4. Add contextual notes
                    """
                )
            ])
            
            return await prompt.execute(self.ai_client, {
                "readings": readings,
                "statistics": stats
            })
        except Exception as e:
            raise EnrichmentError(f"Failed to learn from readings: {str(e)}")

    async def _analyze_reading_patterns(self, readings: List[Reading], card_name: str, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze patterns in readings for a specific card."""
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
            
            response = await self.ai_client.json_prompt(prompt)
            return response
        except Exception as e:
            raise EnrichmentError(f"Failed to analyze readings: {str(e)}")

    async def _base_enrichment(self, card: CardMeaning) -> CardMeaning:
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
