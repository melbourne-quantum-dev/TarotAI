from tarotai.core.config import get_config, Settings, AISettings, TarotSettings

def test_config_loading():
    """Test that config loads without errors"""
    config = get_config()
    assert isinstance(config, Settings)
    assert isinstance(config.ai, AISettings)
    assert isinstance(config.tarot, TarotSettings)

def test_default_values():
    """Test that default values are set correctly"""
    config = get_config()
    assert config.ai.temperature == 0.7
    assert config.tarot.default_spread == "three_card"
    assert config.tarot.shuffle_on_start is True
