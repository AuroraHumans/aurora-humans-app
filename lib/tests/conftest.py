import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_mongo_client():
    with patch('app.db_operations.MongoClient') as MockClient:
        mock_client = MockClient.return_value
        mock_db = mock_client.__getitem__.return_value
        mock_collection = mock_db.__getitem__.return_value
        yield mock_collection

@pytest.fixture
def mock_storage_client(mocker):
    """Fixture to mock storage.Client and its methods."""
    with patch('app.file_upload.storage.Client') as MockClient:
        yield MockClient

@pytest.fixture
def mock_get_secret(mocker):
    """Fixture to mock secrets_manager_client.get_secret function."""
    with patch('app.file_upload.get_secret') as MockGetSecret:
        yield MockGetSecret

@pytest.fixture
def mock_env(mocker):
    """Fixture to mock os.getenv to return consistent values for testing."""
    mocker.patch('os.getenv', return_value="test_value")