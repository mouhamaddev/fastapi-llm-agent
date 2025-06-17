from pathlib import Path
from unittest.mock import patch, mock_open
from app.services.s3_service import upload_file_to_s3

@patch("builtins.open", new_callable=mock_open, read_data=b"dummy content")
@patch("app.services.s3_service.s3_client.upload_file")
def test_upload_file_to_s3(mock_upload, mock_open_file):
    path = Path("test.pdf")
    filename = "original.pdf"
    url = upload_file_to_s3(path, filename)

    assert url.startswith("s3://document-uploads-bucket-")
    assert path.name in url
    mock_upload.assert_called_once()
