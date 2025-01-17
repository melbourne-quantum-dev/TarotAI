"""
Retrieval-Augmented Generation (RAG) Manager for TarotAI

Handles document storage, retrieval, and generation of responses using
both local knowledge and AI models.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import logging
from dataclasses import dataclass
from src.tarotai.config.schemas.config import get_config
from src.tarotai.ai.embeddings import EmbeddingManager, EmbeddingStorage
from src.tarotai.ai.clients import BaseAIClient

logger = logging.getLogger(__name__)

@dataclass
class RAGResult:
    """Result container for RAG operations"""
    content: str
    sources: List[str]
    confidence: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for serialization"""
        return {
            "content": self.content,
            "sources": self.sources,
            "confidence": self.confidence,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RAGResult":
        """Create RAGResult from dictionary"""
        return cls(
            content=data["content"],
            sources=data["sources"],
            confidence=data["confidence"],
            metadata=data["metadata"]
        )

class RAGManager:
    """Manages the RAG system for TarotAI"""
    
    def __init__(self, 
                 embedding_manager: EmbeddingManager,
                 ai_client: BaseAIClient,
                 storage: Optional[EmbeddingStorage] = None):
        self.embedding_manager = embedding_manager
        self.ai_client = ai_client
        self.storage = storage or EmbeddingStorage()
        self.config = get_config()
        
    async def index_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Index documents for retrieval"""
        try:
            logger.info(f"Indexing {len(documents)} documents")
            
            # Generate embeddings for each document
            embeddings = await self.embedding_manager.generate_batch_embeddings(
                [doc['content'] for doc in documents]
            )
            
            # Store documents with their embeddings
            for doc, embedding in zip(documents, embeddings):
                self.storage.store_document(
                    content=doc['content'],
                    metadata=doc.get('metadata', {}),
                    embedding=embedding
                )
                
            logger.info("Document indexing completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to index documents: {str(e)}")
            raise

    async def query(self, question: str, top_k: int = 3) -> RAGResult:
        """Query the RAG system with a question"""
        try:
            logger.info(f"Processing RAG query: {question}")
            
            # Generate embedding for the question
            question_embedding = await self.embedding_manager.generate_embedding(question)
            
            # Retrieve relevant documents
            results = self.storage.query(question_embedding, top_k=top_k)
            
            if not results:
                logger.warning("No relevant documents found for query")
                return RAGResult(
                    content="",
                    sources=[],
                    confidence=0.0,
                    metadata={}
                )
                
            # Generate response using AI model
            context = "\n\n".join([r.content for r in results])
            prompt = f"""
            Answer the question based on the context below:
            
            Question: {question}
            
            Context:
            {context}
            """
            
            response = await self.ai_client.generate_response(prompt)
            
            return RAGResult(
                content=response,
                sources=[r.metadata.get('source', 'unknown') for r in results],
                confidence=min(r.score for r in results),
                metadata={
                    'model': self.ai_client.model,
                    'top_k': top_k
                }
            )
            
        except Exception as e:
            logger.error(f"RAG query failed: {str(e)}")
            raise

    async def update_document(self, document_id: str, new_content: str) -> None:
        """Update an existing document in the index"""
        try:
            logger.info(f"Updating document {document_id}")
            
            # Generate new embedding
            new_embedding = await self.embedding_manager.generate_embedding(new_content)
            
            # Update in storage
            self.storage.update_document(document_id, new_content, new_embedding)
            
            logger.info(f"Document {document_id} updated successfully")
            
        except Exception as e:
            logger.error(f"Failed to update document {document_id}: {str(e)}")
            raise

    async def delete_document(self, document_id: str) -> None:
        """Delete a document from the index"""
        try:
            logger.info(f"Deleting document {document_id}")
            self.storage.delete_document(document_id)
            logger.info(f"Document {document_id} deleted successfully")
        except Exception as e:
            logger.error(f"Failed to delete document {document_id}: {str(e)}")
            raise
