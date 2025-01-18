"""Core error definitions and handling for TarotAI.

This module defines the foundational error hierarchy and handling mechanisms.
All system-specific exceptions derive from TarotError, providing consistent
error handling patterns across the application.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import HTTPException
from .severity import ErrorSeverity

class TarotAIError(Exception):
    """Alias for TarotError for backward compatibility.
    
    Note: New code should use TarotError directly.
    """
    pass

class TarotError(TarotAIError):
    """Base exception class for TarotAI system.
    
    Provides structured error information including severity, timing,
    and contextual details for system-wide error handling.
    """
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
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
    """HTTP-specific error for API endpoints.
    
    Bridges between internal error system and FastAPI's HTTP exception handling.
    """
    def __init__(self, status_code: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status_code

    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException for API response handling."""
        return HTTPException(
            status_code=self.status_code,
            detail={
                "message": self.message,
                "code": self.code,
                "detail": self.detail
            }
        )

# Domain-specific errors
class DeckError(TarotError):
    """Errors related to deck operations such as shuffling or drawing cards."""
    pass

class ConfigError(TarotError):
    """Configuration related errors including missing or invalid settings."""
    pass

class EnrichmentError(TarotError):
    """Errors during card enrichment process like meaning generation."""
    pass

class EmbeddingError(TarotError):
    """Errors during embedding generation or vector operations."""
    pass

class ReadingError(TarotError):
    """Errors during tarot reading generation and interpretation."""
    pass

class AIClientError(TarotError):
    """Errors during AI client operations and model interactions."""
    pass

class ValidationError(TarotError):
    """Errors during data validation and verification processes."""
    pass

class ProcessingError(TarotError):
    """Errors during card processing operations and transformations."""
    pass

def handle_error(error: Exception) -> TarotError:
    """Convert any error to TarotError for consistent error handling.
    
    Args:
        error: Any exception instance to be converted or wrapped
        
    Returns:
        TarotError: Either the original error if already a TarotError,
                   or a new TarotError wrapping the original exception.
    
    Example:
        try:
            some_operation()
        except Exception as e:
            raise handle_error(e)
    """
    if isinstance(error, TarotError):
        return error
    
    return TarotError(
        message=str(error),
        severity=ErrorSeverity.HIGH,
        code="UNKNOWN_ERROR",
        detail={"original_error": error.__class__.__name__}
    )