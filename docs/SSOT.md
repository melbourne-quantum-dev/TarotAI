# TarotAI System Documentation (Single Source of Truth)

Version 2.1.0

## Documentation Standards

### File Structure
- SSOT.md: Canonical technical documentation
- README.md: Project overview and quickstart  
- CONTRIBUTING.md: Development contribution guide
- CODE_OF_CONDUCT.md: Community standards

### Versioning
- Documentation version must match package version
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in both SSOT.md and README.md

### Style Guide
- Use consistent terminology
- Follow Markdown best practices
- Include code samples where applicable
- Use tables for complex information

## Book T Sequence
// 
// 1. Aces: Wands, Cups, Swords, Pentacles
// 2. Pips:
//    5-7 of Wands
//    8-10 of Pentacles
//    2-4 of Swords
//    5-7 of Cups
//    8-10 of Wands
//    2-4 of Pentacles
//    5-7 of Swords
//    8-10 of Cups
//    2-4 of Wands
//    5-7 of Pentacles
//    8-10 of Swords
//    2-4 of Cups
// 3. Court Cards:
//    Wands (Knight, Queen, King, Princess)
//    Cups (Knight, Queen, King, Princess)
//    Swords (Knight, Queen, King, Princess)
//    Pentacles (Knight, Queen, King, Princess)
// 4. Major Arcana: 0 (Fool), I-XXI

Version 2.0.0

## Table of Contents
1. System Overview
2. Architecture
3. Implementation Guidelines
4. Testing & Quality Assurance
5. Deployment & Operations
6. API Reference
7. Developer Guide

## 1. System Overview

### 1.1 Purpose
TarotAI is a neural-enhanced divination interface providing programmatic access to tarot readings through a CLI interface. It combines traditional tarot interpretation with modern software engineering practices.

### 1.2 Key Features
- Interactive CLI interface with rich visual feedback
- Multiple spread types support
- Context-aware interpretation engine
- Error handling and recovery
- Extensible architecture

## 2. Architecture

### 2.1 Component Structure
```
tarotai/
├── src/
│   ├── tarotai/
│   │   ├── __init__.py
│   │   ├── cli.py           # CLI interface
│   │   ├── core/            # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── types.py     # Type definitions
│   │   │   ├── card.py      # Card implementation
│   │   │   ├── deck.py      # Deck management
│   │   │   └── interpreter.py # Reading interpretation
│   │   └── data/            # Static resources
├── tests/
│   ├── __init__.py
│   └── test_tarotai.py
├── setup.py
├── requirements.txt
└── README.md
```

### 2.2 Key Components

#### TarotDisplay
Manages visual presentation and user feedback:
```python
class TarotDisplay:
    def welcome_banner(self) -> str
    def system_status(self) -> Panel
    def loading_sequence(self, message: str, delay: float = 0.4)
```

#### TarotInterface
Handles user interaction:
```python
class TarotInterface:
    SPREADS: Dict[str, Tuple[str, int]]
    def gather_context(self) -> Tuple[str, str, str]
```

#### TarotReader
Coordinates reading execution:
```python
class TarotReader:
    def execute_reading(self, reading_type: str, focus: str, question: str) -> Reading
```

## 3. Implementation Guidelines

### 3.1 Code Standards
- Use type hints consistently
- Follow PEP 8 style guide
- Document all public interfaces
- Implement proper error handling
- Use context managers for resource management
- Use Pydantic for data validation and serialization
- Follow src-layout project structure

### 3.2 Error Handling
```python
@contextmanager
def loading_sequence(self, message: str):
    try:
        with self.console.status(message) as status:
            yield status
    except KeyboardInterrupt:
        self.console.print("[bold red]✘ Operation interrupted[/]")
        raise
```

### 3.3 Type System
```python
@dataclass
class Reading:
    spread: str
    cards: List[Tuple[str, str]]
    interpretation: str

@dataclass
class QuestionContext:
    focus: str
    raw_question: str
    additional_context: Optional[Dict[str, str]] = None
```

