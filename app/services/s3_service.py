import boto3
import hashlib
from datetime import datetime
from pathlib import Path

s3_client = boto3.client("s3", region_name="us-east-1")
BUCKET_NAME = "document-uploads-bucket-88389272"

def upload_file_to_s3(file_path: Path, original_filename: str) -> str:
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()[:8]

    today = datetime.utcnow()
    folder_path = f"uploads/{today.year}/{today.month:02d}/{today.day:02d}"
    s3_key = f"{folder_path}/{file_hash}_{original_filename}"

    s3_client.upload_file(str(file_path), BUCKET_NAME, s3_key)

    s3_url = f"s3://{BUCKET_NAME}/{s3_key}"
    return s3_url
