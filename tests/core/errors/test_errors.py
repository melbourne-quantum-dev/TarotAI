from tarotai.core.errors import TarotError


def test_basic_error():
    """Test basic error creation"""
    error = TarotError(
        code="TEST",
        message="Test message"
    )
    assert error.code == "TEST"
    assert "Test message" in str(error)
