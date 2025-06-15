from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil
from pathlib import Path
from enum import Enum

from app.services.textract_service import extract_text_from_file
from app.services.s3_service import upload_file_to_s3
from app.services.openai_service import summarize_text

from app.utils import ALLOWED_EXTENSIONS, SummaryLength

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    summary_length: SummaryLength = Query("medium", description="Choose summary length: short, medium, or long")
):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, PNG, JPG, JPEG files are supported")

    with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        text = extract_text_from_file(tmp_path)
        s3_url = upload_file_to_s3(tmp_path, file.filename)

        summary = await summarize_text(text, summary_length)

        return JSONResponse(content={
            "filename": file.filename,
            "extracted_text": text,
            "summary": summary,
            "s3_url": s3_url,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        tmp_path.unlink(missing_ok=True)