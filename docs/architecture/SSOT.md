                                                    TarotAI System Documentation
                                                    Version 2.2.0 (2025-01-19)

## AI Assistant Instructions

As an AI assistant working with this codebase:

1. **Role and Scope**
- You are assisting with the TarotAI project development
- Follow the architecture and patterns documented here
- Respect all security and validation requirements

2. **Code Generation Guidelines**
- Use type hints consistently
- Follow async patterns for I/O operations
- Implement error handling as specified
- Generate tests for new code

3. **Knowledge Access**
- Use RAG system for tarot knowledge queries
- Respect the Golden Dawn system as primary source
- Maintain separation of concerns in knowledge access
- Follow the validation chain for all operations

4. **Response Format**
- Provide code with complete type annotations
- Include docstrings in Google format
- Explain architectural decisions
- Reference relevant sections of this document

5. **Limitations**
- Do not modify core knowledge base directly
- Respect rate limits and token budgets
- Maintain strict validation boundaries
- Follow security guidelines for sensitive data

## System Requirements

- Python 3.12+
- Vector store compatibility
- GPU support (optional, for embedding generation)
- Minimum 4GB RAM
- API keys for:
  - Claude
  - DeepSeek
  - Voyage

## Development Guidelines

- Follow PEP 8 style guide
- Async/await for all I/O operations
- Type hints required
- Documentation in Google style
- Test coverage minimum 80%

## Deployment

### Environment Setup
- Virtual environment recommended
- Configuration via environment variables
- API keys stored in `.env`

### Production Considerations
- Rate limiting implementation
- Error monitoring
- Performance tracking
- Backup strategies

## Security Considerations

### API Security
- Key rotation policy
- Request signing
- Rate limiting

### Data Protection
- PII handling
- Data retention policies
- Encryption at rest

## AI Development Context

### Agent Interaction Guidelines
- Use structured prompts from `prompts/templates/`
- Follow the RAG pipeline for knowledge queries
- Respect rate limits and token budgets
- Handle partial or incomplete responses gracefully

### Knowledge Base Context
- Golden Dawn system is primary source
- Historical context preserved in vector store
- Symbolism hierarchies maintained
- Cross-references validated

### Development Workflow
- AI-assisted code generation follows type system
- Validation chain: local → CI → production
- Template-first approach for new features
- Consistent error handling patterns

### Model Requirements
- Claude: Complex reasoning, validation
- DeepSeek: Core interpretation tasks
- Voyage: Embedding generation, similarity search

### Context Boundaries
- Strict separation of interpretation logic
- Knowledge base immutability
- Clear validation chains
- Explicit error surfaces

                                                      Project Structure

TarotAI
├── src/tarotai/
│   ├── ai/                           # AI Integration Layer
│   │   ├── agents/                   # AI Agent System
│   │   │   ├── base.py               # Base Agent Class
│   │   │   ├── interpretation.py     # Interpretation Agent
│   │   │   ├── knowledge.py          # Knowledge Agent
│   │   │   └── validation.py         # Validation Agent
│   │   ├── clients/                  # Provider Implementations
│   │   │   ├── providers/           
│   │   │   │   ├── claude.py         # Claude AI Integration
│   │   │   │   ├── deepseek_v3.py    # DeepSeek Integration
│   │   │   │   └── voyage.py         # Voyage AI Integration
│   │   │   ├── base.py               # Base Client Interface
│   │   │   └── unified.py            # Unified Client Manager
│   │   ├── embeddings/               # Embedding System
│   │   ├── knowledge/                # Knowledge Processing
│   │   ├── prompts/                  # Prompt Management
│   │   │   └── templates/            # J2 Templates
│   │   └── rag/                      # RAG System
│   ├── core/                         # Core Business Logic
│   │   ├── models/                   # Data Models
│   │   │   ├── card.py               # Card Representations
│   │   │   ├── deck.py               # Deck Management
│   │   │   └── types.py              # Type Definitions
│   │   ├── services/                 # Core Services
│   │   │   ├── interpreter.py        # Reading Interpretation Service
│   │   │   └── reading.py            # Reading Management
│   │   └── errors/                   # Error System
│   ├── extensions/                   # Optional Features
│   │   └── enrichment/               # Knowledge Enrichment
│   └── ui/                           # User Interface
├── data/                             # Data Storage
│   ├── cards_ordered.json            # Base Card Data
│   ├── golden_dawn.json              # Processed GD Data
│   └── processed/                    # Processed Data
├── tests/                            # Test Suite
│   ├── core/                         # Core Tests
│   ├── ai/                           # AI Integration Tests
│   └── extensions/                   # Extension Tests
└── docs/                             # Documentation
    └── architecture/                 # System Architecture

                                                    Key Components

