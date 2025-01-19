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


─────────────────────────────────────────────────────────────────────────────────────
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃               TarotAI System Documentation (Single Source of Truth)               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Version 2.1.0                                                                        


                                   System Overview                                   

TarotAI is a neural-enhanced divination interface that combines traditional tarot    
interpretation with modern AI capabilities. The system provides programmatic access  
to tarot readings through a CLI interface, enriched with Golden Dawn knowledge,      
semantic embeddings, and advanced interpretation techniques.                         

                                    Key Features                                     

 • Interactive CLI interface with rich visual feedback                               
 • Multiple spread types (e.g., Celtic Cross, Three Card, Horseshoe)                 
 • Context-aware interpretation engine                                               
 • Retrieval Augmented Generation (RAG) for knowledge integration                    
 • Multimodal embeddings (text + image) for deeper understanding                     
 • Error handling and recovery                                                       
 • Extensible architecture for future enhancements                                   

─────────────────────────────────────────────────────────────────────────────────────

                             Current System Architecture                             

                                   Core Components                                   

 1 Card Management:                                                                  
    • TarotCard: Represents a tarot card with attributes like name, number, suit,    
      keywords, upright/reversed meanings, and embeddings.                           
    • CardManager: Manages loading, saving, and querying tarot cards.                
 2 Deck Management:                                                                  
    • TarotDeck: Handles card drawing, shuffling, and spread generation.             
    • Follows the Golden Dawn Book T sequence for card ordering.                     
 3 Interpretation Engine:                                                            
    • TarotInterpreter: Generates interpretations using AI models (DeepSeek, Claude, 
      VoyageAI).                                                                     
    • Supports structured responses, tool calling, and chain-of-thought reasoning.   
 4 Embedding System:                                                                 
    • EmbeddingManager: Manages text and multimodal embeddings for cards and         
      readings.                                                                      
    • Uses VoyageAI for embedding generation and semantic search.                    
 5 RAG System:                                                                       
    • RAGSystem: Retrieves relevant knowledge from the Golden Dawn corpus using      
      embeddings.                                                                    
    • Integrates with the interpretation engine for context-aware readings.          
 6 Error Handling:                                                                   
    • Hierarchical error system with specific error types (TarotError, DeckError,    
      ConfigError, etc.).                                                            
    • Structured error information including severity, timing, and contextual        
      details.                                                                       
 7 CLI Interface:                                                                    
    • Interactive command-line interface for performing readings.                    
    • Supports voice input/output for accessibility.                                 

─────────────────────────────────────────────────────────────────────────────────────

                           Current Golden Dawn Integration                           

                                 Existing Knowledge                                  

 • The system currently uses a processed version of the Golden Dawn PDF              
   (data/golden_dawn.json) for:                                                      
    • Card symbolism and correspondences                                             
    • Astrological and Kabbalistic associations                                      
    • Elemental attributions                                                         
    • Traditional reading methods                                                    

                                 Current Limitations                                 

 1 Knowledge Gaps:                                                                   
    • Some Golden Dawn concepts (e.g., advanced Kabbalistic paths, ritual practices) 
      are not fully integrated.                                                      
    • Historical context and esoteric practices are underrepresented.                
 2 RAG System:                                                                       
    • The RAG system currently uses basic embeddings and lacks advanced document     
      chunking or metadata handling.                                                 
    • Knowledge updates require manual processing.                                   
 3 Interpretation Depth:                                                             
    • Interpretations are primarily based on card meanings and lack deeper Golden    
      Dawn context (e.g., ritual significance, spiritual development).               

