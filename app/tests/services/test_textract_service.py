import pytest
from unittest.mock import patch
from app.services.textract_service import extract_text_from_file
from pathlib import Path

@pytest.mark.parametrize("ext", [".jpg", ".jpeg", ".png", ".pdf"])
@patch("builtins.open", new_callable=patch("builtins.open", create=True))
def test_extract_text_from_supported_images(mock_open):
    mock_open.return_value.__enter__.return_value.read.return_value = b"fake"

    dummy_path = Path(f"dummy.jpg")
    with patch("app.services.textract_service.textract.detect_document_text", return_value={
        "Blocks": [{"BlockType": "LINE", "Text": "Line 1"}, {"BlockType": "LINE", "Text": "Line 2"}]
    }):
        result = extract_text_from_file(dummy_path)
        assert "Line 1" in result
        assert "Line 2" in result

@pytest.mark.parametrize("ext", [".docx"])
def test_extract_text_from_docx(monkeypatch):
    class FakeParagraph:
        def __init__(self, text):
            self.text = text
    class FakeDoc:
        paragraphs = [FakeParagraph("A"), FakeParagraph("B")]

    monkeypatch.setattr("app.services.textract_service.Document", lambda path: FakeDoc())
    result = extract_text_from_file(Path("sample.docx"))
    assert "A" in result
    assert "B" in result

def test_extract_text_from_unsupported_format():
    with pytest.raises(ValueError):
        extract_text_from_file(Path("unsupported.xls"))
