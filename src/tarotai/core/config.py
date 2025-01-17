from pydantic import Field, validator
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Dict, Any, Optional
from .errors import ConfigError

class AISettings(BaseSettings):
    """Configuration for AI providers"""
    enabled: bool = Field(default=True)
    api_key: str = Field(..., env="AI_API_KEY")
    model: str = Field(default="deepseek-chat")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class TarotSettings(BaseSettings):
    """Configuration for tarot-specific settings"""
    default_spread: str = Field(default="three_card")
    shuffle_on_start: bool = Field(default=True)
    card_order: str = Field(default="book_t")
    max_cache_size: int = Field(default=100, gt=0)
    data_dir: Path = Field(default=Path("data"))
    
    @validator('data_dir')
    def validate_data_dir(cls, v):
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v

class Settings(BaseSettings):
    """Main application settings"""
    ai: AISettings = Field(default_factory=AISettings)
    tarot: TarotSettings = Field(default_factory=TarotSettings)
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)
    dev_mode: bool = Field(default=False, description="Enable developer features")
    api_mode: bool = Field(default=False, description="Enable API interface")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"

def get_config() -> Settings:
    """Get application configuration"""
    try:
        return Settings()
    except Exception as e:
        raise ConfigError(
            code="CONFIG_ERROR",
            message="Failed to load configuration",
            detail={"error": str(e)}
        )
