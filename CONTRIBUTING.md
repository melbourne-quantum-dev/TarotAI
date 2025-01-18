# Contributing to TarotAI - Personalized Guide for Fuar

Version 2.1.0

## Development Workflow

### Setup
```bash
# Install dependencies using uv (modern Python package manager)
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install -e ".[dev,docs]"
```

### Running Tests
```bash
# Run all tests
make test

# Run specific test groups
make test-card-manager
make test-reading-input
make test-golden-dawn
```

### Code Formatting
```bash
make format
```

### Type Checking
```bash
make lint
```

---

## Next Phase of Development

### **1. Complete Golden Dawn Processing**
The `process-golden-dawn` pipeline needs to be finalized. Here's what you need to do:

#### **1.1 Update Golden Dawn Knowledge Extraction**
- Review `src/tarotai/extensions/enrichment/knowledge/golden_dawn.py`
- Ensure all Golden Dawn knowledge is properly extracted and structured
- Add validation for extracted data
- Update the `GoldenDawnKnowledgeBase` class to handle edge cases

#### **1.2 Enhance PDF Processing**
- Improve PDF text extraction in `scripts/processing/process_golden_dawn.py`
- Add support for:
  - Symbolism extraction
  - Reading methods
  - Historical approaches
- Implement proper error handling for PDF parsing

#### **1.3 Add Multimodal Support**
- Integrate image processing with VoyageAI
- Generate embeddings for both text and images
- Store processed data in a structured format

#### **1.4 Update Tests**
- Add comprehensive tests for Golden Dawn processing:
  - Unit tests for individual components
  - Integration tests for the full pipeline
  - Edge case testing

---

### **2. Update Documentation**
- Update `docs/architecture/SSOT.md` with:
  - New Golden Dawn processing details
  - Updated system architecture
  - Data flow diagrams
- Add developer documentation for the Golden Dawn integration

---

### **3. Refactor Core Models**
- Review `src/tarotai/core/models/types.py`
- Add new types for Golden Dawn data:
  - `GoldenDawnReadingMethod`
  - `HistoricalApproach`
  - `GoldenDawnLore`
- Ensure proper validation and documentation

---

### **4. Implement Data Validation**
- Add validation rules for Golden Dawn data
- Ensure consistency with Book T sequence
- Validate embeddings and metadata

---

### **5. Finalize CLI Integration**
- Add new commands for Golden Dawn processing:
  - `tarotai process-golden-dawn`
  - `tarotai validate-golden-dawn`
- Update help messages and documentation

---

## Recommended Workflow

1. **Start with Golden Dawn Processing**:
   - Focus on completing the `process-golden-dawn` pipeline
   - Add tests and validation

2. **Update Documentation**:
   - Keep `SSOT.md` up to date
   - Add developer guides

3. **Refactor Core Models**:
   - Add new types and validation
   - Ensure backward compatibility

4. **Implement CLI Commands**:
   - Add new commands for Golden Dawn processing
   - Update help messages

---

## Troubleshooting Tips

- **PDF Parsing Issues**:
  - Check for malformed PDFs
  - Use PyPDF2's debug mode
  - Validate extracted text

- **Embedding Generation**:
  - Monitor API usage
  - Handle rate limits
  - Validate embedding dimensions

- **Data Validation**:
  - Use Pydantic for schema validation
  - Add custom validation rules
  - Log validation errors

---

## Code Quality Standards

- Use type hints consistently
- Follow PEP 8 style guide
- Document all public interfaces
- Implement proper error handling
- Use context managers for resource management
- Follow src-layout project structure

---

For community standards, see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
