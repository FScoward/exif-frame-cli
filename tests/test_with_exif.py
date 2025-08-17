#!/usr/bin/env python3
"""Test script to create an image with sample EXIF data and frame it."""

from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
import piexif

# Create a test image
img = Image.new('RGB', (1200, 800), color='darkgreen')
draw = ImageDraw.Draw(img)

# Add some visual content
draw.rectangle([50, 50, 1150, 750], fill='forestgreen', outline='lightgreen', width=5)
draw.ellipse([400, 250, 800, 550], fill='green', outline='darkgreen', width=3)
draw.text((600, 400), 'Sample Photo', fill='white', anchor='mm')

# Create EXIF data similar to your example
exif_dict = {
    "0th": {
        piexif.ImageIFD.Make: "SONY",
        piexif.ImageIFD.Model: "ILCE-7CM2",
        piexif.ImageIFD.Software: "exif-frame-cli",
    },
    "Exif": {
        piexif.ExifIFD.LensModel: "24-70mm F2.8 DG DN II | Art 024",
        piexif.ExifIFD.FocalLength: (70, 1),  # 70mm
        piexif.ExifIFD.FNumber: (56, 10),     # f/5.6
        piexif.ExifIFD.ExposureTime: (1, 125), # 1/125s
        piexif.ExifIFD.ISOSpeedRatings: 200,   # ISO 200
    },
    "GPS": {},
    "1st": {},
    "thumbnail": None,
}

# Convert to bytes
exif_bytes = piexif.dump(exif_dict)

# Save image with EXIF data
img.save('sample_with_exif.jpg', 'JPEG', exif=exif_bytes)
print("Created sample_with_exif.jpg with EXIF data")
print("Now run: poetry run exif-frame-cli sample_with_exif.jpg --verbose")