## Key Components

### AI Integration Layer (`ai/`)
- **Agent System** (`agents/`)
  - Orchestration agents manage reading flow and interpretation
  - Validation agents ensure data quality and format compliance
  - Knowledge agents handle information retrieval and enrichment
  
- **Client System** (`clients/`)
  - Unified interface (`unified.py`) for consistent AI interaction
  - Provider-specific implementations for Claude, DeepSeek, and Voyage
  - Registry pattern for dynamic provider management
  
- **RAG System** (`rag/`)
  - Vector storage for semantic search
  - Response generation with context augmentation
  - Knowledge base integration
  
- **Knowledge System** (`knowledge/`)
  - Golden Dawn implementation
  - Historical context management
  - Symbolism analysis

### Core Business Logic (`core/`)
- **Data Models** (`models/`)
  - Card and deck representations
  - Reading structures
  - Input/output formats

- **Validation System** (`validation/`)
  - Input validation
  - Output verification
  - Format compliance checks

- **Error Management** (`errors/`)
  - Structured error handling
  - Severity classification
  - Recovery strategies

### Configuration Management (`config/`)
- Schema-based configuration
- Environment-specific settings
- Validation rules

### Testing Infrastructure (`tests/`)
- Mirror structure of source code
- Integration test suites
- Validation test cases
                                                        Implementation Details

### Agent System Architecture

The agent system follows a modular, hierarchical design with three main types of agents:

1. **Base Agent Interface**
```python
class BaseAgent(ABC):
    """Base class for all AI agents in the system."""
    def __init__(self, ai_client: Optional[UnifiedAIClient] = None):
        self.ai_client = ai_client
    
    @abstractmethod
    async def process(self, *args, **kwargs):
        """Process the input and return results"""

class InterpretationAgent(BaseAgent):
    """Handles tarot reading interpretations"""
    async def process(self, reading_input: ReadingInput) -> ReadingInterpretation:
        prompt = self.prompt_manager.get_template("interpretation.j2").render(reading=reading_input)
        response = await self.ai_client.generate(prompt, model="deepseek")
        return self._parse_interpretation(response)

class KnowledgeAgent(BaseAgent):
    """Manages knowledge retrieval and enrichment"""
    async def process(self, query: str) -> EnrichedKnowledge:
        embeddings = await self.ai_client.embed(query, model="voyage")
        context = await self.rag_system.retrieve(embeddings)
        prompt = self.prompt_manager.get_template("knowledge_enrichment.j2").render(query=query, context=context)
        response = await self.ai_client.generate(prompt, model="claude")
        return self._parse_enriched_knowledge(response)

class ValidationAgent(BaseAgent):
    """Validates card data and interpretations"""
    async def process(self, data: Union[CardData, ReadingInterpretation]) -> ValidationResult:
        schema = self._get_validation_schema(type(data))
        prompt = self.prompt_manager.get_template("validation.j2").render(data=data, schema=schema)
        response = await self.ai_client.generate(prompt, model="claude")
        return self._parse_validation_result(response)

2. Core Service Integration

class InterpreterService:
    def __init__(self):
        self.interpretation_agent = InterpretationAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.validation_agent = ValidationAgent()
        self.cache = ResponseCache()

    async def perform_reading(self, reading_input: ReadingInput) -> ReadingResult:
        try:
            # Check cache first
            if cached_result := self.cache.get(reading_input):
                return cached_result

            # Perform reading
            interpretation = await self.interpretation_agent.process(reading_input)
            
            # Enrich with knowledge
            enriched_interpretation = await self.knowledge_agent.process(interpretation)
            
            # Validate result
            validation = await self.validation_agent.process(enriched_interpretation)
            
            if validation.is_valid:
                result = ReadingResult(interpretation=enriched_interpretation, validation=validation)
                self.cache.set(reading_input, result)
                return result
            else:
                return await self._handle_invalid_result(reading_input, validation)
        except Exception as e:
            return await self._handle_error(e, reading_input)

3. Knowledge Processing Pipeline

RAGSystem
├── Input Processing
│   ├── TextChunker(chunk_size=512, overlap=64)
│   └── EmbeddingGenerator(model="voyage")
├── Retrieval
│   ├── VectorStore.similarity_search()
│   └── RelevanceReranker(threshold=0.90)
└── Generation
    ├── ContextBuilder(max_tokens=1024)
    └── ResponseGenerator(temperature=0.5)

                                                Context Requirements

Knowledge Context
- Base card meanings loaded
- Golden Dawn correspondences available
- Historical context accessible
- User preference data integrated

Processing Context
- RAG system initialized with current knowledge
- Embeddings pre-generated and indexed
- Templates loaded and validated
- Agent system ready and configured

Response Context
- Output schema validation active
- Error handling context available
- Response formatting rules applied
- Confidence scoring mechanism active

                                                Future Enhancements

1. Agent System Improvements
   - Implement multi-agent collaboration for complex readings
   - Develop specialized agents for different tarot traditions
   - Integrate reinforcement learning for agent performance optimization

2. Knowledge Integration Enhancements
   - Implement dynamic knowledge graph for real-time updates
   - Develop cross-referencing system for multi-source validation
   - Integrate user feedback loop for continuous knowledge refinement

3. Service Layer Advancements
   - Implement adaptive caching based on usage patterns
   - Develop modular plugin system for easy feature extensions
   - Create advanced error recovery and fallback mechanisms

4. AI Model Improvements
   - Explore fine-tuning options for tarot-specific language models
   - Implement model versioning and automatic performance tracking
   - Develop hybrid AI systems combining symbolic and neural approaches

5. User Experience Enhancements
   - Create personalized reading experiences based on user history
   - Implement voice and natural language interfaces
   - Develop AR/VR interfaces for immersive tarot experiences

                                                Implementation Strategy

                                                Core Generation Pipeline

1. Agent-Based Generation System
```python
class GenerationPipeline:
    def __init__(self):
        self.interpretation_agent = InterpretationAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.validation_agent = ValidationAgent()
        
    async def generate_reading(self, reading_input: ReadingInput) -> ReadingResult:
        # Knowledge enrichment
        enriched_context = await self.knowledge_agent.process(reading_input)
        
        # Generate interpretation
        interpretation = await self.interpretation_agent.process(
            reading_input, 
            context=enriched_context
        )
        
        # Validate result
        validation = await self.validation_agent.process(interpretation)
        
        return ReadingResult(
            interpretation=interpretation,
            validation=validation,
            context=enriched_context
        )

