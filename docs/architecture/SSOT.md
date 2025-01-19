                                                    TarotAI System Documentation
                                                    Version 2.1.0 (2025-01-19)

                                                      Project Structure

TarotAI
├── src/tarotai/
│   ├── ai/                           # AI Integration Layer
│   │   ├── clients/                  # Provider Implementations
│   │   │   ├── providers/           
│   │   │   │   ├── claude.py        # Claude AI Integration
│   │   │   │   ├── deepseek_v3.py   # DeepSeek Integration
│   │   │   │   └── voyage.py        # Voyage AI Integration
│   │   │   ├── base.py              # Base Client Interface
│   │   │   └── unified.py           # Unified Client Manager
│   │   ├── embeddings/              # Embedding System
│   │   ├── knowledge/               # Knowledge Processing
│   │   ├── prompts/                 # Prompt Management
│   │   │   └── templates/           # J2 Templates
│   │   └── rag/                     # RAG System
│   ├── core/                        # Core Business Logic
│   │   ├── models/                  # Data Models
│   │   │   ├── card.py             # Card Representations
│   │   │   ├── deck.py             # Deck Management
│   │   │   └── types.py            # Type Definitions
│   │   ├── services/               # Core Services
│   │   │   ├── agents.py           # AI Agents
│   │   │   ├── interpreter.py      # Reading Interpretation
│   │   │   └── reading.py          # Reading Management
│   │   └── errors/                 # Error System
│   ├── extensions/                  # Optional Features
│   │   └── enrichment/             # Knowledge Enrichment
│   └── ui/                         # User Interface
├── data/                           # Data Storage
│   ├── cards_ordered.json          # Base Card Data
│   ├── golden_dawn.json            # Processed GD Data
│   └── processed/                  # Processed Data
├── tests/                          # Test Suite
│   ├── core/                       # Core Tests
│   ├── ai/                         # AI Integration Tests
│   └── extensions/                 # Extension Tests
└── docs/                           # Documentation
    └── architecture/               # System Architecture

                                                    Key Components

AI Integration Layer
    Multiple Provider Support (Claude, DeepSeek, Voyage)
    Unified Client Interface
    RAG System Integration
    Template-based Prompting

Core Business Logic
    Card and Deck Models
    Reading Services
    Interpretation Engine
    Error Management

Extensions
    Knowledge Enrichment
    Golden Dawn Integration
    Reading History

Data Management
    Structured Card Data
    Processed Knowledge
    Embeddings Storage
    Validation System


                                                        Implementation Details

