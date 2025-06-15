import boto3
from pathlib import Path

textract = boto3.client("textract", region_name="us-east-1")

def extract_text_from_file(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    file_ext = file_path.suffix.lower()
    if file_ext in [".jpg", ".jpeg", ".png"]:
        response = textract.detect_document_text(Document={'Bytes': file_bytes})
        blocks = response.get("Blocks", [])
        lines = [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
        return "\n".join(lines)

    elif file_ext == ".pdf":
        response = textract.analyze_document(
            Document={'Bytes': file_bytes},
            FeatureTypes=["TABLES", "FORMS"]
        )
        blocks = response.get("Blocks", [])
        lines = [block["Text"] for block in blocks if block["BlockType"] == "LINE"]
        return "\n".join(lines)

    elif file_ext == ".docx":
        from docx import Document
        doc = Document(str(file_path))
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Unsupported file type for Textract")