2. Template System

# interpretation_template.j2
{
    "reading": {
        "cards": [
            {% for card in cards %}
            {
                "name": "{{ card.name }}",
                "position": {{ card.position }},
                "reversed": {{ card.reversed }},
                "interpretation": {
                    "core_meaning": "",
                    "context_specific": "",
                    "advice": ""
                }
            }
            {% endfor %}
        ],
        "synthesis": {
            "overall_theme": "",
            "key_insights": [],
            "guidance": ""
        }
    }
}

# validation_template.j2
{
    "validation": {
        "is_valid": boolean,
        "confidence": float,
        "checks": [
            {
                "aspect": str,
                "passed": boolean,
                "notes": str
            }
        ]
    }
}

3. Integration Flow

class ReadingOrchestrator:
    def __init__(self):
        self.pipeline = GenerationPipeline()
        self.template_manager = TemplateManager()
        
    async def perform_reading(self, cards: List[Card], context: ReadingContext) -> Reading:
        # Prepare templates
        interpretation_template = self.template_manager.get("interpretation.j2")
        validation_template = self.template_manager.get("validation.j2")
        
        # Generate reading
        result = await self.pipeline.generate_reading(
            ReadingInput(
                cards=cards,
                context=context,
                templates={
                    "interpretation": interpretation_template,
                    "validation": validation_template
                }
            )
        )
        
        return self._format_result(result)

Key Features:

Agent-based architecture
  Template-driven generation
  Structured validation
  Context-aware processing
  Implementation Notes:

Each agent handles a specific aspect of the reading
  Templates ensure consistent output structure
  Validation occurs at multiple stages
  Context flows through entire pipeline

  ## Project Structure Verification

The project includes a verification script ([verify_project_structure.py](cci:7://file:///home/fuar/projects/TarotAI/verify_project_structure.py:0:0-0:0)) that ensures:

### Directory Structure
- `/src/tarotai/` - Main package source code
  - [ai/](cci:1://file:///home/fuar/projects/TarotAI/verify_project_structure.py:115:0-123:19) - AI-related modules
  - `core/` - Core functionality
  - `config/` - Configuration management
  - `ui/` - User interface components

### Test Structure
- `/tests/` - Mirrors the source code structure
  - Unit tests follow the pattern `test_*.py`
  - Each source module has a corresponding test module

### Development Tools
- Root-level configuration files (`.envrc`, `setup.py`, etc.)
- Development scripts in `/scripts/`
- Documentation in `/docs/`

### Verification
Run the structure verification:
```bash
python3 verify_project_structure.py