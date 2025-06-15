from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import shutil
from pathlib import Path
from app.services.textract_service import extract_text_from_file

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, PNG, JPG, JPEG files are supported")

    with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        text = extract_text_from_file(tmp_path)
        return JSONResponse(content={"filename": file.filename, "extracted_text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
    finally:
        tmp_path.unlink(missing_ok=True)