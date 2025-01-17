from pydantic import BaseModel

class TarotError(BaseModel):
    message: str
    code: int

class EnrichmentError(TarotError):
    """Error during card enrichment"""
    pass

class EmbeddingError(TarotError):
    """Error during embedding generation"""
    pass
