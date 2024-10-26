from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime

class User(Document):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "users"  # MongoDB collection name
