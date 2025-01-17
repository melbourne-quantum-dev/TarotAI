from pydantic import Field, validator, root_validator
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Dict, Any, Optional, List
from .errors import ConfigError
import yaml

class AISettings(BaseSettings):
    """Configuration for AI providers"""
    enabled: bool = Field(default=True)
    api_key: str = Field(default="", env="AI_API_KEY")
    model: str = Field(default="deepseek-chat")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=1000, gt=0)
    timeout: int = Field(default=30, gt=0)

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
    """Get unified application configuration"""
    try:
        return UnifiedSettings()
    except Exception as e:
        raise ConfigError(
            code="CONFIG_ERROR",
            message="Failed to load configuration",
            detail={"error": str(e)}
        )
