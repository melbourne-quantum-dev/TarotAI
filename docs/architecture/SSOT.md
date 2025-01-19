# TarotAI System Documentation
Version 2.2.0 (2025-01-19)

## Technical Requirements

The system is implemented using:
- Python 3.12 or higher
- Type hints with PEP 484 and PEP 593
- Asynchronous operations following PEP 492
- Pydantic v2.5+ for data validation
- pytest 8.0+ for testing framework

## Core Type System

The type system provides the foundation for all tarot operations:

```python
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class CardSuit(Enum):
    """Fundamental categorization of tarot cards."""
    MAJOR = "major"
    WANDS = "wands"
    CUPS = "cups"
    SWORDS = "swords"
    PENTACLES = "pentacles"

class CardMeaning(BaseModel):
    """Structured representation of a card's meanings."""
    upright: List[str]
    reversed: List[str]
    keywords: List[str]
    element: Optional[str]
    numerology: Optional[int]

class TarotCard(BaseModel):
    """Core representation of a tarot card."""
    name: str
    suit: CardSuit
    number: int
    meanings: CardMeaning

    def get_meaning(self, is_reversed: bool = False) -> str:
        """Returns appropriate meaning based on card orientation."""
        return self.meanings.reversed if is_reversed else self.meanings.upright

class TarotDeck:
    """Implements the Golden Dawn card sequence."""
    def __init__(self, cards_data: Path):
        self.cards: List[TarotCard] = self._load_cards(cards_data)
        self.reset()
    
    def draw(self, count: int = 1) -> List[Tuple[TarotCard, bool]]:
        """Draws specified number of cards with randomized orientations."""
        if count > len(self.cards):
            raise DeckError("Not enough cards remaining")
        cards = self.cards[:count]
        self.cards = self.cards[count:]
        return [(card, random.choice([True, False])) for card in cards]
```

## AI Integration Layer

The AI system uses multiple specialized agents and clients:

```python
class BaseAgent(ABC):
    """Base for all AI agents in the system."""
    def __init__(self, ai_client: Optional[UnifiedAIClient] = None):
        self.ai_client = ai_client
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> AgentResult:
        """Process the input and return results."""
        pass

class InterpretationAgent(BaseAgent):
    """Handles tarot interpretation tasks."""
    async def process(self, cards: List[Dict], context: Optional[str] = None) -> Dict:
        enriched_context = await self._enrich_context(cards, context)
        return await self._generate_interpretation(cards, enriched_context)

class KnowledgeAgent(BaseAgent):
    """Manages knowledge retrieval and enrichment."""
    async def process(self, query: str) -> Dict:
        context = await self._get_rag_context(query)
        return await self._generate_response(query, context)

class UnifiedAIClient:
    """Unified interface for multiple AI providers."""
    def __init__(self, config: AISettings):
        self.config = config
        self.providers = {
            "claude": ClaudeClient(),
            "deepseek": DeepSeekClient(),
            "voyage": VoyageClient()
        }
```

## RAG System Implementation

The Retrieval Augmented Generation system provides knowledge context:

```python
class RAGSystem:
    """Manages retrieval augmented generation."""
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.chunk_size = 512
        self.context_window = 4096
    
    async def retrieve(self, query: str) -> RAGResult:
        embeddings = await self.generate_embeddings(query)
        contexts = await self.vector_store.similarity_search(
            embeddings,
            k=3,
            threshold=0.85
        )
        return self._build_rag_result(contexts)

@dataclass
class RAGResult:
    """Container for RAG operation results."""
    contexts: List[str]
    metadata: Dict[str, Any]
    confidence: float

    def validate(self) -> bool:
        """Validates the retrieval results."""
        return (
            len(self.contexts) > 0 and
            self.confidence >= 0.8
        )
```

## Testing Framework

The project uses pytest with a comprehensive testing structure:

