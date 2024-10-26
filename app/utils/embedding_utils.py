from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from models.job_model import job_data_collection, pdf_embeddings_collection
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer from Hugging Face Transformers
model_name = "distilgpt2"  # Lightweight model; adjust based on resources
tokenizer = AutoTokenizer.from_pretrained(model_name)
gptmodel = AutoModelForCausalLM.from_pretrained(model_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str):
    return model.encode(text).tolist()

def retrieve_similar_content(query: str, k: int = 5):
    query_embedding = np.array(generate_embedding(query)).astype('float32').reshape(1, -1)
    job_records = list(job_data_collection.find())
    pdf_records = list(pdf_embeddings_collection.find())
    all_embeddings = np.array([record['embedding'] for record in job_records + pdf_records]).astype('float32')
    faiss_index = faiss.IndexFlatL2(all_embeddings.shape[1])
    faiss_index.add(all_embeddings)
    distances, indices = faiss_index.search(query_embedding, k)
    return [job_records + pdf_records]
    #return [job_records + pdf_records][i] for i in indices[0]

def generate_response(prompts):
    """
    Generates a response based on the provided prompts using a language model.
    Args:
        prompts (list): A list of strings representing input prompts for the model.
    Returns:
        str: The generated response.
    """
    # Combine prompts into a single string for the model
    prompt_text = "\n".join(prompts)

    # Tokenize the input and generate output from the model
    inputs = tokenizer(prompt_text, return_tensors="pt")
    outputs = gptmodel.generate(inputs["input_ids"], max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)

    # Decode the output to get the response text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response
