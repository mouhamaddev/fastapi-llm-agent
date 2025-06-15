from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_document():
    return {"message": "Document received"}

@router.get("/summary")
async def get_summary():
    return {"summary": "This is a placeholder summary"}