─────────────────────────────────────────────────────────────────────────────────────

                                Areas for Enhancement                                

                         1. Golden Dawn Knowledge Expansion                          

 • Unaddressed Insights:                                                             
    • Advanced Kabbalistic correspondences                                           
    • Ritual practices and their symbolic meanings                                   
    • Historical context and esoteric practices                                      
 • Integration Ideas:                                                                
    • Add new fields to TarotCard for ritual significance and spiritual development. 
    • Enhance the RAG system to handle advanced Golden Dawn concepts.                

                             2. RAG System Improvements                              

 • Current State:                                                                    
    • Basic embedding-based retrieval                                                
    • Limited metadata handling                                                      
 • Enhancements:                                                                     
    • Implement document chunking for better context retrieval.                      
    • Add metadata fields for version control and source tracking.                   
    • Integrate with the interpretation engine for dynamic context updates.          

                        3. Interpretation Engine Enhancements                        

 • Current State:                                                                    
    • Generates interpretations based on card meanings and basic Golden Dawn context.
 • Enhancements:                                                                     
    • Incorporate ritual significance and spiritual development into interpretations.
    • Add support for advanced reading methods (e.g., pathworking, meditation        
      guidance).                                                                     

                               4. Novel Opportunities                                

 • New Features:                                                                     
    • Guided meditations based on card symbolism                                     
    • Interactive learning modules for Golden Dawn concepts                          
    • Ritual guidance and spiritual development tools                                
 • Innovative Integrations:                                                          
    • Combine Golden Dawn rituals with AI-generated interpretations.                 
    • Use embeddings to create personalized spiritual development plans.             

─────────────────────────────────────────────────────────────────────────────────────

                                   Data Structures                                   

                                     Card Schema                                     

                                                                                     
 {                                                                                   
   "name": "string",                                                                 
   "number": "int|null",                                                             
   "suit": "string",                                                                 
   "element": "string",                                                              
   "astrological": "string",                                                         
   "kabbalistic": "string",                                                          
   "keywords": ["string"],                                                           
   "upright_meaning": "string",                                                      
   "reversed_meaning": "string",                                                     
   "golden_dawn": {                                                                  
     "title": "string",                                                              
     "symbolism": ["string"],                                                        
     "reading_methods": ["string"],                                                  
     "ritual_significance": "string",                                                
     "spiritual_development": "string"                                               
   },                                                                                
   "embeddings": {                                                                   
     "upright": ["float"],                                                           
     "reversed": ["float"],                                                          
     "multimodal": ["float"]                                                         
   }                                                                                 
 }                                                                                   
                                                                                     

                                   Reading Schema                                    

                                                                                     
 {                                                                                   
   "spread": "string",                                                               
   "cards": [                                                                        
     {                                                                               
       "name": "string",                                                             
       "position": "string",                                                         
       "is_reversed": "bool",                                                        
       "interpretation": "string"                                                    
     }                                                                               
   ],                                                                                
   "context": {                                                                      
     "question": "string",                                                           
     "focus": "string",                                                              
     "user_profile": {                                                               
       "name": "string",                                                             
       "reading_style": "string",                                                    
       "detail_level": "string"                                                      
     }                                                                               
   },                                                                                
   "metadata": {                                                                     
     "timestamp": "string",                                                          
     "version": "string"                                                             
   }                                                                                 
 }                                                                                   
                                                                                     

─────────────────────────────────────────────────────────────────────────────────────

                               Implementation Roadmap                                

                            Phase 1: Knowledge Expansion                             

 1 Analyze the Golden Dawn PDF for unaddressed insights.                             
 2 Update the card schema to include new fields (e.g., ritual significance, spiritual
   development).                                                                     
 3 Enhance the RAG system to handle advanced Golden Dawn concepts.                   

                          Phase 2: RAG System Improvements                           

 1 Implement document chunking for better context retrieval.                         
 2 Add metadata fields for version control and source tracking.                      
 3 Integrate with the interpretation engine for dynamic context updates.             

                     Phase 3: Interpretation Engine Enhancements                     

 1 Incorporate ritual significance and spiritual development into interpretations.   
 2 Add support for advanced reading methods (e.g., pathworking, meditation guidance).

                               Phase 4: Novel Features                               

 1 Develop guided meditations based on card symbolism.                               
 2 Create interactive learning modules for Golden Dawn concepts.                     
 3 Build ritual guidance and spiritual development tools.                            

