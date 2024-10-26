import fitz
from models.job_model import pdf_embeddings_collection
from utils.embedding_utils import generate_embedding

def process_pdf(file, user_id: str):
    text_content = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text_content += page.get_text()
    
    embeddings = generate_embedding(text_content)
    pdf_data = {"user_id": user_id, "file_name": file.filename, "content": text_content, "embedding": embeddings}
    pdf_embeddings_collection.insert_one(pdf_data)
    return "PDF uploaded and vectorized successfully"
