# models/chat_model.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from utils.db import db

class Message(BaseModel):
    sender: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Chat(BaseModel):
    user_id: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Define MongoDB collection
chat_collection = db["chats"]
