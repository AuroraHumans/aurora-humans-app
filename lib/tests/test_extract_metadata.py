from unittest.mock import mock_open, patch
import exifread

@pytest.fixture
def mock_exif_tags():
    return {
        'EXIF DateTimeOriginal': '2021:04:01 12:34:56',
        'GPS GPSLatitude': exifread.classes.IfdTag(mock_name="GPS GPSLatitude", field_type=5, values=[50, 30, 30], field_offset=1, field_length=1),
        'GPS GPSLatitudeRef': exifread.classes.IfdTag(mock_name="GPS GPSLatitudeRef", field_type=2, values='N', field_offset=1, field_length=1),
        'GPS GPSLongitude': exifread.classes.IfdTag(mock_name="GPS GPSLongitude", field_type=5, values=[4, 30, 30], field_offset=1, field_length=1),
        'GPS GPSLongitudeRef': exifread.classes.IfdTag(mock_name="GPS GPSLongitudeRef", field_type=2, values='E', field_offset=1, field_length=1)
    }

def test_extract_metadata_with_gps(mock_exif_tags):
    with patch('builtins.open', mock_open(read_data="dummy data")) as mock_file:
        with patch('exifread.process_file', return_value=mock_exif_tags):
            latitude, longitude = extract_metadata("fake_path.jpg")
            assert latitude == pytest.approx(50.508333)
            assert longitude == pytest.approx(4.508333)

def test_extract_metadata_without_gps():
    tags_without_gps = {'EXIF DateTimeOriginal': '2021:04:01 12:34:56'}
    with patch('builtins.open', mock_open(read_data="dummy data")):
        with patch('exifread.process_file', return_value=tags_without_gps):
            with pytest.raises(KeyError):  # As GPS keys will not be found
                extract_metadata("fake_path.jpg")
