"""
Configuration Schema Module
--------------------------
Core configuration with version-aware Pydantic imports.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List

import yaml

# Pydantic imports
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# Local imports
from tarotai.core.errors import ConfigError

from .limits import InterpretationLimits

logger = logging.getLogger(__name__)

from .limits import InterpretationLimits


class AISettings(BaseSettings):
    """
    Configuration for AI providers with V2-compatible initialization.
    Handles provider-specific settings and interpretation limits.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
        validate_default=True
    )

    # Core Settings
    enabled: bool = Field(
        default=True, 
        description="Whether the provider is enabled"
    )
    api_key: str = Field(
        default="",
        env=[
            "AI_API_KEY",
            "DEEPSEEK_API_KEY",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "VOYAGE_API_KEY"
        ],
        description="API key for the provider"
    )
    model: str = Field(
        default="deepseek-chat", 
        description="Model name to use"
    )
    
    # Performance Settings
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Sampling temperature (0.0-1.0)"
    )
    max_tokens: int = Field(
        default=4000, 
        gt=0, 
        description="Maximum tokens per API call"
    )
    timeout: int = Field(
        default=30, 
        gt=0, 
        description="API timeout in seconds"
    )
    
    # Interpretation Configuration
    interpretation_limits: InterpretationLimits = Field(
        default_factory=InterpretationLimits.create_default,
        description="Limits for different interpretation types"
    )

    @classmethod
    def create_default(cls) -> "AISettings":
        """Factory method for creating default settings"""
        return cls.model_validate({})

    def model_post_init(self, _context: Any) -> None:
        """Post-initialization validation for complex constraints"""
        if not 0.0 <= self.temperature <= 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0")
        if not 1 <= self.timeout <= 120:
            raise ValueError("Timeout must be between 1 and 120 seconds")

class TarotSettings(BaseSettings):
    """
    Configuration for tarot-specific settings.
    Manages spread types, deck behavior, and data storage.
    """
    
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        validate_default=True
    )

    default_spread: str = Field(default="three_card")
    shuffle_on_start: bool = Field(default=True)
    card_order: str = Field(default="book_t")
    max_cache_size: int = Field(default=100, gt=0)
    data_dir: Path = Field(default=Path("data"))
    allowed_spreads: List[str] = Field(
        default=["single", "three_card", "celtic_cross"]
    )

    def model_post_init(self, _context: Any) -> None:
        """Ensure data directory exists and validate spread types"""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

class UnifiedSettings(BaseSettings):
    """
    Single source of truth for configuration with V2 patterns.
    Coordinates all subsystem configurations and environment integration.
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        validate_default=True
    )

    # Version Control
    version: str = Field(default="2.0.0")
    environment: str = Field(default="development")

    # Provider Configuration with V2 initialization
    ai_providers: Dict[str, AISettings] = Field(
        default_factory=lambda: {
            "deepseek": AISettings.create_default(),
            "anthropic": AISettings.model_validate({
                "enabled": False,
                "model": "claude-3-opus"
            }),
            "openai": AISettings.model_validate({
                "enabled": False,
                "model": "gpt-4-turbo"
            })
        }
    )

    # Core Settings
    tarot: TarotSettings = Field(
        default_factory=lambda: TarotSettings.model_validate({})
    )
    
    # System Configuration
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    dev_mode: bool = Field(default=False)
    api_mode: bool = Field(default=False)

    @classmethod
    def from_yaml(cls, file_path: str) -> "UnifiedSettings":
        """Load settings from YAML with enhanced error handling"""
        if not Path(file_path).exists():
            logger.warning(f"Config file not found at {file_path}, using defaults")
            return cls.model_validate({})

        try:
            with open(file_path) as f:
                yaml_data = yaml.safe_load(f)
                return cls.model_validate(yaml_data)
        except Exception as e:
            raise ConfigError(
                code="YAML_LOAD_ERROR",
                message=f"Failed to load YAML config: {str(e)}",
                detail={"error": str(e), "file": file_path}
            )


def get_config() -> UnifiedSettings:
    """
    Get unified application configuration with comprehensive error handling.
    
    Returns:
        UnifiedSettings: Validated configuration object
        
    Raises:
        ConfigError: If configuration validation fails
    """
    try:
        config = UnifiedSettings.model_validate({})
        logger.info("Successfully loaded configuration")
        return config
    except ValidationError as e:
        error_detail = {
            "error": str(e),
            "fields": [err["loc"] for err in e.errors()],
            "messages": [err["msg"] for err in e.errors()]
        }
        logger.error(f"Configuration validation failed: {error_detail}")
        raise ConfigError(
            code="CONFIG_VALIDATION_ERROR",
            message="Configuration validation failed",
            detail=error_detail
        )
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {str(e)}")
        raise ConfigError(
            code="CONFIG_LOAD_ERROR",
            message="Failed to load configuration",
            detail={"error": str(e)}
        )
