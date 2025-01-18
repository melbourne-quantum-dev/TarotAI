"""
Core error types for TarotAI system.
Provides a structured hierarchy of exceptions for different components.
"""
from enum import Enum
from typing import Optional, Any, Dict

class ErrorSeverity(Enum):
    """Severity levels for TarotAI errors"""
    LOW = "low"           # Minor issues that don't affect core functionality
    MEDIUM = "medium"     # Issues that degrade but don't prevent functionality
    HIGH = "high"         # Issues that prevent specific features from working
    CRITICAL = "critical" # Issues that prevent system operation

class TarotAIError(Exception):
    """Base exception class for TarotAI system"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.severity = severity
        self.details = details or {}
        super().__init__(self.message)

class DeckError(TarotAIError):
    """Raised when deck operations fail"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, severity, details)

class ProcessingError(TarotAIError):
    """Raised when processing operations fail"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, severity, details)

class EnrichmentError(TarotAIError):
    """Raised when enrichment operations fail"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, severity, details)

class EmbeddingError(TarotAIError):
    """Raised when embedding operations fail"""
    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message, severity, details)

class AIClientError(TarotAIError):
    """Raised when AI client operations fail"""
    def __init__(
        self,
        message: str,
        client_name: str,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        details["client_name"] = client_name
        super().__init__(message, severity, details)

class ConfigurationError(TarotAIError):
    """Raised when configuration issues occur"""
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.CRITICAL,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if config_key:
            details["config_key"] = config_key
        super().__init__(message, severity, details)

class ValidationError(TarotAIError):
    """Raised when data validation fails"""
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        severity: ErrorSeverity = ErrorSeverity.HIGH,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if field_name:
            details["field_name"] = field_name
        super().__init__(message, severity, details)

__all__ = [
    'ErrorSeverity',
    'TarotAIError',
    'DeckError',
    'ProcessingError',
    'EnrichmentError',
    'EmbeddingError',
    'AIClientError',
    'ConfigurationError',
    'ValidationError'
]
