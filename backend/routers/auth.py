"""
Authentication router for user registration and login endpoints.

This module handles user registration, login (JWT token generation),
and retrieving current user information.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, User as UserSchema, Token
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def validate_password(password: str) -> bool:
    """
    Validate password strength requirements.
    
    Requirements:
    - At least 8 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Args:
        password: The password to validate
        
    Returns:
        bool: True if password meets requirements, False otherwise
        
    Raises:
        HTTPException: If password doesn't meet requirements
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=422,
            detail="Password must be at least 8 characters long"
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=422,
            detail="Password must contain at least one uppercase letter"
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=422,
            detail="Password must contain at least one lowercase letter"
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=422,
            detail="Password must contain at least one digit"
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=422,
            detail="Password must contain at least one special character"
        )
    return True

def validate_username(username: str) -> bool:
    """
    Validate username requirements.
    
    Requirements:
    - At least 3 characters long
    - Only alphanumeric characters and underscores
    - Must start with a letter
    
    Args:
        username: The username to validate
        
    Returns:
        bool: True if username meets requirements, False otherwise
        
    Raises:
        HTTPException: If username doesn't meet requirements
    """
    if len(username) < 3:
        raise HTTPException(
            status_code=422,
            detail="Username must be at least 3 characters long"
        )
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", username):
        raise HTTPException(
            status_code=422,
            detail="Username must start with a letter and contain only letters, numbers, and underscores"
        )
    return True

@router.post("/register", response_model=UserSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Args:
        user: User registration data (username and password)
        db: Database session
        
    Returns:
        User: The created user object (without password)
        
    Raises:
        HTTPException: If username already exists or validation fails
    """
    logger.info(f"Registration attempt for username: {user.username}")
    
    # Validate username and password
    validate_username(user.username)
    validate_password(user.password)
    
    # Check if username already exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Registration failed: Username '{user.username}' already exists")
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Hash the password and create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"User '{user.username}' registered successfully")
    return db_user

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Args:
        form_data: OAuth2 form with username and password
        db: Database session
        
    Returns:
        Token: JWT access token for authentication
        
    Raises:
        HTTPException: If username or password is incorrect
    """
    logger.info(f"Login attempt for username: {form_data.username}")
    
    # Verify user exists and password is correct
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        logger.warning(f"Login failed: User '{form_data.username}' not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found. Please sign up first."
        )
    if not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Incorrect password for user '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Generate JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User '{form_data.username}' logged in successfully")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: The authenticated user (from JWT token)
        
    Returns:
        User: The current user's information
    """
    return current_user