## 4. Testing & Quality Assurance

### 4.1 Test Structure
- Unit tests for core components
- Integration tests for CLI interface
- End-to-end tests for complete readings

### 4.2 Test Guidelines
```python
def test_reading_execution():
    reader = TarotReader(display=MockDisplay())
    reading = reader.execute_reading(
        reading_type="single",
        focus="Present",
        question="Test question"
    )
    assert reading.spread == "single"
    assert len(reading.cards) == 1
```

## 5. Deployment & Operations

### 5.1 Environment Setup
```bash
# Required environment variables
DATA_DIR=/path/to/data
CARD_MEANINGS_PATH=${DATA_DIR}/card_meanings.json
ANTHROPIC_API_KEY=your_anthropic_api_key
VOYAGEAI_API_KEY=your_voyageai_api_key

# Install uv (if not already installed)
pip install uv

# Create virtual environment
uv venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Install tarotai in development mode
uv pip install -e .
```

### 5.2 Deployment Process
1. Update version in `__init__.py`
2. Run test suite
3. Build distribution package
4. Deploy to target environment

## 6. API Reference

### 6.1 Core Types
```python
class Reading(BaseModel):
    context: QuestionContext
    reading_type: ReadingType  # single, three_card, celtic_cross, custom
    positions: List[SpreadPosition]
    cards: List[CardMeaning]
    is_reversed: List[bool]
    timestamp: str
    interpretation: Optional[str]

class CardMeaning(BaseModel):
    name: str
    number: int  # 0-21 for Major, 1-14 for Minor
    suit: Optional[CardSuit]  # major, wands, cups, swords, pentacles
    keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
```

#### TarotDeck
```python
class TarotDeck:
    def draw_spread(self, reading_type: str) -> List[Tuple[str, str]]
```

### 6.2 Constants
```python
SPREADS = {
    "◈ Single Card": ("single", 1),
    "◈ Three Card": ("three", 3),
    "◈ Celtic Cross": ("celtic_cross", 10),
    "◈ Horseshoe": ("horseshoe", 7)
}
```

## 7. Developer Guide

### 7.1 Getting Started
1. Clone repository
2. Install dependencies
3. Set up environment variables
4. Run test suite

#### Example Usage
```python
reading = reader.execute_reading(
    reading_type=ReadingType.SINGLE,
    focus="Present",
    question="What energies are present?"
)
```

### 7.2 Common Tasks
```python
# Creating a new reading
reader = TarotReader(display=TarotDisplay())
reading = reader.execute_reading(
    reading_type="single",
    focus="Present",
    question="What energies are present?"
)
```

### 7.3 Troubleshooting
- Check environment variables
- Verify data file permissions
- Review error logs
- Test network connectivity

## 8. System Implementation Details

## 9. AI and Embedding Architecture

### 9.1 Overview
The system integrates multiple AI providers for meaning generation and embedding services:
- **DeepSeek V3**: Primary model for card meaning generation
- **VoyageAI**: Primary embedding service for semantic analysis
- **Anthropic Claude**: Secondary model for meaning generation and structured responses

### 9.2 AI Client Implementations

#### DeepSeekClient
- Supports Multi-Token Prediction (MTP)
- FP8 and BF16 precision modes
- Advanced load balancing strategies
- Key features:
  ```python
  async def generate_with_mtp(self, prompt: str) -> Dict[str, Any]
  async def generate_fp8_embedding(self, text: str) -> List[float]
  ```

#### VoyageClient
- Multimodal embeddings (text + image)
- Reranking capabilities
- Quantized embeddings (int8)
- Usage tracking and cost estimation
- Key features:
  ```python
  async def generate_multimodal_embedding(content: List[Dict[str, Any]]) -> List[float]
  async def rerank_documents(query: str, documents: List[str]) -> List[Dict[str, Any]]
  ```

