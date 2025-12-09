from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.models.mongo_models import User, Conversation
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from beanie import PydanticObjectId
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/auth/mongo", tags=["MongoDB Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user in MongoDB."""
    try:
        # Check if user already exists
        existing_user = await User.find_one(
            {"$or": [{"email": user_data.email}, {"username": user_data.username}]}
        )
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
    except HTTPException:
        raise
    except Exception as e:
        # If there's old/corrupted data, ignore and proceed
        pass
    
    # Create new user
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password)
    )
    
    await user.insert()
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user and return JWT token."""
    # Find user
    user = await User.find_one({"email": credentials.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check password - MongoDB stores in 'password' field with bcrypt hash
    password_valid = False
    if user.password:
        # Check if it's a hashed password (starts with $2a$ or $2b$)
        if user.password.startswith('$2a$') or user.password.startswith('$2b$'):
            password_valid = verify_password(credentials.password, user.password)
        else:
            # Plain text password
            password_valid = (credentials.password == user.password)
    elif user.hashed_password:
        # New user with hashed_password field
        password_valid = verify_password(credentials.password, user.hashed_password)
    
    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user_mongo(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from MongoDB."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    user_id: str = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await User.get(PydanticObjectId(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user_mongo)):
    """Get current user information."""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user_mongo)):
    """Get detailed user profile with preferences and conversation stats."""
    # Get user's conversation count
    conversation_count = await Conversation.find({"user_id": str(current_user.id)}).count()
    
    return {
        "user": {
            "id": str(current_user.id),
            "name": current_user.full_name,
            "email": current_user.email,
            "username": current_user.username,
            "created_at": current_user.created_at,
            "preferences": current_user.preferences or {},
            "profile_data": current_user.profile_data or {}
        },
        "stats": {
            "total_conversations": conversation_count,
            "account_age_days": (datetime.utcnow() - current_user.created_at).days
        }
    }


@router.put("/profile")
async def update_user_profile(
    preferences: dict,
    current_user: User = Depends(get_current_user_mongo)
):
    """Update user preferences for personalization."""
    current_user.preferences = preferences
    await current_user.save()
    
    return {
        "message": "Profile updated successfully",
        "preferences": current_user.preferences
    }
