"""
Embedding management system for TarotAI
"""
from tarotai.ai.embeddings.manager import EmbeddingManager
from tarotai.ai.embeddings.storage import EmbeddingStorage
from tarotai.core.models.types import CardEmbeddings, ReadingEmbeddings

__all__ = [
    'EmbeddingManager',
    'EmbeddingStorage',
    'CardEmbeddings',
    'ReadingEmbeddings'
]
