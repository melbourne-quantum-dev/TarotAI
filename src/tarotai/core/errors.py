from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import HTTPException

class TarotError(BaseModel):
    """Base error model for TarotAI system"""
    code: str
    message: str
    detail: Optional[Dict[str, Any]] = None

class TarotException(HTTPException):
    """Custom exception for TarotAI system"""
    def __init__(self, error: TarotError, status_code: int = 400):
        super().__init__(status_code=status_code, detail=error.dict())

# Specific error types
class DeckError(TarotError):
    code = "DECK_ERROR"
    message = "An error occurred with the deck"

class ConfigError(TarotError):
    code = "CONFIG_ERROR" 
    message = "Configuration error"

class EnrichmentError(TarotError):
    code = "ENRICHMENT_ERROR"
    message = "Error during card enrichment"

class EmbeddingError(TarotError):
    code = "EMBEDDING_ERROR"
    message = "Error generating embeddings"

class ReadingError(TarotError):
    code = "READING_ERROR"
    message = "Error during reading interpretation"

def handle_error(error: Exception) -> TarotError:
    """Convert exceptions to TarotError format"""
    if isinstance(error, TarotException):
        return error
    return TarotError(
        code="UNKNOWN_ERROR",
        message="An unexpected error occurred",
        detail={"error": str(error)}
    )
