from PIL import Image
from PIL.ExifTags import TAGS

def dms_to_decimal(degrees, minutes, seconds, direction):
    """Convert degrees, minutes, seconds to decimal format."""
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def extract_gps_location(gps_info):
    """Extract and convert GPS coordinates to decimal degrees."""
    lat_ref = gps_info.get(1)
    lat = gps_info.get(2)
    lon_ref = gps_info.get(3)
    lon = gps_info.get(4)

    if lat and lon and lat_ref and lon_ref:
        lat_decimal = dms_to_decimal(*lat, lat_ref)
        lon_decimal = dms_to_decimal(*lon, lon_ref)
        return lat_decimal, lon_decimal
    else:
        return None, None

def read_exif_data(image_path):
    exclusions :tuple = ("MakerNote")
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return None

        image_exif_data :dict = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag in exclusions:
                continue
            image_exif_data[tag] = value
        
        return image_exif_data

    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")