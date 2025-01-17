from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import HTTPException

from enum import Enum, auto
from datetime import datetime

class ErrorSeverity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

class TarotError(Exception):
    """Base exception class for TarotAI system"""
    def __init__(
        self, 
        message: str, 
        code: str = "UNKNOWN_ERROR", 
        detail: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.ERROR
    ):
        self.message = message
        self.code = code
        self.detail = detail or {}
        self.severity = severity
        self.timestamp = datetime.utcnow()
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/reporting"""
        return {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
            "severity": self.severity.name,
            "timestamp": self.timestamp.isoformat()
        }

class TarotHTTPException(HTTPException):
    """Custom HTTP exception for TarotAI system"""
    def __init__(self, error: TarotError, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail={
                "code": error.code,
                "message": error.message,
                "detail": error.detail
            }
        )

# Specific error types
class DeckError(TarotError):
    """Errors related to deck operations"""
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DECK_ERROR", detail)

class ConfigError(TarotError):
    """Configuration-related errors"""
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFIG_ERROR", detail)

class EnrichmentError(TarotError):
    """Errors during card enrichment"""
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, "ENRICHMENT_ERROR", detail)

class EmbeddingError(TarotError):
    """Errors during embedding generation"""
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, "EMBEDDING_ERROR", detail)

class ReadingError(TarotError):
    """Errors during reading interpretation"""
    def __init__(self, message: str, detail: Optional[Dict[str, Any]] = None):
        super().__init__(message, "READING_ERROR", detail)

def handle_error(error: Exception) -> TarotError:
    """Convert exceptions to TarotError format"""
    if isinstance(error, TarotError):
        return error
    return TarotError(
        message=str(error),
        code="UNKNOWN_ERROR",
        detail={"original_error": error.__class__.__name__}
    )
