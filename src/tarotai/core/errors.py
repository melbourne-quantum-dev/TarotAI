from typing import Optional, Dict, Any, Literal
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
    code: Literal["DECK_ERROR"] = "DECK_ERROR"
    message: Literal["An error occurred with the deck"] = "An error occurred with the deck"

class ConfigError(TarotError):
    code: Literal["CONFIG_ERROR"] = "CONFIG_ERROR"
    message: Literal["Configuration error"] = "Configuration error"

class EnrichmentError(TarotError):
    code: Literal["ENRICHMENT_ERROR"] = "ENRICHMENT_ERROR"
    message: Literal["Error during card enrichment"] = "Error during card enrichment"

class EmbeddingError(TarotError):
    code: Literal["EMBEDDING_ERROR"] = "EMBEDDING_ERROR"
    message: Literal["Error generating embeddings"] = "Error generating embeddings"

class ReadingError(TarotError):
    code: Literal["READING_ERROR"] = "READING_ERROR"
    message: Literal["Error during reading interpretation"] = "Error during reading interpretation"

def handle_error(error: Exception) -> TarotError:
    """Convert exceptions to TarotError format"""
    if isinstance(error, TarotException):
        return error
    return TarotError(
        code="UNKNOWN_ERROR",
        message="An unexpected error occurred",
        detail={"error": str(error)}
    )
