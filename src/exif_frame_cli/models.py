"""Data models for EXIF information."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ExifData:
    """Container for EXIF metadata extracted from an image."""
    
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    lens_model: Optional[str] = None
    focal_length: Optional[str] = None
    aperture: Optional[str] = None
    shutter_speed: Optional[str] = None
    iso: Optional[str] = None
    datetime_original: Optional[str] = None
    
    @property
    def camera_full_name(self) -> str:
        """Get the full camera name combining make and model."""
        if self.camera_make and self.camera_model:
            return f"{self.camera_make} {self.camera_model}"
        elif self.camera_model:
            return self.camera_model
        elif self.camera_make:
            return self.camera_make
        return "Unknown Camera"
    
    @property
    def lens_display_name(self) -> str:
        """Get the lens name for display."""
        return self.lens_model or "Unknown Lens"
    
    def format_settings(self) -> str:
        """Format technical settings as a single line."""
        settings = []
        
        if self.focal_length:
            settings.append(self.focal_length)
        if self.aperture:
            settings.append(f"f/{self.aperture}")
        if self.shutter_speed:
            settings.append(f"{self.shutter_speed}s")
        if self.iso:
            settings.append(f"ISO{self.iso}")
            
        return " ".join(settings) if settings else "Settings Unknown"
    
    def format_datetime(self) -> str:
        """Format datetime for display."""
        if not self.datetime_original:
            return ""
        
        try:
            # Parse the EXIF datetime format: "YYYY:MM:DD HH:MM:SS"
            from datetime import datetime
            dt = datetime.strptime(self.datetime_original, "%Y:%m:%d %H:%M:%S")
            # Format like the sample: "20:13:02 2024.12.09"
            return dt.strftime("%H:%M:%S %Y.%m.%d")
        except:
            return self.datetime_original