─────────────────────────────────────────────────────────────────────────────────────

                            Error Handling and Monitoring                            

                                     Error Types                                     

 • TarotError: Base exception class for all tarot-related errors.                    
 • DeckError: Errors related to deck operations.                                     
 • ConfigError: Errors related to configuration settings.                            
 • EnrichmentError: Errors during knowledge enrichment.                              
 • EmbeddingError: Errors during embedding generation.                               

                                Monitoring Strategies                                

 • Log all errors with severity levels (INFO, WARNING, ERROR, CRITICAL).             
 • Track API usage and error rates for AI providers.                                 
 • Implement version control for knowledge updates.                                  

─────────────────────────────────────────────────────────────────────────────────────

                                     Next Steps                                      

 1 Analyze the Golden Dawn PDF:                                                      
    • Identify unaddressed insights and novel opportunities.                         
    • Propose updates to the card schema and RAG system.                             
 2 Enhance the RAG System:                                                           
    • Implement document chunking and metadata handling.                             
    • Integrate with the interpretation engine for dynamic context updates.          
 3 Develop New Features:                                                             
    • Guided meditations and interactive learning modules.                           
    • Ritual guidance and spiritual development tools.                               



[Old]
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

## Advanced AI Implementation: Beyond ChatGPT

TarotAI goes far beyond standard AI chatbots through its sophisticated architecture and specialized components:

### 1. Specialized AI Clients
The system uses multiple AI providers, each optimized for specific tasks:

```python
class UnifiedAIClient:
    def __init__(self, config: AISettings):
        self.clients = {
            "voyage": VoyageClient(config.voyage_model),
            "deepseek": DeepSeekClient(config.deepseek_model),
            "anthropic": AnthropicClient(config.anthropic_model)
        }
```

- **DeepSeek**: Handles core meaning generation with multi-token prediction
- **VoyageAI**: Manages advanced embeddings and semantic search
- **Claude**: Provides structured responses and tool calling

### 2. Multimodal Embeddings
Unlike standard chatbots, TarotAI uses multiple types of embeddings:

```python
class CardEmbeddings:
    text_embedding: List[float]
    image_embedding: Optional[List[float]]
    multimodal_embedding: Optional[List[float]]
```

This allows the system to understand both text and visual symbolism, creating richer interpretations.

### 3. Retrieval Augmented Generation (RAG)
The RAG system combines traditional knowledge with modern AI:

```python
class RAGSystem:
    def __init__(self, voyage_client: VoyageClient, ai_client: BaseAIClient):
        self.voyage = voyage_client
        self.ai = ai_client
        self.knowledge_base = KnowledgeBase()
```

Key features:
- Context-aware responses
- Semantic search across modalities
- Dynamic knowledge integration

## Meaning Generation Process

The system generates card meanings through a sophisticated pipeline:

### 1. Initial Data Extraction
The `process_golden_dawn.py` script extracts knowledge from the Golden Dawn PDF:

```python
async def enhanced_process_golden_dawn(pdf_path, ai_clients, card_processor):
    # Extract knowledge using Claude
    pdf_content = extract_pdf_content(pdf_path)
    gd_knowledge = await ai_clients["claude"].extract_structured_knowledge(pdf_content)
```

### 2. Meaning Generation
The CardProcessor class generates meanings using multiple AI models:

```python
class CardProcessor:
    async def generate_meanings(self, card, golden_dawn):
        # Generate keywords if missing
        if not card.get("keywords"):
            card["keywords"] = await self._generate_keywords(card, golden_dawn)
        
        # Generate meanings
        card["upright_meaning"] = await self.ai_client.generate_response(
            f"Generate upright meaning for {card['name']}"
        )
        card["reversed_meaning"] = await self.ai_client.generate_response(
            f"Generate reversed meaning for {card['name']}"
        )
```

