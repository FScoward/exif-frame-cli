"""Frame generation for instant camera-style photos."""

from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from .models import ExifData


class FrameGenerator:
    """Generate instant camera-style frames with EXIF metadata."""
    
    def __init__(self, style: str = "classic"):
        self.style = style
        self.frame_color = (255, 255, 255)  # White frame
        self.text_color = (50, 50, 50)      # Dark gray text
        
    def _calculate_frame_dimensions(self, image_size: Tuple[int, int]) -> dict:
        """Calculate frame dimensions based on image size."""
        width, height = image_size
        
        # Frame margins - more like instant camera proportions
        side_margin = int(width * 0.05)   # 5% of width for sides
        top_margin = int(height * 0.05)   # 5% of height for top
        bottom_margin = int(height * 0.25) # 25% of height for metadata area
        
        new_width = width + (side_margin * 2)
        new_height = height + top_margin + bottom_margin
        
        return {
            'new_size': (new_width, new_height),
            'image_position': (side_margin, top_margin),
            'text_area_start': height + top_margin,
            'text_area_height': bottom_margin,
            'side_margin': side_margin
        }
    
    def _get_font_size(self, text: str, max_width: int, max_height: int) -> int:
        """Calculate appropriate font size for given text and area."""
        # Much larger base font size based on available space
        base_size = max_height // 2  # Use 1/2 of available height (larger than before)
        
        # Calculate based on text length and available width - much more generous
        width_based_size = max_width // len(text) * 10  # Even more generous width calculation
        
        # Use the smaller of the two, but with much higher minimums
        font_size = min(base_size, width_based_size)
        
        # Set much larger bounds - increase minimum significantly
        return max(80, min(font_size, 140))
    
    def _draw_text_line(self, draw: ImageDraw.Draw, text: str, y_position: int, 
                       frame_width: int, side_margin: int, font_size: int, bold: bool = False):
        """Draw a line of text centered horizontally."""
        # Try more stylish fonts first
        if bold:
            font_names = [
                "HelveticaNeue-Medium.ttc",   # macOS Helvetica Neue Medium
                "HelveticaNeue-Bold.ttc",     # macOS Helvetica Neue Bold
                "Helvetica-Bold.ttc",         # macOS Helvetica Bold
                "SF-Pro-Display-Medium.otf",  # macOS San Francisco Medium
                "Roboto-Medium.ttf",          # Google Roboto Medium
                "Inter-Medium.ttf",           # Inter Medium
                "Lato-Bold.ttf",              # Lato Bold
                "Arial-Bold.ttf",             # Fallback Arial Bold
                "DejaVuSans-Bold.ttf"         # Linux fallback Bold
            ]
        else:
            font_names = [
                "HelveticaNeue-Light.ttc",    # macOS Helvetica Neue Light
                "Helvetica Neue.ttc",         # macOS Helvetica Neue
                "Helvetica.ttc",              # macOS Helvetica
                "SF-Pro-Display-Light.otf",   # macOS San Francisco Light
                "Roboto-Light.ttf",           # Google Roboto Light
                "Inter-Light.ttf",            # Inter Light
                "Lato-Light.ttf",             # Lato Light
                "Arial.ttf",                  # Fallback Arial
                "DejaVuSans.ttf"              # Linux fallback
            ]
        
        font = None
        for font_name in font_names:
            try:
                font = ImageFont.truetype(font_name, font_size)
                break
            except (OSError, IOError):
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Center the text
        x_position = (frame_width - text_width) // 2
        
        draw.text((x_position, y_position), text, fill=self.text_color, font=font)
        return bbox[3] - bbox[1]  # Return text height
    
    def generate_frame(self, image_path: str, exif_data: ExifData, output_path: str):
        """Generate framed image with EXIF metadata."""
        # Open original image
        original_image = Image.open(image_path)
        
        # Calculate frame dimensions
        frame_info = self._calculate_frame_dimensions(original_image.size)
        
        # Create new image with frame
        framed_image = Image.new('RGB', frame_info['new_size'], self.frame_color)
        
        # Paste original image onto frame
        framed_image.paste(original_image, frame_info['image_position'])
        
        # Add metadata text
        draw = ImageDraw.Draw(framed_image)
        
        # Calculate font sizes and positions
        text_area_width = frame_info['new_size'][0] - (frame_info['side_margin'] * 2)
        line_height = frame_info['text_area_height'] // 2  # Two lines instead of three
        
        # First line: Camera and Lens info (larger and bold)
        camera_lens_text = f"{exif_data.camera_full_name}"
        if exif_data.lens_model and exif_data.lens_model != "Unknown Lens":
            camera_lens_text += f" / {exif_data.lens_model}"
        
        camera_font_size = self._get_font_size(
            camera_lens_text, text_area_width, line_height
        )
        # Make camera/lens text 30% larger
        camera_font_size = int(camera_font_size * 1.3)
        
        # First get actual text heights to calculate proper centering
        # Create temporary font to measure text heights
        temp_font_camera = None
        temp_font_settings = None
        
        # Get camera text font
        for font_name in ["HelveticaNeue-Medium.ttc", "Arial-Bold.ttf", "DejaVuSans-Bold.ttf"]:
            try:
                temp_font_camera = ImageFont.truetype(font_name, camera_font_size)
                break
            except (OSError, IOError):
                continue
        if temp_font_camera is None:
            temp_font_camera = ImageFont.load_default()
            
        # Get settings text font
        settings_text = exif_data.format_settings()
        settings_font_size = self._get_font_size(settings_text, text_area_width, line_height)
        for font_name in ["HelveticaNeue-Light.ttc", "Arial.ttf", "DejaVuSans.ttf"]:
            try:
                temp_font_settings = ImageFont.truetype(font_name, settings_font_size)
                break
            except (OSError, IOError):
                continue
        if temp_font_settings is None:
            temp_font_settings = ImageFont.load_default()
            
        # Calculate actual text heights
        camera_bbox = draw.textbbox((0, 0), camera_lens_text, font=temp_font_camera)
        camera_text_height = camera_bbox[3] - camera_bbox[1]
        
        settings_bbox = draw.textbbox((0, 0), settings_text, font=temp_font_settings)
        settings_text_height = settings_bbox[3] - settings_bbox[1]
        
        # Calculate total height and center position
        text_spacing = 80  # Spacing between lines
        total_actual_height = camera_text_height + text_spacing + settings_text_height
        text_start_y = frame_info['text_area_start'] + (frame_info['text_area_height'] - total_actual_height) // 2
        
        # Draw first line: Camera and Lens info
        y_pos = text_start_y
        actual_camera_height = self._draw_text_line(
            draw, camera_lens_text, y_pos, 
            frame_info['new_size'][0], frame_info['side_margin'], camera_font_size, bold=True
        )
        
        # Draw second line: Technical settings with proper spacing
        y_pos += actual_camera_height + text_spacing
        self._draw_text_line(
            draw, settings_text, y_pos,
            frame_info['new_size'][0], frame_info['side_margin'], settings_font_size
        )
        
        # Save the framed image
        framed_image.save(output_path, quality=80, optimize=True)
        
        return output_path