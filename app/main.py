from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from fastapi.responses import JSONResponse

from app.utils.limiter import limiter

from app.api import api_router

app = FastAPI(title="FastAPI LLM Agent")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.include_router(api_router)

origins = [
    "http://localhost:3000",
    "http://next-client-88389272.s3-website-us-east-1.amazonaws.com",
    "http://d31yw2qefd409z.cloudfront.net",
    "https://d31yw2qefd409z.cloudfront.net",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
