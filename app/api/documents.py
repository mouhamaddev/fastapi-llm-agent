import hashlib
from app.services.redis_service import redis_client
import json
from fastapi import Request

from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
from pathlib import Path

from app.utils.limiter import limiter

from app.services.textract_service import extract_text_from_file
from app.services.s3_service import upload_file_to_s3
from app.services.openai_service import summarize_text

from app.common import ALLOWED_EXTENSIONS, SummaryLength

router = APIRouter()

@router.post("/upload")
@router.post("/upload/")
@limiter.limit("5/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    summary_length: SummaryLength = Query("medium", description="Choose summary length: short, medium, or long")
):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, PNG, JPG, JPEG files are supported")

    file_bytes = await file.read()

    hash_input = file_bytes + summary_length.value.encode()
    doc_hash = hashlib.sha256(hash_input).hexdigest()

    redis_key = f"summary:{doc_hash}"

    cached_data = await redis_client.get(redis_key)
    if cached_data:
        return JSONResponse(content=json.loads(cached_data))

    ext = Path(file.filename).suffix.lower()
    with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(file_bytes)
        tmp_path = Path(tmp.name)

    try:
        text = extract_text_from_file(tmp_path)
        s3_url = upload_file_to_s3(tmp_path, file.filename)
        summary = await summarize_text(text, summary_length)

        result = {
            "filename": file.filename,
            "extracted_text": text,
            "summary": summary,
            "s3_url": s3_url,
        }

        await redis_client.set(redis_key, json.dumps(result), ex=604800)

        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        tmp_path.unlink(missing_ok=True)