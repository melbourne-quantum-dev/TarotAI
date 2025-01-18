from typing import Dict, List, Tuple
from annoy import AnnoyIndex
from tarotai.core.models.types import Reading

class VectorStore:
    """Advanced vector storage and retrieval for readings"""
    
    def __init__(self, embedding_dim: int = 1024):
        self.index = AnnoyIndex(embedding_dim, 'angular')
        self.mapping: Dict[int, Reading] = {}
        self.current_id = 0
        
    def add_reading(self, reading: Reading, embedding: List[float]) -> None:
        """Add a reading with its embedding to the store"""
        self.index.add_item(self.current_id, embedding)
        self.mapping[self.current_id] = reading
        self.current_id += 1
        
    def build_index(self, n_trees: int = 10) -> None:
        """Build the ANN index for faster searches"""
        self.index.build(n_trees)
        
    def find_similar(
        self, 
        target_embedding: List[float], 
        k: int = 5
    ) -> List[Tuple[Reading, float]]:
        """Find similar readings using approximate nearest neighbors"""
        indices, distances = self.index.get_nns_by_vector(
            target_embedding, 
            k, 
            include_distances=True
        )
        return [(self.mapping[i], d) for i, d in zip(indices, distances)]
