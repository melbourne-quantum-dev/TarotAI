"""
Error Severity Levels

This module defines the severity levels used for error classification in TarotAI.
The levels help determine the appropriate response to different types of errors.
"""

from enum import Enum, auto

class ErrorSeverity(Enum):
    """
    Enumeration of error severity levels.
    
    Levels:
        LOW: Minor issues that don't affect core functionality
        MEDIUM: Significant issues that may affect some functionality
        HIGH: Critical issues that affect core functionality (default)
    """
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
