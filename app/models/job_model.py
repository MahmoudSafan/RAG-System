# models/job_model.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from utils.db import db

class JobData(BaseModel):
    title: str
    description: str
    requirements: List[str]
    embedding: List[float] = []

class PDFEmbedding(BaseModel):
    user_id: str
    file_name: str
    content: str
    embedding: List[float]
  
# # Define MongoDB collections
job_data_collection = db["jobs"]
pdf_embeddings_collection = db["pdf_embeddings"]