```python
# tests/core/models/test_card.py
def test_card_validation():
    """Test card validation logic."""
    card = TarotCard(
        name="The Fool",
        number=0,
        suit=CardSuit.MAJOR,
        meanings=CardMeaning(
            upright=["beginnings", "innocence"],
            reversed=["recklessness", "risk-taking"],
            keywords=["potential", "new starts"],
            numerology=0
        )
    )
    assert card.validate() is True

# tests/ai/agents/test_interpretation.py
@pytest.mark.asyncio
async def test_interpretation_generation():
    """Test the interpretation generation pipeline."""
    agent = InterpretationAgent()
    cards = [sample_card_fixture()]
    result = await agent.process(cards)
    assert "interpretation" in result
    assert result["confidence"] > 0.8

# tests/ai/rag/test_generator.py
@pytest.mark.asyncio
async def test_rag_retrieval():
    """Test RAG context retrieval."""
    rag = RAGSystem(mock_vector_store())
    result = await rag.retrieve("Tell me about The Fool")
    assert result.validate()
```

## Project Structure

The project follows a carefully organized structure that reflects its layered architecture. Each directory serves a specific purpose in the system:

```
tarotai/
├── src/
│   └── tarotai/
│       ├── ai/
│       │   ├── agents/
│       │   │   ├── orchestration/  # Reading flow control
│       │   │   │   ├── interpreter.py  # Main interpretation logic
│       │   │   │   └── reading.py  # Reading session management
│       │   │   └── validation/  # Input/output validation
│       │   ├── clients/
│       │   │   ├── providers/  # AI provider implementations
│       │   │   │   ├── claude.py  # Anthropic Claude
│       │   │   │   ├── deepseek_v3.py  # DeepSeek Coder
│       │   │   │   └── voyage.py  # Voyage AI
│       │   │   ├── base.py  # Abstract client interface
│       │   │   └── registry.py  # Client management
│       │   ├── knowledge/  # Knowledge base management
│       │   │   └── golden_dawn.py  # Golden Dawn system
│       │   ├── prompts/  # Prompt engineering
│       │   │   └── templates/  # Jinja2 templates
│       │   └── rag/  # Retrieval system
│       │       ├── generator.py  # Embedding generation
│       │       ├── manager.py  # RAG orchestration
│       │       └── vector_store.py  # Vector operations
│       ├── core/
│       │   ├── models/  # Core data models
│       │   │   ├── card.py  # Card implementation
│       │   │   ├── deck.py  # Deck management
│       │   │   └── types.py  # Type definitions
│       │   ├── errors/  # Error system
│       │   │   └── base.py  # Base exceptions
│       │   └── validation/  # Core validation
│       └── config/
│           └── schemas/  # Configuration schemas
├── tests/  # Test suite (mirrors src)
│   ├── ai/
│   │   ├── agents/
│   │   ├── clients/
│   │   └── rag/
│   └── core/
│       ├── models/
│       └── validation/
├── data/  # Data storage
│   ├── cards_ordered.json  # Card definitions
│   ├── golden_dawn.json  # GD knowledge base
│   └── embeddings/  # Generated embeddings
└── docs/
    └── architecture/
        └── SSOT.md  # This document
```

The structure is organized around several key principles:

1. **Separation of Concerns**: The AI and core functionality are clearly separated, with AI components handling interpretation and knowledge management while core components manage fundamental tarot operations.

2. **Hierarchical Organization**: Components are organized in a logical hierarchy, with more complex features (like RAG and orchestration) building on simpler ones (like basic card models).

3. **Clear Dependencies**: Each component's dependencies are made explicit through the directory structure. For example, the AI agents depend on both the client implementations and the core models.

4. **Testability**: The test suite mirrors the source structure exactly, making it easy to locate and maintain tests for each component.

5. **Data Management**: All non-code artifacts (card definitions, knowledge base, embeddings) are centralized in the data directory for easy management and version control.

This structure supports the system's primary goals of providing accurate tarot interpretations while maintaining modularity and extensibility.
```

This documentation focuses on the core implementation components of TarotAI. For additional details about specific components, refer to the inline documentation in the respective source files.