### 3. Embedding Creation
The system generates multiple types of embeddings:

```python
async def generate_embeddings(self, card):
    if not card.get("embeddings"):
        card["embeddings"] = {}
    
    card["embeddings"]["upright"] = await self.voyage_client.generate_embedding(
        card["upright_meaning"]
    )
    card["embeddings"]["reversed"] = await self.voyage_client.generate_embedding(
        card["reversed_meaning"]
    )
```

### 4. Data Storage
The processed data is stored in `cards_ordered.json`:

```json
{
  "cards": [
    {
      "name": "The Fool",
      "keywords": ["beginnings", "innocence"],
      "upright_meaning": "New beginnings, taking a leap of faith...",
      "reversed_meaning": "Recklessness, lack of direction...",
      "embeddings": {
        "upright": [0.123, 0.456, 0.789],
        "reversed": [0.321, 0.654, 0.987]
      }
    }
  ]
}
```

## Why This is Better Than Standard AI

1. **Specialized Knowledge**:
   - Trained specifically on tarot symbolism
   - Understands Golden Dawn correspondences
   - Maintains traditional accuracy

2. **Contextual Understanding**:
   - Considers card positions and spreads
   - Understands relationships between cards
   - Provides personalized interpretations

3. **Multimodal Capabilities**:
   - Processes both text and images
   - Creates semantic connections
   - Generates richer insights

4. **Structured Responses**:
   - Provides clear, actionable advice
   - Maintains logical flow
   - Offers practical applications

5. **Continuous Learning**:
   - Improves with each reading
   - Learns from user feedback
   - Adapts to individual styles

## The Future of TarotAI

We're constantly enhancing the system with:
- Better multimodal understanding
- More intuitive interfaces
- Deeper integration with traditional knowledge
- Advanced pattern recognition

```python
╔══════════════════════════════════════════════════════════════╗
║           ◈  Experience the Future of Divination  ◈          ║
║     ╭───────────────────  ⚡  ───────────────────╮         ║
║     │    Where Ancient Wisdom Meets Modern AI    │         ║
║     ╰────────────────────────────────────────────╯         ║
╚══════════════════════════════════════════════════════════════╝
```

This advanced system provides a unique blend of traditional wisdom and cutting-edge technology, offering insights that go far beyond standard AI chatbots.

## Development Tools

### Aider Usage

1. **Starting a Session**:
   ```bash
   aider
   ```

2. **Adding Files**:
   ```bash
   /add src/tarotai/core/models/card.py
   /add tests/core/test_card.py
   ```

3. **Common Commands**:
   - Generate documentation:
     ```bash
     /doc Generate detailed documentation for the CardMeaning class
     ```
   - Refactor code:
     ```bash
     Refactor the TarotInterpreter class to use dependency injection
     ```
   - Write tests:
     ```bash
     Write unit tests for the CardManager class
     ```

4. **Best Practices**:
   - Add relevant files before making changes
   - Use clear, specific prompts
   - Review generated code carefully
   - Commit changes frequently

## 10. Golden Dawn Integration
- PDF processing pipeline
- Knowledge extraction
- Traditional symbolism mapping

## 11. AI and Embedding Architecture

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

The system uses a hierarchical error system with specific error types:

```python
class TarotError(Exception):
    """Base exception class for TarotAI system"""
    def __init__(
        self, 
        message: str, 
        code: str = "UNKNOWN_ERROR", 
        detail: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ):
        self.message = message
        self.code = code
        self.detail = detail or {}
        self.severity = severity
        self.timestamp = datetime.utcnow()
        super().__init__(message)

class DeckError(TarotError): ...
class ConfigError(TarotError): ...
class EnrichmentError(TarotError): ...
class EmbeddingError(TarotError): ...
class ReadingError(TarotError): ...
```

Key features:
- Structured error codes
- Severity levels (INFO, WARNING, ERROR, CRITICAL)
- Timestamped errors
- Detailed error context
- HTTP exception conversion

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

