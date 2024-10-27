from utils.embedding_utils import generate_response, retrieve_similar_content, generate_embedding
from models.job_model import JobData, job_data_collection
from datetime import datetime
from bson import ObjectId

async def get_job_recommendation(query: str, k: int = 5):
    similar_content = await retrieve_similar_content(query, k)
    if not similar_content:
        return "No similar content found."
    response = generate_response(similar_content)
    return response

def estimate_salary(job_title: str, years_experience: int):
    prompt = f"Estimate a salary range for a '{job_title}' with {years_experience} years of experience."
    response = generate_response([prompt])
    return response

async def create_job(job_data: JobData):
    # Generate embedding for job description
    job_data.embedding = generate_embedding(f"{job_data.title} {job_data.description}")
    job_dict = job_data.dict()
    result = await job_data_collection.insert_one(job_dict)
    return str(result.inserted_id)

async def get_job(job_id: str):
    job = await job_data_collection.find_one({"_id": ObjectId(job_id)})
    if job:
        return job
    return None

async def update_job(job_id: str, job_data: JobData):
    update_data = {**job_data.dict(), "updated_at": datetime.utcnow()}
    result = await job_data_collection.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": update_data}
    )
    return result.modified_count > 0

async def delete_job(job_id: str):
    result = await job_data_collection.delete_one({"_id": ObjectId(job_id)})
    return result.deleted_count > 0
