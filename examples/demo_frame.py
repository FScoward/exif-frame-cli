#!/usr/bin/env python3
"""Demo script to show frame generation with sample EXIF data."""

from PIL import Image, ImageDraw
from src.exif_frame_cli.models import ExifData
from src.exif_frame_cli.frame_generator import FrameGenerator

# Create a demo image
img = Image.new('RGB', (1200, 800), color=(34, 139, 34))  # Forest green
draw = ImageDraw.Draw(img)

# Add some visual content
draw.rectangle([50, 50, 1150, 750], fill=(46, 125, 50), outline=(144, 238, 144), width=5)
draw.ellipse([400, 250, 800, 550], fill=(0, 100, 0), outline=(0, 50, 0), width=3)

# Try to add text (may fail if no font available, but that's ok)
try:
    draw.text((600, 400), 'Sample Photo', fill='white', anchor='mm')
except:
    draw.text((500, 400), 'Sample Photo', fill='white')

# Save the base image
img.save('demo_photo.jpg', 'JPEG')

# Create sample EXIF data matching your example
sample_exif = ExifData(
    camera_make="SONY",
    camera_model="ILCE-7CM2",
    lens_model="24-70mm F2.8 DG DN II | Art 024",
    focal_length="70mm",
    aperture="5.6",
    shutter_speed="1/125",
    iso="200"
)

# Generate the frame
frame_gen = FrameGenerator(style="classic")
output_path = frame_gen.generate_frame('demo_photo.jpg', sample_exif, 'demo_framed.jpg')

print(f"Demo frame generated: {output_path}")
print("Camera/Lens line:", f"{sample_exif.camera_full_name} / {sample_exif.lens_model}")
print("Settings line:", sample_exif.format_settings())