#### ClaudeClient
- Tool use (function calling)
- Batch message processing
- Streaming responses
- Structured JSON responses
- Key features:
  ```python
  async def generate_batch_responses(prompts: List[str]) -> List[Dict[str, Any]]
  async def generate_structured_response(prompt: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]
  ```

### 9.3 Embedding Management

#### CardEmbeddings Class
```python
class CardEmbeddings:
    text_embedding: List[float]
    image_embedding: Optional[List[float]]
    multimodal_embedding: Optional[List[float]]
    quantized_embedding: Optional[List[int]]
    reduced_dimension_embedding: Optional[List[float]]
```

#### ReadingEmbeddings Class
```python
class ReadingEmbeddings:
    card_embeddings: List[CardEmbeddings]
    position_embeddings: List[List[float]]
    context_embedding: List[float]
```

### 9.4 Integration Points

#### Reading Input
```python
async def generate_embeddings(self, voyage_client) -> Optional[ReadingEmbeddings]:
    # Generate hierarchical embeddings for the reading
    cards = self.get_cards()
    
    # Generate text embeddings
    text_embeddings = await voyage_client.generate_batch_embeddings(
        [card[0].upright_meaning for card in cards]
    )
    
    # Generate multimodal embeddings if images available
    card_embeddings = []
    for card, text_embedding in zip(cards, text_embeddings):
        embeddings = CardEmbeddings(text_embedding=text_embedding)
        
        if card[0].image_url:
            content = [
                {"type": "text", "text": card[0].upright_meaning},
                {"type": "image_url", "image_url": card[0].image_url}
            ]
            embeddings.multimodal_embedding = await voyage_client.generate_multimodal_embedding(content)
```

## 10. Meaning Generation Workflow (Updated)

### 10.1 Enhanced Workflow Steps
1. **Initialization**:
   - Load existing card data
   - Initialize AI clients (DeepSeek, VoyageAI, Claude)
   
2. **Meaning Generation**:
   - Use DeepSeek for primary meaning generation
   - Use Claude for structured responses and tool use
   - Apply validation rules

3. **Embedding Generation**:
   - Generate text embeddings using VoyageAI
   - Generate multimodal embeddings for cards with images
   - Store embeddings in hierarchical structure

4. **Validation**:
   - Semantic consistency checks
   - Embedding dimensionality validation
   - Cross-provider consistency verification

5. **Refinement**:
   - AI-assisted refinement using multiple providers
   - Semantic similarity analysis
   - Pattern recognition across readings

6. **Persistence**:
   - Save updated card data
   - Store embeddings separately
   - Update usage statistics

### 10.2 Example Workflow
```python
async def main():
    # Initialize clients
    deepseek = DeepSeekClient()
    voyage = VoyageClient()
    claude = ClaudeClient()
    
    # Load cards
    cards = load_cards("data/cards_ordered.json")
    
    # Generate meanings
    meanings = await deepseek.generate_batch_responses(
        [card.upright_meaning for card in cards]
    )
    
    # Generate embeddings
    embeddings = await voyage.generate_batch_embeddings(
        [meaning["text"] for meaning in meanings]
    )
    
    # Store results
    save_cards(cards, "data/cards_enhanced.json")
    save_embeddings(embeddings, "data/embeddings.json")
```

## 11. Performance Considerations

### 11.1 Batch Processing
- Use batch APIs for meaning generation and embeddings
- Implement efficient batching strategies
- Monitor API rate limits

### 11.2 Caching
- Cache embeddings and meanings
- Implement LRU cache for frequent queries
- Use versioning for cache invalidation

### 11.3 Cost Optimization
- Track API usage
- Implement cost estimation
- Use quantized embeddings where possible

The system uses an iterative, AI-assisted process to generate and refine card meanings. This workflow ensures consistency and quality while maintaining alignment with traditional tarot interpretations.

### 9.1 Workflow Steps
1. **Initialization**:
   - Load existing card data from `data/cards_ordered.json`.
   - Identify incomplete cards (missing meanings or embeddings).

