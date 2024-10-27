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
    # Generate the query embedding
    query_embedding = np.array(generate_embedding(query)).astype('float32').reshape(1, -1)

    # Retrieve all job and PDF records
    job_records = await job_data_collection.find().to_list(None)
    pdf_records = await pdf_embeddings_collection.find().to_list(None)

    # Collect embeddings, ensuring all are the same shape
    embeddings = []
    valid_records = []  # To store only records with valid embeddings

    for record in job_records + pdf_records:
        embedding = record.get("embedding")
        # Ensure embedding exists and is a list or array of floats
        if isinstance(embedding, list) and len(embedding) > 0:
            embeddings.append(np.array(embedding, dtype='float32'))
            valid_records.append(record)

    # Convert embeddings list to a numpy array
    if not embeddings:
        return []  # Return empty if no valid embeddings
    all_embeddings = np.vstack(embeddings)  # Stack to ensure consistency

    # Perform Faiss similarity search
    dimension = all_embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(all_embeddings)
    distances, indices = faiss_index.search(query_embedding, k)
    
    # Retrieve records based on indices
    similar_records = [valid_records[i] for i in indices[0]]
    
    return similar_records

def generate_response(prompts):
   # Load the model and tokenizer
    model_name = "gpt2"  # Or use "distilgpt2" if resources are limited
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    # Set pad_token if it doesn't exist
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    if not isinstance(prompts, list) or not prompts:
        return "Error: No valid input provided for response generation."

    # Combine prompts into a single string for the model input
    prompt_text = "\n".join(prompts)
    
    # Tokenize the input with padding, truncation, and attention mask
    inputs = tokenizer(prompt_text, return_tensors="pt", padding=True, truncation=True)
    inputs["attention_mask"] = (inputs["input_ids"] != tokenizer.pad_token_id).long()

    # Generate output with `pad_token_id` to avoid padding issues
    outputs = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=30,  # Limit the number of generated tokens
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.pad_token_id
    )
    
    # Decode and return the generated response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
