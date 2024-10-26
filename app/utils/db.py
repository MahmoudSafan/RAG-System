# db.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from dotenv import load_dotenv
import os
from models.user_model import User  # Import User for initialization
# Load environment variables from .env
load_dotenv()

# MongoDB connection string
MONGODB_URI = os.getenv("MONGODB_URI")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client["rag_system"]

# Initialize Beanie with models
async def init_db():
    await init_beanie(database=db, document_models=[User])
