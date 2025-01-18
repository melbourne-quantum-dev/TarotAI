"""Legacy compatibility layer for TarotAI error system.

This module provides backward compatibility for code still using the old
import paths (i.e., 'from errors import X'). It redirects these imports
to the new location without requiring immediate codebase updates.
"""

import sys
from ..severity import ErrorSeverity
from ..base import (
    TarotError,
    TarotAIError,
    TarotHTTPException,
    DeckError,
    ConfigError,
    EnrichmentError,
    EmbeddingError,
    ReadingError,
    AIClientError,
    ValidationError,
    ProcessingError,
    handle_error,
)

# Export all symbols for backward compatibility
__all__ = [
    'ErrorSeverity',
    'TarotError',
    'TarotAIError',
    'TarotHTTPException',
    'DeckError',
    'ConfigError',
    'EnrichmentError',
    'EmbeddingError',
    'ReadingError',
    'AIClientError',
    'ValidationError',
    'ProcessingError',
    'handle_error',
]

# Register this module to handle old-style imports
sys.modules['errors'] = sys.modules[__name__]