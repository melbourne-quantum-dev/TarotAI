import os
import yaml
from dpath import util as dpath_util
from typing import Any, Optional, Union
from pathlib import Path
from pydantic import BaseModel, ValidationError
from typing import Dict

DEFAULT_CONFIG_PATH = "assistant_config.yml"

class ConfigError(Exception):
    """Base exception for configuration errors"""
    pass

class AIConfig(BaseModel):
    enabled: bool
    api_key: str
    model: str

class TarotConfig(BaseModel):
    default_spread: str
    shuffle_on_start: bool
    card_order: str
    interpretation: Dict[str, Any]
    voice: Dict[str, Any]

def _resolve_env_vars(value: str) -> Any:
    """Resolve environment variables in config values"""
    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
        var_name = value[2:-1]
        if var_name not in os.environ:
            raise ConfigError(f"Environment variable {var_name} not found")
        return os.environ[var_name]
    return value

def get_config(
    dot_path_key: str, 
    config_path: str = DEFAULT_CONFIG_PATH,
    default: Optional[Any] = None,
    required: bool = True
) -> Union[str, dict, list, int, float, bool]:
    """
    Enhanced configuration loader with environment variable support and type safety.
    
    Args:
        dot_path_key: Dot notation path to the config value
        config_path: Path to the YAML config file
        default: Default value if key not found
        required: Whether to raise an error if key not found
        
    Returns:
        The resolved config value
        
    Raises:
        ConfigError: If config file not found or key not found (when required=True)
    """
    abs_config_path = Path(config_path).absolute()
    
    if not abs_config_path.exists():
        if required:
            raise ConfigError(f"Config file not found at {abs_config_path}")
        return default

    try:
        with open(abs_config_path) as f:
            config = yaml.safe_load(f)
            
        value = dpath_util.get(config, dot_path_key, separator=".")
        return _resolve_env_vars(value)
        
    except KeyError:
        if required:
            raise ConfigError(f"Key path '{dot_path_key}' not found in config")
        return default
    except Exception as e:
        raise ConfigError(f"Error loading config: {str(e)}")

def validate_config(config_path: str = DEFAULT_CONFIG_PATH) -> bool:
    """
    Validate the configuration file against the expected schema.
    
    Returns:
        bool: True if config is valid
        
    Raises:
        ValidationError: If config doesn't match expected schema
    """
    try:
        config = yaml.safe_load(open(config_path))
        
        # Validate AI providers
        for provider, settings in config.get('ai', {}).get('providers', {}).items():
            AIConfig(**settings)
            
        # Validate tarot settings
        TarotConfig(**config.get('tarot', {}))
        
        return True
    except ValidationError as e:
        raise ConfigError(f"Configuration validation failed: {str(e)}")
