from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    language: Optional[str] = "en"


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    language: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    title: Optional[str] = "New Conversation"
    language: Optional[str] = "en"


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    language: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = 0  # Default to 0 for new conversations or anonymous users
    language: Optional[str] = "en"
    university_id: Optional[int] = 0


class ChatResponse(BaseModel):
    conversation_id: str  # Changed to str for MongoDB ObjectId support
    message: str
    language: str
    sources: List[str] = []
