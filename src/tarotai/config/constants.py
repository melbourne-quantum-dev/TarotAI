from enum import Enum
from typing import Final

class EnvVars(str, Enum):
    """Environment variables with type safety"""
    DEEPSEEK_API_KEY: Final = "DEEPSEEK_API_KEY"
    ANTHROPIC_API_KEY: Final = "ANTHROPIC_API_KEY"
    OPENAI_API_KEY: Final = "OPENAI_API_KEY"
    VOYAGE_API_KEY: Final = "VOYAGE_API_KEY"
    LOG_LEVEL: Final = "LOG_LEVEL"
    DEBUG: Final = "DEBUG"
    DEV_MODE: Final = "DEV_MODE"
    API_MODE: Final = "API_MODE"