from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.db import init_db
from routers import auth_router, job_router, chat_router, pdf_router

import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await init_db()  # Initialize Beanie and MongoDB connection

# Register routers
app.include_router(auth_router.router)
app.include_router(job_router.router)
app.include_router(chat_router.router)
app.include_router(pdf_router.router)

# Serve static files
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
