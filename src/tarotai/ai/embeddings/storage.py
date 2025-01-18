from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass
import logging
from tarotai.core.models.types import CardEmbeddings, ReadingEmbeddings

logger = logging.getLogger(__name__)

@dataclass
class Document:
    """Represents a stored document with its embedding"""
    content: str
    metadata: Dict[str, Any]
    embedding: np.ndarray
    document_id: str

class EmbeddingStorage:
    """Stores and retrieves documents with their embeddings"""
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        
    def store_document(self, content: str, metadata: Dict[str, Any], embedding: np.ndarray) -> str:
        """Store a document with its embedding"""
        document_id = str(len(self.documents))
        document = Document(
            content=content,
            metadata=metadata,
            embedding=embedding,
            document_id=document_id
        )
        self.documents[document_id] = document
        return document_id
        
    def query(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Document]:
        """Query documents by similarity to the query embedding"""
        if not self.documents:
            return []
            
        # Calculate cosine similarity between query and all documents
        similarities = []
        for doc in self.documents.values():
            similarity = np.dot(query_embedding, doc.embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc.embedding)
            )
            similarities.append((doc, similarity))
            
        # Sort by similarity and return top_k results
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in similarities[:top_k]]
        
    def update_document(self, document_id: str, new_content: str, new_embedding: np.ndarray) -> None:
        """Update an existing document"""
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")
        self.documents[document_id].content = new_content
        self.documents[document_id].embedding = new_embedding
        
    def delete_document(self, document_id: str) -> None:
        """Delete a document from storage"""
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")
        del self.documents[document_id]
