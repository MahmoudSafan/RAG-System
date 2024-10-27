from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from models.job_model import job_data_collection, pdf_embeddings_collection
from transformers import AutoModelForCausalLM, AutoTokenizer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str):
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
    model_name = "distilgpt2"  # Lightweight model; adjust based on resources
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    gptmodel = AutoModelForCausalLM.from_pretrained(model_name)
    # Add a padding token if not available
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token


    # Combine prompts into a single string for the model
    prompt_texts = [record.get("description", "") for record in prompts if isinstance(record.get("description"), str)]

    # Tokenize the input and generate output from the model
    inputs =  tokenizer(prompt_texts, return_tensors="pt", padding=True, truncation=True)
    outputs = gptmodel.generate(inputs["input_ids"], max_length=1000, num_return_sequences=1, no_repeat_ngram_size=2)
    # Decode the output to get the response text
    response =  tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
