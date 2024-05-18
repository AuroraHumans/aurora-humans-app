import pytest
from app.db_operations import insert_metadata, find_metadata

def test_insert_metadata_success(mock_mongo_client):
    """Test successful insertion of metadata."""
    mock_mongo_client.insert_one.return_value = MagicMock(inserted_id="mocked_id")

    metadata = {"key": "value"}
    result = insert_metadata(metadata)

    mock_mongo_client.insert_one.assert_called_once_with(metadata)
    assert result == "mocked_id"

def test_insert_metadata_connection_error(mock_mongo_client):
    """Test handling of connection errors during insertion."""
    mock_mongo_client.insert_one.side_effect = ConnectionRefusedError("connection error")

    result = insert_metadata({"key": "value"})
    assert result is None

def test_find_metadata_success(mock_mongo_client):
    """Test successful retrieval of metadata."""
    mock_cursor = MagicMock()
    mock_mongo_client.find.return_value = mock_cursor

    query = {"key": "value"}
    result = find_metadata(query)

    mock_mongo_client.find.assert_called_once_with(query)
    assert result == mock_cursor

def test_find_metadata_exception(mock_mongo_client):
    """Test handling of exceptions during metadata retrieval."""
    mock_mongo_client.find.side_effect = Exception("generic error")

    result = find_metadata({"key": "value"})
    assert result is None
