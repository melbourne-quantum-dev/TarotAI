from tarotai.core.errors import TarotError, DeckError
from tarotai.core.exceptions import TarotException

def test_tarot_error_creation():
    """Test basic error creation"""
    error = TarotError(
        code="TEST_ERROR",
        message="Test error message",
        detail={"key": "value"}
    )
    assert error.code == "TEST_ERROR"
    assert "Test error message" in str(error)

def test_deck_error():
    """Test deck-specific error"""
    error = DeckError(
        code="DECK_ERROR",
        message="Test deck error",
        detail={"card": "The Fool"}
    )
    assert "DECK_ERROR" in str(error)
    assert "The Fool" in str(error.detail)

def test_tarot_exception():
    """Test exception creation"""
    error = TarotError(
        code="EXCEPTION_TEST",
        message="Test exception"
    )
    exception = TarotException(error, status_code=400)
    assert exception.status_code == 400
    assert "EXCEPTION_TEST" in str(exception)
