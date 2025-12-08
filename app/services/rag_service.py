from typing import List, Dict, Optional
from app.core.config import settings
import logging
import os
import json

logger = logging.getLogger(__name__)


class RAGService:
    """Simple RAG service using file-based storage (100% free, no heavy dependencies)."""
    
    def __init__(self):
        # Initialize storage directory
        os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        self.storage_file = os.path.join(settings.CHROMA_PERSIST_DIRECTORY, "knowledge_base.json")
        self.documents = self._load_documents()
        logger.info("RAG service initialized successfully")
    
    def _load_documents(self) -> List[Dict]:
        """Load documents from file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_documents(self):
        """Save documents to file."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
    
    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ):
        """Add documents to the knowledge base."""
        try:
            if ids is None:
                ids = [f"doc_{len(self.documents) + i}" for i in range(len(documents))]
            
            if metadatas is None:
                metadatas = [{} for _ in documents]
            
            for doc, meta, doc_id in zip(documents, metadatas, ids):
                self.documents.append({
                    "id": doc_id,
                    "content": doc,
                    "metadata": meta
                })
            
            self._save_documents()
            logger.info(f"Added {len(documents)} documents to knowledge base")
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    def query(
        self,
        query_text: str,
        n_results: int = None,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """Query the knowledge base using simple keyword matching."""
        try:
            if n_results is None:
                n_results = settings.TOP_K_RESULTS
            
            # Simple keyword-based search
            query_lower = query_text.lower()
            scored_docs = []
            
            for doc in self.documents:
                # Skip if doesn't match metadata filter
                if filter_metadata:
                    match = all(
                        doc["metadata"].get(k) == v 
                        for k, v in filter_metadata.items()
                    )
                    if not match:
                        continue
                
                # Calculate simple match score
                content_lower = doc["content"].lower()
                score = sum(1 for word in query_lower.split() if word in content_lower)
                
                if score > 0:
                    scored_docs.append((score, doc))
            
            # Sort by score and take top results
            scored_docs.sort(reverse=True, key=lambda x: x[0])
            top_docs = scored_docs[:n_results]
            
            # Format results
            documents = [[doc["content"] for _, doc in top_docs]]
            metadatas = [[doc["metadata"] for _, doc in top_docs]]
            distances = [[1.0 / (score + 1) for score, _ in top_docs]]
            
            return {
                "documents": documents,
                "metadatas": metadatas,
                "distances": distances
            }
            
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
    
    async def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        university_id: Optional[int] = None
    ) -> List[Dict]:
        """Retrieve relevant context from knowledge base (async version for MongoDB)."""
        filter_dict = None
        if university_id:
            filter_dict = {"university_id": university_id}
        
        results = self.query(query, n_results=top_k, filter_metadata=filter_dict)
        
        if not results["documents"] or not results["documents"][0]:
            return []
        
        # Format results as list of dicts
        context_docs = []
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            context_docs.append({
                "text": doc,
                "source": meta.get("source", f"Document {i+1}"),
                "metadata": meta
            })
        
        return context_docs
    
    def get_context_for_query(
        self,
        query: str,
        university_id: Optional[int] = None
    ) -> str:
        """Get relevant context from knowledge base."""
        filter_dict = None
        if university_id:
            filter_dict = {"university_id": university_id}
        
        results = self.query(query, filter_metadata=filter_dict)
        
        if not results["documents"] or not results["documents"][0]:
            return "No relevant information found in the knowledge base."
        
        # Combine top results
        context_parts = []
        for i, doc in enumerate(results["documents"][0]):
            context_parts.append(f"[Source {i+1}]\n{doc}\n")
        
        return "\n".join(context_parts)
    
    def delete_collection(self):
        """Delete the entire collection."""
        self.documents = []
        self._save_documents()
        logger.info("Knowledge base collection deleted")


# Singleton instance
rag_service = RAGService()
