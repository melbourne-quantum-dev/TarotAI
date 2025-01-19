"""
TarotAI Error Handling Module

This module provides a comprehensive error handling system for the TarotAI application.
It includes custom exceptions for various error scenarios that may occur during tarot
readings, AI interactions, and general application operations.
"""

from typing import Any, Dict, Optional, Type

from .base import (
    AIClientError,
    ConfigError,
    DeckError,
    EmbeddingError,
    EnrichmentError,
    InterpretationError,
    ProcessingError,
    ReadingError,
    TarotAIError,
    TarotError,
    TarotHTTPException,
    ValidationError,
)
from .severity import ErrorSeverity

__all__ = [
    "ErrorSeverity",
    "TarotError",
    "TarotAIError",
    "TarotHTTPException",
    "ConfigError",
    "DeckError",
    "EnrichmentError",
    "EmbeddingError",
    "InterpretationError",
    "ReadingError",
    "AIClientError",
    "ValidationError",
    "ProcessingError"
]

def get_error_class(error_type: str) -> Type[TarotError]:
    """
    Get the appropriate error class based on the error type string.
    
    Args:
        error_type: String identifier for the error class
        
    Returns:
        The corresponding error class
        
    Raises:
        ValueError: If the error type is not recognized
    """
    error_map: Dict[str, Type[TarotError]] = {
        "config": ConfigError,
        "deck": DeckError,
        "enrichment": EnrichmentError,
        "embedding": EmbeddingError,
        "interpretation": InterpretationError,
        "reading": ReadingError,
        "ai_client": AIClientError,
        "validation": ValidationError,
        "processing": ProcessingError
    }
    
    if error_type not in error_map:
        raise ValueError(f"Unknown error type: {error_type}")
    
    return error_map[error_type]

def create_error(
    error_type: str,
    message: str,
    severity: ErrorSeverity = ErrorSeverity.HIGH,  # Changed from ERROR to HIGH
    **kwargs: Any
) -> TarotError:
    """
    Factory function to create error instances.
    
    Args:
        error_type: Type of error to create
        message: Error message
        severity: Error severity level (defaults to HIGH)
        **kwargs: Additional error-specific parameters
        
    Returns:
        An instance of the appropriate error class
    """
    error_class = get_error_class(error_type)
    return error_class(message=message, severity=severity, **kwargs)
