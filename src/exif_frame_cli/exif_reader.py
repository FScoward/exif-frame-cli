"""EXIF data extraction from images."""

from typing import Optional
from fractions import Fraction

from PIL import Image
from PIL.ExifTags import TAGS

from .models import ExifData


class ExifReader:
    """Extract EXIF metadata from image files."""
    
    def __init__(self, image_path: str):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.exif_dict = self._get_exif_dict()
    
    def _get_exif_dict(self) -> dict:
        """Extract EXIF data as a dictionary."""
        exif_data = {}
        if hasattr(self.image, '_getexif') and self.image._getexif() is not None:
            exif = self.image._getexif()
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_data[tag] = value
        return exif_data
    
    def _format_shutter_speed(self, shutter_speed) -> Optional[str]:
        """Format shutter speed from EXIF data."""
        if shutter_speed is None:
            return None
        
        # Convert to float for calculation (handles IFDRational and other numeric types)
        try:
            speed_value = float(shutter_speed)
        except (ValueError, TypeError):
            return str(shutter_speed)
        
        # Handle speed values
        if speed_value >= 1:
            # For 1 second or longer exposures
            if speed_value == int(speed_value):
                return f"{int(speed_value)}s"
            else:
                return f"{speed_value:.1f}s"
        else:
            # For fractions less than 1 second, show as 1/x format
            reciprocal = 1 / speed_value
            return f"1/{int(round(reciprocal))}"
    
    def _format_aperture(self, aperture) -> Optional[str]:
        """Format aperture from EXIF data."""
        if aperture is None:
            return None
        
        if isinstance(aperture, tuple):
            if len(aperture) == 2:
                numerator, denominator = aperture
                if denominator != 0:
                    return f"{numerator / denominator:.1f}"
        
        return str(aperture)
    
    def _format_focal_length(self, focal_length) -> Optional[str]:
        """Format focal length from EXIF data."""
        if focal_length is None:
            return None
        
        if isinstance(focal_length, tuple):
            if len(focal_length) == 2:
                numerator, denominator = focal_length
                if denominator != 0:
                    return f"{int(numerator / denominator)}mm"
        
        if isinstance(focal_length, (int, float)):
            return f"{int(focal_length)}mm"
        
        # For any other type, try to convert to float and add mm unit
        try:
            value = float(focal_length)
            return f"{int(value)}mm"
        except (ValueError, TypeError):
            return f"{focal_length}mm"
    
    def extract_exif_data(self) -> ExifData:
        """Extract and format EXIF data into ExifData object."""
        return ExifData(
            camera_make=self.exif_dict.get('Make'),
            camera_model=self.exif_dict.get('Model'),
            lens_model=self.exif_dict.get('LensModel'),
            focal_length=self._format_focal_length(self.exif_dict.get('FocalLength')),
            aperture=self._format_aperture(self.exif_dict.get('FNumber')),
            shutter_speed=self._format_shutter_speed(self.exif_dict.get('ExposureTime')),
            iso=str(self.exif_dict.get('ISOSpeedRatings', '')) if self.exif_dict.get('ISOSpeedRatings') else None
        )