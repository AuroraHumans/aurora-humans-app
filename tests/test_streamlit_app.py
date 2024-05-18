import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
import io

# Assume the module is named streamlit_app.py and contains the Streamlit script
from app import uploaded_file

@pytest.fixture
def mock_streamlit():
    with patch('streamlit_app.st') as mock:
        yield mock

@pytest.fixture
def mock_image_open():
    with patch('streamlit_app.Image.open') as mock:
        mock.return_value = Image.new('RGB', (100, 100))
        yield mock

@pytest.fixture
def mock_extract_metadata():
    with patch('streamlit_app.extract_metadata') as mock:
        mock.return_value = (51.5074, -0.1278)  # Example lat, long for London
        yield mock

@pytest.fixture
def mock_upload_blob():
    with patch('streamlit_app.upload_blob') as mock:
        yield mock

@pytest.fixture
def mock_insert_metadata():
    with patch('streamlit_app.insert_metadata') as mock:
        yield mock

def test_uploaded_file(mock_streamlit):
    file = MagicMock()
    result = uploaded_file(file)
    assert result == file

def test_integration_flow(mock_streamlit, mock_image_open, mock_extract_metadata, mock_upload_blob, mock_insert_metadata):
    # Setup
    mock_streamlit.file_uploader.return_value = "fake_path.jpg"
    mock_streamlit.text_input.return_value = "Test Title"
    mock_streamlit.date_input.return_value = "2021-01-01"
    mock_streamlit.checkbox.return_value = True
    mock_streamlit.text_area.return_value = "Test Description"

    # Simulate button click
    mock_streamlit.button.return_value = True

    # Run function - Normally, you would call a function that encapsulates the logic
    # For this example, the main logic would be triggered here (not directly callable without refactoring)

    # Assertions to confirm behaviors
    mock_image_open.assert_called_once_with("fake_path.jpg")
    mock_extract_metadata.assert_called_once()
    mock_upload_blob.assert_called()
    mock_insert_metadata.assert_called()

    # Ensure Streamlit displays success
    mock_streamlit.success.assert_called_with("Image and metadata successfully uploaded to Google Cloud")
