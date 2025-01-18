from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import HTTPException
from . import ErrorSeverity  # Import ErrorSeverity from the package


class TarotError(Exception):
    """Base exception class for TarotAI system"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,  # Changed from ERROR to HIGH
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
        severity=ErrorSeverity.HIGH,
        code="UNKNOWN_ERROR",
        detail={"original_error": error.__class__.__name__}
    )

class AIClientError(TarotError):
    """Errors during AI client operations"""
    pass

class ValidationError(TarotError):
    """Errors during data validation"""
    pass

class ProcessingError(TarotError):
    """Errors during card processing operations"""
    pass
