import io
import json
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from unittest.mock import AsyncMock, patch

from app.common import SummaryLength

ALLOWED_TYPES = [".pdf", ".docx", ".jpg", ".jpeg", ".png"]

@pytest.mark.asyncio
@pytest.mark.parametrize("ext", ALLOWED_TYPES)
async def test_upload_document_success(ext):
    fake_file_content = b"hello world"
    fake_filename = f"test{ext}"
    fake_summary = "This is a summary."
    fake_s3_url = "s3://bucket/uploads/summary.pdf"
    fake_extracted = "This is extracted text."

    with (
        patch("app.services.redis_service.redis_client.get", new_callable=AsyncMock, return_value=None),
        patch("app.services.redis_service.redis_client.set", new_callable=AsyncMock),
        patch("app.services.textract_service.extract_text_from_file", return_value=fake_extracted),
        patch("app.services.s3_service.upload_file_to_s3", return_value=fake_s3_url),
        patch("app.services.openai_service.summarize_text", new_callable=AsyncMock, return_value=fake_summary)
    ):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resp = await ac.post(
                "/upload",
                files={"file": (fake_filename, io.BytesIO(fake_file_content), "application/octet-stream")},
                params={"summary_length": "short"},
            )

    assert resp.status_code == 200
    data = resp.json()
    assert data["filename"] == fake_filename
    assert data["summary"] == fake_summary
    assert data["extracted_text"] == fake_extracted
    assert data["s3_url"] == fake_s3_url

@pytest.mark.asyncio
@pytest.mark.parametrize("ext", [".exe", ".txt", ".csv"])
async def test_upload_document_invalid_extension(ext):
    fake_file_content = b"dummy"
    filename = f"file{ext}"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/upload",
            files={"file": (filename, io.BytesIO(fake_file_content), "application/octet-stream")}
        )
    assert resp.status_code == 400
    assert "Only PDF" in resp.json()["detail"]

@pytest.mark.asyncio
async def test_upload_document_cached_summary():
    cached_result = {
        "filename": "doc.pdf",
        "summary": "Cached summary",
        "extracted_text": "Cached extracted",
        "s3_url": "s3://bucket/...",
    }

    with patch("app.services.redis_service.redis_client.get", new_callable=AsyncMock, return_value=json.dumps(cached_result)):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            resp = await ac.post(
                "/upload",
                files={"file": ("doc.pdf", io.BytesIO(b"data"), "application/pdf")},
                params={"summary_length": "medium"}
            )
    assert resp.status_code == 200
    assert resp.json() == cached_result

@pytest.mark.asyncio
async def test_upload_document_internal_failure():
    with patch("app.services.textract_service.extract_text_from_file", side_effect=Exception("Textract fail")):
        with patch("app.services.redis_service.redis_client.get", new_callable=AsyncMock, return_value=None):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                resp = await ac.post(
                    "/upload",
                    files={"file": ("doc.pdf", io.BytesIO(b"abc"), "application/pdf")}
                )
    assert resp.status_code == 500
    assert "Processing failed" in resp.json()["detail"]