2. **Meaning Generation**:
   - Use AI models (DeepSeek, VoyageAI) to generate upright and reversed meanings.
   - Apply validation rules to ensure consistency.

3. **Embedding Generation**:
   - Generate semantic embeddings for each card's meanings using VoyageAI.
   - Store embeddings for use in semantic search and pattern analysis.

4. **Validation**:
   - Check for consistency in generated meanings.
   - Verify embeddings are valid and complete.

5. **Refinement**:
   - Manually review and refine generated meanings.
   - Use semantic similarity to resolve inconsistencies.

6. **Persistence**:
   - Save updated card data to `data/cards_ordered.json`.

### 9.2 Extension Configuration

Extensions can be configured via environment variables:

```bash
# Enrichment settings
export ENRICHMENT_MODEL="deepseek"
export VOYAGEAI_API_KEY="your_key"

# Voice settings
export VOICE_MODEL="elevenlabs"
export VOICE_SPEED=1.0
```

### 9.3 Key Components

#### Prompt Templates
```python
UPRIGHT_PROMPT = """
Generate an upright meaning for the {card_name} tarot card. 
The card is associated with {element} and represents {keywords}.
The astrological correspondence is {astrological}, and the Kabbalistic path is {kabbalistic}.
Provide a concise, modern interpretation.
"""

REVERSED_PROMPT = """
Generate a reversed meaning for the {card_name} tarot card.
The upright meaning is: {upright_meaning}.
Provide a concise, modern interpretation of the reversed energy.
```
```

#### Validation Rules
- Meanings must be non-empty and contextually relevant.
- Embeddings must match the expected dimensionality (e.g., 1024 for VoyageAI).
- Keywords must align with the card's traditional symbolism.

#### Error Handling
- Retry failed API requests with exponential backoff.
- Log errors for manual review.
- Skip invalid cards to prevent data corruption.

### 9.3 Example Workflow
```python
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
```

### 8.1 Core Components

#### TarotDeck
```python
class TarotDeck:
    def __init__(self, cards_data: Path):
        self.cards: List[CardMeaning] = self._load_cards(cards_data)
    
    def shuffle(self) -> None: ...
    def draw(self, count: int = 1) -> List[Tuple[CardMeaning, bool]]: ...
    def reset(self) -> None: ...
```

### TarotReader
```python
class TarotReader:
    def __init__(self, deck: TarotDeck, interpreter: Interpreter):
        self.deck = deck
        self.interpreter = interpreter

    async def execute_reading(
        self, 
        reading_type: ReadingType,
        focus: str,
        question: str,
        context: Optional[Dict[str, str]] = None
    ) -> Reading: ...

    def _prepare_spread(self, reading_type: ReadingType) -> List[SpreadPosition]: ...
```

#### Interpreter
```python
class Interpreter:
    def __init__(self, model_config: Dict[str, Any]):
        self.model = self._initialize_model(model_config)

    async def interpret_reading(
        self,
        reading: Reading,
        depth: Optional[str] = "detailed"
    ) -> str: ...

    def _generate_prompt(self, reading: Reading) -> str: ...
```

#### CLI Interface
```python
@click.group()
def cli():
    """TarotAI - Neural-Enhanced Tarot Reading Interface"""

@cli.command()
@click.option("--reading-type", type=click.Choice([t.value for t in ReadingType]))
@click.option("--focus", prompt=True)
@click.option("--question", prompt=True)
def read(reading_type: str, focus: str, question: str): ...

@cli.command()
def interactive(): ...
```

### 8.2 Data Flow
1. User initiates reading through CLI
2. TarotReader creates QuestionContext
3. TarotDeck shuffles and draws cards
4. SpreadPositions are created based on reading type
5. Reading object is constructed
6. Interpreter processes reading
7. Results displayed via Rich console

### 8.3 Error Handling Strategy
```python
class TarotError(Exception): pass
class DeckError(TarotError): pass
class ReadingError(TarotError): pass
class InterpretationError(TarotError): pass

