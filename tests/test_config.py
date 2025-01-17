from tarotai.core.config import AISettings, TarotSettings, Settings, get_config
from pydantic import ValidationError
import pytest

def test_ai_settings_defaults():
    """Test AI settings default values"""
    settings = AISettings()
    assert settings.enabled is True
    assert settings.model == "deepseek-chat"
    assert settings.temperature == 0.7

def test_tarot_settings_defaults():
    """Test tarot settings default values"""
    settings = TarotSettings()
    assert settings.default_spread == "three_card"
    assert settings.shuffle_on_start is True
    assert settings.card_order == "book_t"
    assert settings.max_cache_size == 100

def test_settings_validation():
    """Test settings validation"""
    with pytest.raises(ValidationError):
        # Invalid temperature value
        AISettings(temperature=1.5)
    
    with pytest.raises(ValidationError):
        # Invalid max cache size
        TarotSettings(max_cache_size=-1)

def test_get_config():
    """Test configuration loading"""
    config = get_config()
    assert isinstance(config, Settings)
    assert isinstance(config.ai, AISettings)
    assert isinstance(config.tarot, TarotSettings)
