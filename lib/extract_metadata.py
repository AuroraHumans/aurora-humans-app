from PIL import Image
import exifread
from PIL import Image

# Function to convert GPS coordinates
def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    flip = -1 if ref in ['S', 'W'] else 1
    return flip * (degrees + (minutes / 60.0) + (seconds / 3600.0))

# Function to extract metadata
def extract_metadata(image_path):
    # Open image file for reading (binary mode)
    with open(image_path, 'rb') as image_file:
        # Using exifread to get the EXIF metadata
        tags = exifread.process_file(image_file, details=True)

        # Extracting date and time
        date_time = tags.get('EXIF DateTimeOriginal', 'Not Found')
        print(f"Date and Time: {date_time}")

        # Extracting GPS data
        if 'GPS GPSLatitude' in tags:
            lat_dms = tags['GPS GPSLatitude'].values
            lat_ref = tags['GPS GPSLatitudeRef'].values
            lon_dms = tags['GPS GPSLongitude'].values
            lon_ref = tags['GPS GPSLongitudeRef'].values
            
            latitude = get_decimal_from_dms(lat_dms, lat_ref)
            longitude = get_decimal_from_dms(lon_dms, lon_ref)
            print(f"Location: Latitude {latitude}, Longitude {longitude}")
        else:
            print("Location: Not Found")
        return latitude, longitude 