def handle_reading_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TarotError as e:
            logger.error(f"Reading error: {e}")
            raise
        except Exception as e:
            logger.exception("Unexpected error during reading")
            raise TarotError(f"Reading failed: {e}")
    return wrapper
```

### 8.4 Testing Strategy
- Unit tests for each core component
- Integration tests for full reading flow
- Mock API calls for interpretation
- Property-based testing for deck operations
- Snapshot testing for CLI output

## Appendix A: Security Considerations

### A.1 Data Protection
- Secure storage of card meanings
- Input validation
- Error message sanitization
- API key management for multiple AI providers (Anthropic, DeepSeek, Voyage)

### A.2 Error Handling
- Graceful degradation
- User feedback
- Logging standards

## Appendix B: Change Management

### B.1 Version Control
- Feature branches
- Pull request process
- Code review requirements

### B.2 Release Process
- Version numbering
- Changelog maintenance
- Deployment verification

## 9. Extensions

### 9.1 Enrichment Extension

The enrichment extension enhances the core tarot system with AI-powered features and historical analysis.

#### 9.1.1 Key Capabilities
- AI-enhanced card meanings beyond static definitions (via Anthropic or DeepSeek)
- Reading pattern analysis and insights
- Historical reading tracking and analysis
- Semantic search via embeddings (VoyageAI)
- Flexible AI provider selection

#### 9.1.2 Component Structure
```python
extensions/
└── enrichment/
    ├── __init__.py
    ├── enricher.py          # Main enrichment coordinator
    ├── reading_history.py   # Reading history management
    ├── analyzers/
    │   ├── __init__.py
    │   ├── base.py         # Base analyzer interface
    │   ├── temporal.py     # Time-based pattern analysis
    │   ├── combinations.py # Card combination analysis
    │   └── insights.py     # Reading insight generation
    └── clients/
        ├── __init__.py
        ├── base.py         # Base AI client interface
        ├── claude.py       # Claude integration
        └── voyage.py       # VoyageAI integration
```

#### 9.1.3 Core vs Extension
The core system provides:
- Basic card meanings and attributes
- Spread mechanics and position meanings
- Basic interpretation logic
- Reading execution flow

The enrichment extension adds:
- Dynamic meaning enhancement via AI
- Pattern recognition across readings
- Historical context and learning
- Semantic similarity search
- Advanced interpretation insights

#### 9.1.4 Integration Points
```python
# Core reading enhanced with enrichment
class Reading(BaseModel):
    # Core attributes
    context: QuestionContext
    cards: List[CardMeaning]
    positions: List[SpreadPosition]
    
    # Enrichment attributes
    enriched_meanings: Optional[Dict[str, Any]]
    pattern_insights: Optional[Dict[str, Any]]
    similar_readings: Optional[List[Reading]]
    resonance_score: Optional[float]

# Core card meaning enhanced with enrichment
class CardMeaning(BaseModel):
    # Core attributes
    name: str
    number: int
    suit: Optional[CardSuit]
    
    # Enrichment attributes
    ai_enhanced_meaning: Optional[Dict[str, Any]]
    historical_patterns: Optional[Dict[str, Any]]
    embedding: Optional[List[float]]
    combination_affinities: Optional[Dict[str, float]]
```

#### 9.1.5 Usage Example
```python
# Core reading with enrichment
async def execute_enriched_reading(
    reader: TarotReader,
    enricher: TarotEnricher,
    context: QuestionContext
) -> Reading:
    # Core reading
    reading = await reader.execute_reading(context)
    
    # Enrichment layer
    enriched = await enricher.enrich_reading(reading)
    patterns = await enricher.analyze_patterns(reading)
    similar = await enricher.find_similar_readings(reading)
    
    return Reading(
        **reading.dict(),
        enriched_meanings=enriched,
        pattern_insights=patterns,
        similar_readings=similar
    )
