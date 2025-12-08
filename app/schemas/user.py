from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: Union[int, str]  # Support both SQLite (int) and MongoDB (str)
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserMongoResponse(UserBase):
    """MongoDB-specific user response with string ID."""
    id: str = Field(..., alias="_id")
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
