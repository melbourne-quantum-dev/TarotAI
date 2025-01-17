try:
    from pydantic import Field, validator, root_validator, ValidationError
    from pydantic_settings import BaseSettings
except ImportError as e:
    raise ImportError(
        "Required packages not found. Please install with: "
        "pip install pydantic>=2.10.5 pydantic-settings>=2.2.1"
    ) from e
from pathlib import Path
from typing import Dict, Any, Optional, List
from tarotai.core.errors import ConfigError
import yaml
import logging

logger = logging.getLogger(__name__)

from .limits import InterpretationLimits

class AISettings(BaseSettings):
    """Configuration for AI providers
    
    Attributes:
        enabled: Whether the provider is enabled
        api_key: API key for the provider
        model: Model name to use
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens per API call
        timeout: API timeout in seconds
        interpretation_limits: Limits for different interpretation types
    """
    enabled: bool = Field(default=True, description="Whether the provider is enabled")
    api_key: str = Field(default="", env=["AI_API_KEY", "DEEPSEEK_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "VOYAGE_API_KEY"], description="API key for the provider")
    model: str = Field(default="deepseek-chat", description="Model name to use")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Sampling temperature (0.0-1.0)")
    max_tokens: int = Field(default=4000, gt=0, description="Maximum tokens per API call")
    timeout: int = Field(default=30, gt=0, description="API timeout in seconds")
    interpretation_limits: InterpretationLimits = Field(
        default_factory=InterpretationLimits,
        description="Limits for different interpretation types"
    )

    @validator('temperature')
    def validate_temperature(cls, v):
        """Validate temperature is within valid range"""
        if not (0.0 <= v <= 1.0):
            raise ValueError("Temperature must be between 0.0 and 1.0")
        return v

    @validator('timeout')
    def validate_timeout(cls, v):
        """Validate timeout is reasonable"""
        if v < 1 or v > 120:
            raise ValueError("Timeout must be between 1 and 120 seconds")
        return v

class TarotSettings(BaseSettings):
    """Configuration for tarot-specific settings"""
    default_spread: str = Field(default="three_card")
    shuffle_on_start: bool = Field(default=True)
    card_order: str = Field(default="book_t")
    max_cache_size: int = Field(default=100, gt=0)
    data_dir: Path = Field(default=Path("data"))
    allowed_spreads: List[str] = Field(default=["single", "three_card", "celtic_cross"])
    
    @validator('data_dir')
    def validate_data_dir(cls, v):
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v

class UnifiedSettings(BaseSettings):
    """Single source of truth for configuration"""
    version: str = Field(default="2.0.0")
    environment: str = Field(default="development")
    
    # AI Providers
    ai_providers: Dict[str, AISettings] = Field(
        default={
            "deepseek": AISettings(),
            "anthropic": AISettings(enabled=False, model="claude-3-opus"),
            "openai": AISettings(enabled=False, model="gpt-4-turbo")
        }
    )
    
    # Tarot Settings
    tarot: TarotSettings = Field(default_factory=TarotSettings)
    
    # System Settings
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    dev_mode: bool = Field(default=False)
    api_mode: bool = Field(default=False)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        yaml_file = "config.yml"
        env_prefix = "TAROTAI_"
        
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # Load YAML first, then env vars, then init
            return (
                init_settings,
                cls.yaml_config_source(cls.yaml_file),
                env_settings,
                file_secret_settings,
            )
        
        @classmethod
        def yaml_config_source(cls, file_path: str):
            """Load YAML configuration"""
            if not Path(file_path).exists():
                return {}
                
            try:
                with open(file_path) as f:
                    return yaml.safe_load(f)
            except Exception as e:
                raise ConfigError(
                    code="YAML_LOAD_ERROR",
                    message="Failed to load YAML config",
                    detail={"error": str(e)}
                )

def get_config() -> UnifiedSettings:
    """Get unified application configuration
    
    Returns:
        UnifiedSettings: Validated configuration object
        
    Raises:
        ConfigError: If configuration validation fails
    """
    try:
        config = UnifiedSettings()
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
