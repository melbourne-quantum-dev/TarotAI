                                                    TarotAI System Documentation
                                                    Version 2.2.0 (2025-03-15)

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

AI Layer (`src/tarotai/ai/`)
- **Agents**
  - `BaseAgent`: Abstract base class for all AI agents
  - `InterpretationAgent`: Handles tarot reading interpretations
  - `KnowledgeAgent`: Manages knowledge retrieval and enrichment
  - `ValidationAgent`: Validates card data and interpretations
- **Clients**
  - Multiple Provider Support (Claude, DeepSeek, Voyage)
  - Unified Client Interface
- **RAG System**
  - Knowledge Processing
  - Embedding System
- **Prompt Management**
  - Template-based Prompting

Core Services (`src/tarotai/core/services/`)
- **Interpreter Service**
  - High-level reading orchestration
  - Caching and configuration
  - Error handling and recovery
  - Service-level coordination
- **Reading Management**
  - Spread type handling
  - Card selection and layout

Data Models
- Card and Deck Models
- Type Definitions

Extensions
- Knowledge Enrichment
- Golden Dawn Integration
- Reading History

Data Management
- Structured Card Data
- Processed Knowledge
- Embeddings Storage
- Validation System

                                                        Implementation Details

1. Agent System Architecture
```python
class BaseAgent:
    """Base class for all AI agents"""
    def __init__(self, ai_client: Optional[UnifiedAIClient] = None):
        self.ai_client = ai_client or UnifiedAIClient()
        self.prompt_manager = PromptManager()

    @abstractmethod
    async def process(self, *args, **kwargs): pass

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