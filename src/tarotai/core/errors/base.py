"""
Base Error Classes for TarotAI

This module defines the fundamental error classes used throughout the TarotAI application.
All custom exceptions inherit from TarotError, which provides consistent error handling
and reporting capabilities.
"""

from typing import Any, Optional
from .severity import ErrorSeverity

class TarotError(Exception):
    """Base class for all TarotAI errors."""
    
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        **kwargs: Any
    ) -> None:
        super().__init__(message)
        self.message = message
        self.severity = severity
        self.extra = kwargs

    def __str__(self) -> str:
        return f"[{self.severity.name}] {self.message}"

class TarotAIError(TarotError):
    """Base class for errors specific to AI operations."""
    pass

class TarotHTTPException(TarotError):
    """Exception for HTTP-related errors."""
    pass

class ConfigError(TarotError):
    """Exception for configuration-related errors."""
    pass

class DeckError(TarotError):
    """Exception for deck-related errors."""
    pass

class EnrichmentError(TarotError):
    """Exception for data enrichment errors."""
    pass

class EmbeddingError(TarotError):
    """Exception for embedding-related errors."""
    pass

class ReadingError(TarotError):
    """Exception for tarot reading errors."""
    pass

class AIClientError(TarotError):
    """Exception for AI client-related errors."""
    pass

class ValidationError(TarotError):
    """Exception for validation errors."""
    pass

class ProcessingError(TarotError):
    """Exception for data processing errors."""
    pass

class InterpretationError(TarotError):
    """Exception for interpretation-related errors."""
    pass