1. AI Integration Points
```python
UnifiedAIClient
├── Provider Selection
│   ├── DeepSeek: Primary reasoning and interpretation
│   ├── Voyage: Embedding and knowledge retrieval
│   └── Claude: Structured output and validation
├── Context Management
│   ├── PromptTemplate(template_path="templates/reading_interpretation.j2")
│   └── KnowledgeContext(golden_dawn=True, base_cards=True)
└── Response Processing
    └── ResponseValidator(schema=reading_schema)


2. Knowledge Processing Pipeline

RAGSystem
├── Input Processing
│   ├── TextChunker(chunk_size=1024, overlap=128)
│   └── EmbeddingGenerator(model="voyage")
├── Retrieval
│   ├── VectorStore.similarity_search()
│   └── RelevanceReranker(threshold=0.85)
└── Generation
    ├── ContextBuilder(max_tokens=2048)
    └── ResponseGenerator(temperature=0.7)


3. Core Service Integration

TarotInterpreter
├── Knowledge Sources
│   ├── BaseKnowledge("cards_ordered.json")
│   └── GoldenDawnKnowledge("golden_dawn.json")
├── Reading Methods
│   ├── StandardReading(spread_type="celtic_cross")
│   └── GoldenDawnMethod(ritual_context=True)
└── Response Generation
    ├── StructuredOutput(format="json")
    └── NarrativeOutput(style="interpretive")

                                                Context Requirements
Knowledge Context
Base card meanings must be loaded
Golden Dawn correspondences available
Historical context accessible
Processing Context
RAG system initialized with current knowledge
Embeddings pre-generated and indexed
Templates loaded and validated
Response Context
Output schema validation active
Error handling context available
Response formatting rules applied

                                                Technical Implementation Details

4. Data Processing Pipeline Issues

ProcessingPipeline
├── generate_meanings.py
│   ├── Current Issues
│   │   ├── Batch processing (5 cards) without proper error recovery
│   │   ├── Missing keyword generation fallback
│   │   └── Incomplete embedding validation
│   └── Integration Points
│       ├── DEFAULT_KNOWLEDGE fallback when GD fails
│       └── Async batch processing without proper rate limiting
│
├── process_golden_dawn.py
│   ├── Critical Failures
│   │   ├── Incomplete merging of GD symbolism
│   │   ├── Missing validation for reading_methods
│   │   └── Inconsistent title mapping
│   └── Data Structure Mismatches
│       ├── cards_ordered.json expects ["cards"] array
│       └── golden_dawn.json uses flat dictionary

5. Data Integrity Issues

cards_ordered.json
├── Schema Violations
│   ├── Missing required fields
│   │   ├── golden_dawn.symbolism
│   │   └── golden_dawn.reading_methods
│   └── Inconsistent metadata
│       ├── confidence scores missing
│       └── source attribution incomplete
└── Integration Failures
    ├── Partial GD merges
    └── Orphaned embeddings

6. Recovery Strategy

DataRecovery
├── Phase 1: Validation
│   ├── validate_card_schema.py
│   └── check_golden_dawn_integrity()
├── Phase 2: Reconstruction
│   ├── rebuild_missing_embeddings()
│   └── regenerate_incomplete_meanings()
└── Phase 3: Verification
    ├── validate_merged_data()
    └── verify_embedding_consistency()


                                                Implementation Strategy

1. Core Generation Pipeline
```python
# generate_meanings.py
class MeaningGenerator:
    def __init__(self):
        self.deepseek = DeepSeekClient()  # Primary for structured reasoning
        self.claude = ClaudeClient()       # Backup for validation
        self.batch_size = 3                # Reduced from 5 for reliability
        
    async def generate_card_batch(self, cards: List[str]):
        results = []
        for card in cards:
            try:
                # Primary generation with DeepSeek
                meaning = await self.deepseek.generate(
                    template="card_meaning.j2",
                    context={"card": card, "require_structure": True}
                )
                # Validation with Claude
                validated = await self.claude.validate_structure(
                    meaning, schema="card_schema.json"
                )
                results.append(validated)
            except AIError:
                results.append(await self._fallback_generation(card))

Interim Golden Dawn Integration

# First pass without PDF processing
class GoldenDawnIntegrator:
    def __init__(self):
        self.base_knowledge = self._load_base_mappings()
        self.voyage = VoyageClient()  # For semantic matching
        
    async def enrich_card_data(self, card_data: Dict):
        # Start with known correspondences
        gd_data = self.base_knowledge.get(card_data['name'], {})
        
        # Enhance with semantic search
        similar_concepts = await self.voyage.similarity_search(
            card_data['name'],
            threshold=0.85
        )
        
        return {
            **card_data,
            'golden_dawn': {
                'symbolism': gd_data.get('symbolism', []),
                'correspondences': similar_concepts,
                'confidence': 0.85 if gd_data else 0.6
            }
        }

Data Validation Pipeline

# validate_card_schema.py
class CardValidator:
    required_fields = {
        'name': str,
        'number': int,
        'suit': str,
        'meanings': {
            'upright': list,
            'reversed': list
        },
        'keywords': list,
        'golden_dawn': {
            'symbolism': list,
            'confidence': float
        }
    }
    
    def validate_card(self, card: Dict) -> Tuple[bool, List[str]]:
        errors = []
        for field, field_type in self.required_fields.items():
            if not self._validate_field(card, field, field_type):
                errors.append(f"Missing/invalid field: {field}")
        return len(errors) == 0, errors


Phased Implementation Plan

Phase 1: Base Functionality
├── Generate basic meanings (DeepSeek)
├── Implement validation (Claude)
└── Create basic GD mappings (manual)

Phase 2: Enhanced Generation
├── Add keyword extraction
├── Implement confidence scoring
└── Add semantic enrichment

Phase 3: GD Integration
├── Start with known correspondences
├── Add semantic matching
└── Prepare for future PDF processing

                                                Template Implementation

