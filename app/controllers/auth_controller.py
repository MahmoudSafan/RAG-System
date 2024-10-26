from passlib.context import CryptContext
from models.user_model import User
from utils.token_utils import create_access_token
from pydantic import EmailStr
from datetime import datetime

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def register_user(email: EmailStr, password: str):
    # Check if the user already exists
    existing_user = await User.find_one(User.email == email)
    if existing_user:
        return None  # Return None if user already exists

    # Hash password and create a new user
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    await new_user.insert()
    return new_user

async def authenticate_user(email: EmailStr, password: str):
    user = await User.find_one(User.email == email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.token_utils import decode_access_token
from models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await User.find_one(User.email == payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
