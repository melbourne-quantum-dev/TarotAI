from typing import List, Dict, Optional
from dataclasses import dataclass
from tarotai.ai.clients.providers.voyage import VoyageClient
from tarotai.ai.clients.base import BaseAIClient
from tarotai.core.models.types import CardEmbeddings, ReadingEmbeddings
from .vector_store import VectorStore

@dataclass
class KnowledgeBase:
    """Stores and retrieves document embeddings"""
    documents: List[str] = []
    embeddings: List[List[float]] = []
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]]):
        """Add documents with their embeddings to the knowledge base"""
        self.documents.extend(documents)
        self.embeddings.extend(embeddings)
        
    def find_similar(self, query_embedding: List[float], top_k: int = 3) -> List[str]:
        """Find similar documents using cosine similarity"""
        # Simple cosine similarity implementation
        from numpy import dot
        from numpy.linalg import norm
        
        similarities = [
            dot(query_embedding, doc_embedding) / (norm(query_embedding) * norm(doc_embedding))
            for doc_embedding in self.embeddings
        ]
        
        # Get top k most similar documents
        sorted_indices = sorted(
            range(len(similarities)),
            key=lambda i: similarities[i],
            reverse=True
        )[:top_k]
        
        return [self.documents[i] for i in sorted_indices]

class RAGSystem:
    """Retrieval Augmented Generation system using VoyageAI"""
    def __init__(self, voyage_client: VoyageClient, ai_client: BaseAIClient):
        self.voyage = voyage_client
        self.ai = ai_client
        self.knowledge_base = KnowledgeBase()
        
    async def add_knowledge(self, documents: List[str]):
        """Index new knowledge documents"""
        embeddings = await self.voyage.generate_batch_embeddings(documents)
        self.knowledge_base.add_documents(documents, embeddings)
        
    async def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context using VoyageAI embeddings"""
        # Generate query embedding
        query_embedding = await self.voyage.generate_embedding(query)
        
        # Find similar documents
        documents = self.knowledge_base.find_similar(query_embedding, top_k)
        
        # Rerank results using VoyageAI's reranking
        if len(documents) > 1:
            documents = await self.voyage.rerank_documents(query, documents)
            
        return "\n\n".join(documents)
    
    async def generate_response(self, query: str, context: str) -> str:
        """Generate response using retrieved context"""
        prompt = f"""
        Use the following context to answer the question:
        
        Context:
        {context}
        
        Question:
        {query}
        """
        return await self.ai.generate_response(prompt)
