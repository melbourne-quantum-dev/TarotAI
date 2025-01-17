from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CardEmbeddings:
    """Multi-vector embeddings for a tarot card"""
    text_embedding: List[float]
    image_embedding: Optional[List[float]] = None
    multimodal_embedding: Optional[List[float]] = None
    quantized_embedding: Optional[List[int]] = None
    reduced_dimension_embedding: Optional[List[float]] = None
    version: str = "2.0"

@dataclass
class ReadingEmbeddings:
    """Container for hierarchical embeddings of a reading"""
    card_embeddings: List[CardEmbeddings]
    position_embeddings: List[List[float]] 
    context_embedding: List[float]
    version: int = 2