## 9. Reading Interpretation

The TarotInterpreter class handles reading interpretation with RAG and AI integration:

```python
class TarotInterpreter:
    def __init__(self, config: AISettings):
        self.interpretation_cache: Dict[str, Any] = {}
        self.model_router = ModelRouter(config)
        self.rag = RAGSystem(
            voyage_client=VoyageClient(config.voyage_model),
            ai_client=UnifiedAIClient(config)
        )

    async def _generate_interpretation(
        self,
        cards: List[Tuple[CardMeaning, bool]],
        question: Optional[str] = None
    ) -> str:
        """Generate interpretation using model router and RAG"""
```

Key features:
- Retrieval Augmented Generation (RAG) integration
- Model routing for different tasks
- Context-aware interpretation
- Golden Dawn symbolism integration

### 10. Card Processing Workflow

The CardProcessor class handles core card processing logic:

```python
class CardProcessor:
    """Centralized card processing logic"""
    
    def __init__(self, ai_client: BaseAIClient, voyage_client: VoyageClient):
        self.ai_client = ai_client
        self.voyage_client = voyage_client

    async def generate_meanings(self, card: Dict[str, Any], golden_dawn: Dict[str, Any]) -> Dict[str, Any]:
        """Generate upright and reversed meanings for a card"""
        
    async def generate_embeddings(self, card: Dict[str, Any]) -> Dict[str, Any]:
        """Generate embeddings for a card's meanings"""
        
    async def _generate_keywords(self, card: Dict[str, Any], golden_dawn: Dict[str, Any]) -> List[str]:
        """Generate keywords for a card using AI and Golden Dawn knowledge"""
```

Key features:
- AI-assisted meaning generation
- Multimodal embedding support
- Golden Dawn integration
- Structured validation

### 11. Data Structures

#### 11.1 Card Embeddings

```python
@dataclass
class CardEmbeddings:
    """Multi-vector embeddings for a tarot card"""
    text_embedding: List[float]
    image_embedding: Optional[List[float]] = None
    multimodal_embedding: Optional[List[float]] = None
    quantized_embedding: Optional[List[int]] = None
    reduced_dimension_embedding: Optional[List[float]] = None
    version: str = "2.0"
```

#### 11.2 Reading Embeddings

```python
@dataclass
class ReadingEmbeddings:
    """Container for hierarchical embeddings of a reading"""
    card_embeddings: List[CardEmbeddings]
    position_embeddings: List[List[float]] 
    context_embedding: List[float]
    version: int = 2
```

### 12. Extensions

### 12.1 Enrichment Extension

The enrichment extension enhances the core tarot system with AI-powered features and historical analysis.

#### 12.1.1 Key Capabilities
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

## 12. User Workflow Documentation

### 12.1 Initial Setup

