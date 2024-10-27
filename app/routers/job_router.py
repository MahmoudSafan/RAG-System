from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from controllers.job_controller import get_job_recommendation, estimate_salary, create_job, get_job, update_job, delete_job
from models.job_model import JobData
from controllers.pdf_controller import process_pdf
from controllers.auth_controller import get_current_user
from utils.helper import convert_object_ids
import json

router = APIRouter()

@router.get("/generate-recommendation")
async def generate_recommendation(query: str, k: int = 5, user: dict = Depends(get_current_user)):
    response = await get_job_recommendation(query, k)
    if response == "Error: Invalid input for response generation.":
        raise HTTPException(status_code=500, detail="Failed to generate a response.")
    new_response = convert_object_ids(response)
    print(new_response)
    return new_response

@router.get("/estimate-salary")
async def estimate_salary_endpoint(job_title: str, years_experience: int, user: dict = Depends(get_current_user)):
    response = estimate_salary(job_title, years_experience)
    return {"estimated_salary": response}

@router.post("/upload-pdf")
async def upload_pdf_file(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
    result = process_pdf(file, user["sub"])
    return {"message": result}

@router.post("/jobs", response_model=object)
async def create_job_route(job_data: JobData, user=Depends(get_current_user)):
    job_id = await create_job(job_data)
    return {"message": "Job created successfully", "id": job_id}

@router.get("/jobs/{job_id}", response_model=JobData)
async def get_job_route(job_id: str, user=Depends(get_current_user)):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/jobs/{job_id}", response_model=bool)
async def update_job_route(job_id: str, job_data: JobData, user=Depends(get_current_user)):
    success = await update_job(job_id, job_data)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or not updated")
    return success

@router.delete("/jobs/{job_id}", response_model=bool)
async def delete_job_route(job_id: str, user=Depends(get_current_user)):
    success = await delete_job(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found or not deleted")
    return success