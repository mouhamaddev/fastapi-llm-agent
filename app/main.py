from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

app = FastAPI(title="FastAPI LLM Agent")

app.include_router(api_router)

origins = [
    "http://localhost:3000",
    "http://next-client-88389272.s3-website-us-east-1.amazonaws.com",
    "https://d31yw2qefd409z.cloudfront.net",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