```

## 10. Development Workflow

### 10.1 Setup Environment
```bash
# Create virtual environment
uv venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Install tarotai in development mode
uv pip install -e .
```

### 10.2 Common Development Commands

#### Run Tests
```bash
uv run pytest tests/
```

#### Generate Card Meanings
```bash
uv run python scripts/generate_meanings.py
```

#### Process Golden Dawn PDF
```bash
uv run python src/tarotai/extensions/enrichment/enricher.py
```

#### Run CLI Interface
```bash
uv run python src/tarotai/cli.py
```

### 10.3 Git Workflow

#### Standard Commit Process
```bash
# Stage changes
git add .

# Check status
git status

# Commit with message
git commit -m "Your commit message"

# Push changes
git push
```

#### Recommended Commit Message Format
```
type(scope): short description

[optional body]

[optional footer]
```

Where type is one of:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style/formatting
- refactor: Code refactoring
- test: Test additions/modifications
- chore: Maintenance tasks

Example:
```
feat(enrichment): add Golden Dawn PDF processing
```

### 10.4 Code Quality Checks

#### Run Linting
```bash
uv run flake8 src/ tests/
```

#### Run Type Checking
```bash
uv run mypy src/ tests/
```

#### Format Code
```bash
uv run black src/ tests/
```

### 10.5 Release Process

1. Update version in `src/tarotai/__init__.py`
2. Run full test suite
3. Build distribution package
4. Deploy to target environment

## 11. Data Structures

### 10.1 Card Definitions

The `cards_ordered.json` file contains the canonical card definitions following the Book T sequence. This file serves as the single source of truth for card meanings and attributes.

#### 10.1.1 Schema

```json
{
  "version": "2.0.0",
  "last_updated": "2025-01-14",
  "cards": [
    {
      "name": "Ace of Wands",
      "number": 1,
      "suit": "WANDS",
      "element": "FIRE",
      "astrological": "Root of the Powers of Fire",
      "kabbalistic": "Kether in Atziluth",
      "decan": null,
      "keywords": [
        "creation",
        "inspiration",
        "power",
        "potential"
      ],
      "upright_meaning": "Raw power and potential. The initial spark of inspiration...",
      "reversed_meaning": "Blocked creativity. Delays in projects...",
      "book_t_description": "Root of the Powers of Fire",
      "golden_dawn_title": "The Root of the Powers of Fire"
    }
  ]
}
```

#### 10.1.2 Card Ordering

The cards follow the Book T sequence:

1. Aces (Wands → Cups → Swords → Pentacles)
2. Pips in groups:
   - 2-10 of Wands
   - 2-10 of Cups
   - 2-10 of Swords
   - 2-10 of Pentacles
3. Court Cards by suit (Page → Knight → Queen → King)
4. Major Arcana (0-XXI)

#### 10.1.3 Usage in Core System

```python
def _load_cards(self, cards_file: Path) -> List[CardMeaning]:
    """Load and validate card definitions."""
    data = json.loads(cards_file.read_text())
    cards = [CardMeaning(**card) for card in data["cards"]]
    # Verify card count and sequence
    assert len(cards) == 78, "Invalid number of cards"
    assert all(i+1 == c.number for i, c in enumerate(cards[:40])), "Invalid minor arcana order"
    assert all(c.number == i-21 for i, c in enumerate(cards[40:], start=62)), "Invalid major arcana order"
    return cards
```

#### 10.1.4 Enrichment Extensions

The enrichment system can add to card meanings without modifying the base file:

```python
class EnrichedCardMeaning(CardMeaning):
    ai_enhanced_meaning: Optional[Dict[str, Any]]
    historical_patterns: Optional[Dict[str, Any]]
    embedding: Optional[List[float]]
    combination_affinities: Optional[Dict[str, float]]
    
    class Config:
        extra = "allow"  # Allows additional fields for future extensions
```

#### 10.1.5 Validation Rules

- All 78 cards must be present
- Book T sequence must be maintained
- Required fields: name, number, suit, element, keywords, upright_meaning, reversed_meaning
- Suit required for minor arcana, null for major arcana
- Version must match current system version
- Last updated date must be in ISO 8601 format
