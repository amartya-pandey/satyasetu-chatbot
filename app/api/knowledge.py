from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import List
from app.core.security import get_current_user
from app.services.rag_service import rag_service
import json

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base"])


@router.post("/upload")
async def upload_knowledge(
    documents: List[str] = Form(...),
    metadatas: str = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload documents to knowledge base.
    Admin endpoint to add forgery detection knowledge.
    """
    try:
        metadata_list = json.loads(metadatas) if metadatas else None
        
        rag_service.add_documents(
            documents=documents,
            metadatas=metadata_list
        )
        
        return {
            "message": f"Successfully added {len(documents)} documents to knowledge base",
            "count": len(documents)
        }
    
    except Exception as e:
        return {"error": str(e)}


@router.post("/query")
async def query_knowledge(
    query: str,
    n_results: int = 5,
    current_user: dict = Depends(get_current_user)
):
    """Query the knowledge base directly."""
    results = rag_service.query(query, n_results)
    
    return {
        "query": query,
        "results": results["documents"][0] if results["documents"] else [],
        "count": len(results["documents"][0]) if results["documents"] else 0
    }
