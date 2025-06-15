from fastapi import FastAPI
from app.api import api_router

app = FastAPI(title="FastAPI LLM Agent")

app.include_router(api_router)
