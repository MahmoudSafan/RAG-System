from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from models.job_model import job_data_collection, pdf_embeddings_collection
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

# Suppress parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def generate_embedding(text: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model.encode(text).tolist()

async def retrieve_similar_content(query: str, k: int = 5):
    query_embedding = np.array(generate_embedding(query)).astype('float32').reshape(1, -1)

    job_records = await job_data_collection.find().to_list(None)
    pdf_records = await pdf_embeddings_collection.find().to_list(None)

    # Collect embeddings, ensuring all are the same shape
    embeddings = []
    valid_records = [] 

    for record in job_records + pdf_records:
        embedding = record.get("embedding")
        if isinstance(embedding, list) and len(embedding) > 0:
            embeddings.append(np.array(embedding, dtype='float32'))
            valid_records.append(record)

    if not embeddings:
        return []  
    
    all_embeddings = np.vstack(embeddings) 

    # Perform Faiss similarity search
    dimension = all_embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(all_embeddings)
    distances, indices = faiss_index.search(query_embedding, k)
    
    # Retrieve records based on indices
    similar_records = [valid_records[i] for i in indices[0]]
    return similar_records

def generate_response(prompts):
    model_name = "gpt2" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    if not isinstance(prompts, list) or not prompts:
        return "Error: No valid input provided for response generation."

    prompt_text = "\n".join(prompts)
    
    inputs = tokenizer(prompt_text, return_tensors="pt", padding=True, truncation=True)
    inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=30, 
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.pad_token_id
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
