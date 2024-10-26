from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from controllers.auth_controller import register_user, authenticate_user
from utils.token_utils import create_access_token

router = APIRouter()

# Request and Response Models
class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/auth/register", status_code=201)
async def register(request: RegisterRequest):
    user = await register_user(request.email, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    return {"message": "User registered successfully"}

@router.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    user = await authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Generate JWT token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