1. Card Generation Templates (card_generation.j2)
```python
# Primary Template for DeepSeek
Generate structured card meaning for {{ card.name }}:
{
    "name": "{{ card.name }}",
    "number": {{ card.number }},
    "suit": "{{ card.suit }}",
    "meanings": {
        "upright": [
            # 5 core meanings with confidence scores
        ],
        "reversed": [
            # 5 core meanings with confidence scores
        ]
    },
    "keywords": [
        # 8-10 essential keywords
    ],
    "associations": {
        "elements": [],
        "astrology": [],
        "numerology": []
    }
}

2. Validation Template (for Claude)

# card_validation.j2
Validate the following card data for {{ card.name }}:
{{ card_data | json }}

Requirements:
1. All required fields present
2. Meanings are contextually accurate
3. Keywords are distinct and relevant
4. Associations follow traditional systems

Return:
{
    "is_valid": boolean,
    "confidence": float,
    "corrections": []
}

3.Semantic Integration (for Voyage)

# semantic_enrichment.j2
Analyze relationships between:
Base Card: {{ card.name }}
Golden Dawn Concepts: {{ gd_concepts | join(', ') }}

Generate:
{
    "semantic_matches": [
        {
            "concept": str,
            "confidence": float,
            "reasoning": str
        }
    ],
    "suggested_integrations": []
}

Implementation Flow

class CardGenerationPipeline:
    def __init__(self):
        self.prompt_manager = PromptTemplateManager()
        self.validators = {
            'structure': self.claude,
            'semantics': self.voyage,
            'content': self.deepseek
        }
    
    async def generate_card(self, card_name: str):
        # 1. Initial Generation (DeepSeek)
        base_data = await self.generate_base_data(card_name)
        
        # 2. Validation (Claude)
        validated = await self.validate_card_data(base_data)
        
        # 3. Semantic Enrichment (Voyage)
        if validated['is_valid']:
            enriched = await self.enrich_card_data(validated['data'])
            return self.finalize_card(enriched)
        
        return await self.handle_generation_failure(card_name)

                                                Prompt System Integration

1. Enhanced Validation System
```python
class CardValidator:
    def __init__(self):
        self.claude = ClaudeClient()
        self.prompt_manager = PromptManager()
        self.validation_cache = {}
    
    async def validate_card_data(self, card_data: Dict) -> Dict:
        # Load and customize validation template
        template = self.prompt_manager.get_template('card_validation.j2')
        validation_prompt = template.render(
            card=card_data,
            validation_rules=self._get_validation_rules(card_data['type'])
        )
        
        try:
            # Primary validation with Claude
            result = await self.claude.validate(
                prompt=validation_prompt,
                temperature=0.3,  # Lower temp for consistent validation
                max_tokens=1000
            )
            
            if result['is_valid']:
                self.validation_cache[card_data['name']] = result
                return result
            
            # If invalid, get specific corrections
            return await self._get_detailed_corrections(card_data, result['corrections'])
            
        except AIError as e:
            return self._fallback_validation(card_data)

2. Semantic Matching System
class SemanticMatcher:
    def __init__(self):
        self.voyage = VoyageClient()
        self.prompt_manager = PromptManager()
        self.embedding_cache = {}
        
    async def enrich_card_data(self, card_data: Dict) -> Dict:
        # Get or generate embeddings
        card_embedding = await self._get_card_embedding(card_data)
        
        # Match with Golden Dawn concepts
        gd_matches = await self._find_gd_matches(card_embedding)
        
        template = self.prompt_manager.get_template('semantic_enrichment.j2')
        enrichment_prompt = template.render(
            card=card_data,
            gd_concepts=gd_matches[:5]  # Top 5 matches
        )
        
        try:
            # Generate semantic relationships
            relationships = await self.voyage.generate_relationships(
                prompt=enrichment_prompt,
                embedding=card_embedding,
                threshold=0.85
            )
            
            # Filter and validate matches
            validated_matches = self._validate_semantic_matches(relationships)
            
            return {
                **card_data,
                'golden_dawn': {
                    'symbolism': validated_matches['symbols'],
                    'correspondences': validated_matches['correspondences'],
                    'confidence': validated_matches['confidence'],
                    'source': 'semantic_matching'
                }
            }
            
        except AIError:
            return self._fallback_enrichment(card_data)
    
    def _validate_semantic_matches(self, matches: Dict) -> Dict:
        # Remove low-confidence matches
        filtered = [m for m in matches['semantic_matches'] 
                   if m['confidence'] > 0.85]
        
        # Group by type
        symbols = [m for m in filtered if m['type'] == 'symbol']
        correspondences = [m for m in filtered if m['type'] == 'correspondence']
        
        # Calculate overall confidence
        confidence = sum(m['confidence'] for m in filtered) / len(filtered)
        
        return {
            'symbols': symbols,
            'correspondences': correspondences,
            'confidence': confidence
        }
Key Features:

1.Validation System
    Template-based validation rules
    Caching for performance
    Detailed correction feedback
    Fallback validation path
2.Semantic Matching
    Embedding-based initial matching
    Confidence scoring
    Type-based grouping
    Fallback enrichment