"""Severity levels for TarotAI error system.

Provides enumerated severity levels for error classification across the system.
Each level indicates a distinct impact category for system operations.
"""

from enum import Enum

class ErrorSeverity(Enum):
    """Severity levels for TarotAI errors"""
    LOW = "low"           # Minor issues that don't affect core functionality
    MEDIUM = "medium"     # Issues that degrade but don't prevent functionality
    HIGH = "high"         # Issues that prevent specific features from working
    CRITICAL = "critical" # Issues that prevent system operation

    def __str__(self) -> str:
        """String representation matches value for backward compatibility"""
        return self.value