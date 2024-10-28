import fitz
from models.job_model import pdf_embeddings_collection
from utils.embedding_utils import generate_embedding
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controllers.pdf_controller import process_pdf
from controllers.auth_controller import get_current_user

router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
    result = await process_pdf(file, user.id)
    return {"message": result}