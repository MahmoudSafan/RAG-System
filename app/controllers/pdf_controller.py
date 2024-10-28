import fitz
from models.job_model import pdf_embeddings_collection
from utils.embedding_utils import generate_embedding

async def process_pdf(file, user_id: str):
    text_content = ""
    file_content = await file.read()
    with fitz.open(stream=file_content, filetype="pdf") as pdf:
        for page in pdf:
            text_content += page.get_text()
    
    # Generate embeddings for the extracted text
    embeddings = generate_embedding(text_content)
    
    pdf_data = {
        "user_id": user_id,
        "file_name": file.filename,
        "content": text_content,
        "embedding": embeddings
    }

    await pdf_embeddings_collection.insert_one(pdf_data)
    return "PDF uploaded and vectorized successfully"