from fastapi import APIRouter
from . import health, documents

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
