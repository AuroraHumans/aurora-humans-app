import pytest
from app.file_upload import upload_blob
from datetime import datetime

def test_upload_blob_success(mock_storage_client, mock_get_secret, mock_env, tmp_path):
    """Test upload_blob function success scenario."""
    # Setup
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("content")
    
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    
    # Test
    upload_blob("destination_blob_name", str(p))
    
    # Verify
    mock_get_secret.assert_called_once_with(project_id="test_value", secret="test_value")
    mock_storage_client.assert_called_once_with(project="test_value", credentials="test_value")
    mock_bucket.blob.assert_called_once_with("destination_blob_name")
    mock_blob.upload_from_filename.assert_called_once_with(
        f"{str(p)}_{datetime.now().isoformat()}.png", if_generation_match=0
    )

def test_upload_blob_fail_file_not_found(mock_storage_client, mock_get_secret, mock_env):
    """Test upload_blob fails if file does not exist."""
    with pytest.raises(FileNotFoundError):
        upload_blob("destination_blob_name", "nonexistentfile.txt")
