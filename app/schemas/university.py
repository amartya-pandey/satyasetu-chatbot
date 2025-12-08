from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime


class UniversityBase(BaseModel):
    name: str
    code: str
    location: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"


class UniversityCreate(UniversityBase):
    verification_url: Optional[str] = None
    verification_method: Optional[Dict] = None
    common_forgery_patterns: Optional[List[str]] = None


class UniversityResponse(UniversityBase):
    id: int
    verification_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentTemplateCreate(BaseModel):
    university_id: int
    document_type: str
    template_features: Optional[Dict] = None
    security_features: Optional[Dict] = None


class DocumentTemplateResponse(BaseModel):
    id: int
    university_id: int
    document_type: str
    template_features: Optional[Dict] = None
    security_features: Optional[Dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
