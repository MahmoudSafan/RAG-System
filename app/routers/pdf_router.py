import fitz
from models.job_model import pdf_embeddings_collection
from utils.embedding_utils import generate_embedding
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controllers.pdf_controller import process_pdf
from controllers.auth_controller import get_current_user


def process_pdf(file, user_id: str):
    text_content = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text_content += page.get_text()
    
    embeddings = generate_embedding(text_content)
    pdf_data = {"user_id": user_id, "file_name": file.filename, "content": text_content, "embedding": embeddings}
    pdf_embeddings_collection.insert_one(pdf_data)
    return "PDF uploaded and vectorized successfully"



router = APIRouter()

@router.post("/upload-pdf")
async def upload_pdf_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
    result = process_pdf(file, user["sub"])
    return {"message": result}