from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta
from ..schemas import UserSignup, UserLogin, User, AuthResponse
from ..database import db
from ..security import hash_password, verify_password, create_access_token, verify_token
from ..config import settings

router = APIRouter()

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = hash_password(user_data.password)
    user_dict = db.create_user(user_data.username, user_data.email, hashed_password)
    user = User(**user_dict)
    
    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return AuthResponse(
        user=user,
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserLogin):
    """Login user"""
    user_data = db.get_user_by_email(credentials.email)
    if not user_data or not verify_password(credentials.password, user_data.get("password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    user = User(**{k: v for k, v in user_data.items() if k != "password"})
    
    # Create token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return AuthResponse(
        user=user,
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/me", response_model=User)
async def get_current_user(user_id: str = Depends(verify_token)):
    """Get current user info"""
    user_dict = db.get_user(user_id)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return User(**user_dict)
