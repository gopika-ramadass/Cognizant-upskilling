"""
Security Utility Module for Hands-On 9
Implements password hashing with bcrypt, JWT token generation,
and FastAPI OAuth2 authentication dependencies.
"""

import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User

# ---------------------------------------------------------------------------------
# SECURITY NOTICE: Password Hashing Rationale (Task 1 - Step 89)
# Plain-text passwords MUST NEVER be stored or logged at any point.
# bcrypt is preferred over MD5 or SHA-256 because:
# 1. MD5 and SHA-256 are fast hash algorithms designed for maximum throughput, making them
#    highly vulnerable to GPU-accelerated brute-force attacks and rainbow table lookups.
# 2. bcrypt incorporates an adaptive work factor (cost factor) and automatic unique salting.
#    This makes each hash computation computationally expensive, rendering brute-force attacks
#    and pre-computed rainbow tables infeasible for attackers.
# ---------------------------------------------------------------------------------

# JWT Configuration Parameters (Task 2 - Step 91)
SECRET_KEY = "SUPER_SECRET_JWT_KEY_FOR_DIGITAL_NURTURE_DEMO_EXERCISE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 bearer token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


def get_password_hash(password: str) -> str:
    """Hash plain-text password using bcrypt (Task 1 - Step 87)."""
    # Truncate to 72 bytes max as required by bcrypt specification
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain-text password against bcrypt hash (Task 1 - Step 87)."""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(pwd_bytes, hash_bytes)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a signed JWT access token with expiration timestamp (Task 2 - Step 91).
    
    JWT Payload Warning: JWT claims are base64url-encoded strings, NOT ENCRYPTED!
    Never store sensitive credentials (passwords, credit cards, PII) in JWT payloads.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency: Decodes and validates JWT token (Task 2 - Step 92).
    Returns current authenticated User object or raises 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user
