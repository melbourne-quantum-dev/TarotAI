"""Error types and handling for TarotAI"""

from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import datetime
from ..models.types import ErrorSeverity

class TarotError(Exception):
    """Base exception class for TarotAI system"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        code: Optional[str] = None,
        detail: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.severity = severity
        self.code = code or self.__class__.__name__
        self.detail = detail or {}
        self.timestamp = datetime.now()
        super().__init__(message)

class TarotHTTPException(TarotError):
    """HTTP-specific error for API endpoints"""
    def __init__(self, status_code: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code

    def to_http_exception(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "code": self.code,
                "detail": self.detail
            }
        )

class DeckError(TarotError):
    """Errors related to deck operations"""
    pass

class ConfigError(TarotError):
    """Configuration related errors"""
    pass

class EnrichmentError(TarotError):
    """Errors during card enrichment"""
    pass

class EmbeddingError(TarotError):
    """Errors during embedding generation"""
    pass

class ReadingError(TarotError):
    """Errors during tarot reading generation"""
    pass

def handle_error(error: Exception) -> TarotError:
    """Convert any error to TarotError"""
    if isinstance(error, TarotError):
        return error
    
    return TarotError(
        message=str(error),
        severity=ErrorSeverity.ERROR,
        code="UNKNOWN_ERROR",
        detail={"original_error": error.__class__.__name__}
    )

__all__ = [
    'ErrorSeverity',
    'TarotError',
    'TarotHTTPException',
    'DeckError',
    'ConfigError',
    'EnrichmentError',
    'EmbeddingError',
    'ReadingError',
    'handle_error'
]