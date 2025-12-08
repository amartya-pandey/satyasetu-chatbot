from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.conversation import Conversation, Message
from app.schemas.chat import (
    ChatRequest, ChatResponse, ConversationResponse,
    ConversationCreate, MessageResponse
)
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service
from app.services.translation_service import translation_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message and get AI response.
    Supports bilingual chat (English/Hindi) with RAG.
    """
    user_id = int(current_user["user_id"])
    
    # Detect language if not provided
    if not request.language:
        request.language = translation_service.detect_language(request.message)
    
    # Get or create conversation
    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == user_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            language=request.language,
            title=request.message[:50] + "..." if len(request.message) > 50 else request.message
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message,
        language=request.language
    )
    db.add(user_message)
    db.commit()
    
    # Get relevant context from RAG
    context = rag_service.get_context_for_query(
        request.message,
        university_id=request.university_id
    )
    
    # Prepare messages for LLM
    system_prompt = llm_service.create_system_prompt(context, request.language)
    
    # Get conversation history
    history = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at.desc()).limit(10).all()
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add history in reverse order (oldest first)
    for msg in reversed(history[:-1]):  # Exclude the just-added message
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add current message
    messages.append({"role": "user", "content": request.message})
    
    # Generate response
    response_text = await llm_service.generate_response(messages)
    
    # Save assistant message
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response_text,
        language=request.language
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(
        conversation_id=conversation.id,
        message=request.message,
        response=response_text,
        language=request.language,
        sources=[]  # TODO: Add source documents from RAG
    )


@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user."""
    user_id = int(current_user["user_id"])
    
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(Conversation.updated_at.desc()).all()
    
    return conversations


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific conversation with all messages."""
    user_id = int(current_user["user_id"])
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversation


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a conversation."""
    user_id = int(current_user["user_id"])
    
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    
    return {"message": "Conversation deleted successfully"}
