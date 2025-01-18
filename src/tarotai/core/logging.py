"""Core logging configuration for TarotAI"""

import logging
from typing import Optional

def setup_logging(level: Optional[int] = None) -> logging.Logger:
    """Configure logging for TarotAI
    
    Args:
        level: Logging level (defaults to INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("tarotai")
    logger.setLevel(level or logging.INFO)
    
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(ch)
    
    return logger