1. **Install dependencies**:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   uv pip install -e .
   ```

2. **Configure environment variables**:
   Create a `.env` file with your API keys:
   ```bash
   DEEPSEEK_API_KEY=your_key
   VOYAGEAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   ```

3. **Validate card data**:
   ```bash
   python scripts/data/validate_data.py
   ```

### 12.2 Processing Golden Dawn Knowledge

1. **Place the Golden Dawn PDF**:
   - Copy your Golden Dawn PDF to `data/sources/golden_dawn.pdf`

2. **Run the processing script**:
   ```bash
   python scripts/processing/process_golden_dawn.py
   ```

3. **Verify output**:
   - Check `data/processed/golden_dawn/` for:
     - `golden_dawn_knowledge.json`
     - `golden_dawn_results.json`
     - Extracted images (if VoyageAI is configured)

### 12.3 Generating Card Meanings

1. **Generate initial meanings**:
   ```bash
   python scripts/processing/generate_meanings.py
   ```

2. **Review and refine**:
   - Check `data/cards_ordered.json` for generated meanings
   - Manually edit as needed

### 12.4 Running the CLI Interface

1. **Start interactive mode**:
   ```bash
   tarotai interactive
   ```

2. **Perform a reading**:
   - Choose spread type
   - Enter focus area
   - Ask your question
   - View interpretation

3. **Voice interface** (if configured):
   ```bash
   tarotai voice
   ```

### 12.5 Common Development Tasks

1. **Run tests**:
   ```bash
   pytest tests/
   ```

2. **Format code**:
   ```bash
   black src/ tests/
   ```

3. **Check types**:
   ```bash
   mypy src/ tests/
   ```

4. **Lint code**:
   ```bash
   flake8 src/ tests/
   ```

### 12.6 Working with Aider

1. **Start aider session**:
   ```bash
   aider
   ```

2. **Common commands**:
   - Add files to session:
     ```bash
     /add src/tarotai/core/models/types.py
     ```
   - Generate documentation:
     ```bash
     /doc Generate detailed documentation for the CardMeaning class
     ```
   - Refactor code:
     ```bash
     Refactor the TarotInterpreter class to use dependency injection
     ```

### 12.7 Maintenance Tasks

1. **Clean up project**:
   ```bash
   make clean
   # or
   tarotai-cleanup
   ```

2. **Update dependencies**:
   ```bash
   uv pip compile --upgrade
   uv pip sync
   ```

3. **Validate configuration**:
   ```bash
   python -c "from tarotai.config.schemas.config import get_config; get_config()"
   ```

### 12.8 Troubleshooting

1. **Common issues**:
   - Missing API keys: Verify `.env` file
   - Invalid card data: Run validation script
   - Large files: Check `data/` directory for unnecessary files
   - Performance issues: Check API rate limits

2. **Debugging tips**:
   - Increase log level:
     ```bash
     export LOG_LEVEL=DEBUG
     ```
   - Check logs in `logs/` directory
   - Use verbose mode for scripts:
     ```bash
     python scripts/processing/process_golden_dawn.py --verbose
     ```

### 12.9 Recommended Workflow

1. Start with a clean environment
2. Process Golden Dawn knowledge
3. Generate initial card meanings
4. Validate data and configuration
5. Run interactive CLI for testing
6. Use aider for development tasks
7. Regularly clean and validate the project
8. Update documentation as changes are made

### 12.10 Example Session

```bash
# Setup environment
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install -e .

# Process Golden Dawn knowledge
python scripts/processing/process_golden_dawn.py

# Generate card meanings
python scripts/processing/generate_meanings.py

# Validate data
python scripts/data/validate_data.py

# Start interactive session
tarotai interactive

# Perform a reading
> Choose spread type: Three Card
> Focus area: Career
> Question: What should I focus on in my career?

# Start aider session
aider
/add src/tarotai/core/models/types.py
/help
```

## 13. Data Structures

### 13.1 Card Definitions Schema

```json
{
  "version": "string",  // Schema version
  "last_updated": "string",  // ISO 8601 timestamp
  "schema_version": "string",
  "cards": [
    {
      "number": "int|null",
      "suit": "string",
      "name": "string",
      "element": "string",
      "astrological": "string",
      "kabbalistic": "string",
      "decan": "string|null",
      "keywords": ["string"],
      "upright_meaning": "string",
      "reversed_meaning": "string",
      "golden_dawn": {
        "title": "string",
        "symbolism": ["string"],
        "reading_methods": ["string"],
        "reversed_notes": "string",
        "shadow_aspects": ["string"]
      },
      "embeddings": {
        "upright": ["float"],
        "reversed": ["float"]
      },
      "metadata": {
        "last_updated": "string",
        "source": "string",
        "confidence": "float"
      }
    }
  ]
}
```

### Validation Rules
- All 78 cards must be present
- Required fields: name, number, suit, element, keywords, upright_meaning, reversed_meaning
- Golden Dawn section must be present for all cards
- Embeddings must match expected dimensionality
- Metadata must include source and confidence

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
