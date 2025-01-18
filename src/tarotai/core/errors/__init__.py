"""
Core error types for TarotAI system.
Provides a structured hierarchy of exceptions for different components.
"""
from enum import Enum
from typing import Any, Dict, Optional

class ErrorSeverity(Enum):
    """Severity levels for TarotAI errors"""
    LOW = "low"           # Minor issues that don't affect core functionality
    MEDIUM = "medium"     # Issues that degrade but don't prevent functionality
    HIGH = "high"         # Issues that prevent specific features from working
    CRITICAL = "critical" # Issues that prevent system operation

from .errors import (
    TarotError,
    TarotHTTPException,
    ConfigError,
    DeckError,
    EnrichmentError,
    EmbeddingError,
    ReadingError,
    AIClientError,
    ValidationError
)

__all__ = [
    'ErrorSeverity',
    'TarotError',
    'TarotHTTPException',
    'ConfigError',
    'DeckError',
    'EnrichmentError',
    'EmbeddingError',
    'ReadingError',
    'AIClientError',
    'ValidationError'
]
