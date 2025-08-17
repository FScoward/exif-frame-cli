"""Frame generation for instant camera-style photos."""

from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from .models import ExifData


class FrameGenerator:
    """Generate instant camera-style frames with EXIF metadata."""
    
    def __init__(self, style: str = "classic", quality: int = 95, font_scale: float = 1.0, theme: str = "black", layout: str = "compact"):
        self.style = style
        self.quality = quality
        self.font_scale = font_scale
        self.theme = theme.lower()
        self.layout = layout.lower()
        
        # Set colors based on theme
        if self.theme == "white":
            self.frame_color = (255, 255, 255)  # White background
            self.primary_text_color = (0, 0, 0)     # Black text
            self.secondary_text_color = (100, 100, 100)  # Dark gray text
        else:  # black theme (default)
            self.frame_color = (0, 0, 0)        # Black background
            self.primary_text_color = (255, 255, 255)   # White text
            self.secondary_text_color = (180, 180, 180) # Light gray text
        
    def _calculate_frame_dimensions(self, image_size: Tuple[int, int]) -> dict:
        """Calculate frame dimensions based on image size."""
        width, height = image_size
        
        if self.layout == "full":
            # Full margins on all sides - original instant camera style
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
        else:  # compact layout (default)
            # No margins on top, left, and right - only bottom margin for text
            side_margin = 0                    # No side margins
            top_margin = 0                     # No top margin
            bottom_margin = int(height * 0.15) # 15% of height for metadata area
            
            new_width = width                  # Same width as original image
            new_height = height + bottom_margin # Only add bottom margin
            
            return {
                'new_size': (new_width, new_height),
                'image_position': (0, 0),      # Position image at top-left corner
                'text_area_start': height,     # Text starts right after image
                'text_area_height': bottom_margin,
                'side_margin': 0               # No side margins for text centering
            }
    
    def _get_font_size(self, text: str, max_width: int, max_height: int) -> int:
        """Calculate appropriate font size for given text and area."""
        # Larger base font size for better readability
        base_size = max_height // 3  # Use 1/3 of available height
        
        # Calculate based on text length and available width
        width_based_size = max_width // len(text) * 3  # More generous width calculation
        
        # Use the smaller of the two
        font_size = min(base_size, width_based_size)
        
        # Set larger bounds for better visibility and apply scale factor
        scaled_font_size = int(font_size * self.font_scale)
        return max(int(24 * self.font_scale), min(scaled_font_size, int(72 * self.font_scale)))
    
    def _draw_text_left(self, draw: ImageDraw.Draw, text: str, x_position: int, y_position: int, 
                       font_size: int, bold: bool = False, text_color=None):
        """Draw text aligned to the left."""
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
        
        color = text_color if text_color is not None else self.primary_text_color
        draw.text((x_position, y_position), text, fill=color, font=font)
        return bbox[3] - bbox[1]  # Return text height
    
    def _draw_text_center(self, draw: ImageDraw.Draw, text: str, center_x: int, y_position: int, 
                         font_size: int, bold: bool = False, text_color=None):
        """Draw text centered horizontally."""
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
        
        # Position text centered
        x_position = center_x - text_width // 2
        
        color = text_color if text_color is not None else self.primary_text_color
        draw.text((x_position, y_position), text, fill=color, font=font)
        return bbox[3] - bbox[1]  # Return text height
    
    def _draw_text_right(self, draw: ImageDraw.Draw, text: str, right_x: int, y_position: int, 
                        font_size: int, bold: bool = False, text_color=None):
        """Draw text aligned to the right."""
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
        
        # Position text so it ends at right_x
        x_position = right_x - text_width
        
        color = text_color if text_color is not None else self.primary_text_color
        draw.text((x_position, y_position), text, fill=color, font=font)
        return bbox[3] - bbox[1]  # Return text height
    
    def generate_frame(self, image_path: str, exif_data: ExifData, output_path: str):
        """Generate framed image with EXIF metadata."""
        # Open original image
        original_image = Image.open(image_path)
        
        # Try to detect original image quality to preserve it
        original_quality = 95  # Default high quality
        try:
            # Check if the original image has quality info
            if hasattr(original_image, 'quantization'):
                # Estimate quality from quantization tables (rough estimate)
                original_quality = 95  # Conservative high quality for preservation
        except:
            original_quality = 95
        
        # Calculate frame dimensions
        frame_info = self._calculate_frame_dimensions(original_image.size)
        
        # Create new image with frame
        framed_image = Image.new('RGB', frame_info['new_size'], self.frame_color)
        
        # Paste original image onto frame without recompression
        framed_image.paste(original_image, frame_info['image_position'])
        
        # Add metadata text
        draw = ImageDraw.Draw(framed_image)
        
        # Calculate layout based on layout mode
        if self.layout == "full":
            # Use frame side margins plus additional padding
            left_margin = frame_info['side_margin'] + 40
            right_margin = frame_info['side_margin'] + 40
        else:  # compact layout
            left_margin = 100   # Left margin for left-aligned text
            right_margin = 100  # Right margin for right-aligned text
        
        # Left side: Camera and Lens info
        camera_lens_text = f"{exif_data.camera_full_name}"
        if exif_data.lens_model and exif_data.lens_model != "Unknown Lens":
            camera_lens_text += f"\n{exif_data.lens_model}"
        
        # Right side: Settings and DateTime
        settings_text = exif_data.format_settings()
        datetime_text = exif_data.format_datetime()
        if datetime_text:
            right_side_text = f"{settings_text}\n{datetime_text}"
        else:
            right_side_text = settings_text
        
        # Calculate font sizes (smaller to match sample style)
        base_font_size = max(24, int(frame_info['text_area_height'] * 0.15))
        
        # Adjust font size based on layout
        if self.layout == "full":
            base_font_size = int(base_font_size * 1.0)  # Normal size for full layout
        else:
            base_font_size = int(base_font_size * 1.3)  # Larger size for compact layout
            
        small_font_size = int(base_font_size * 0.75)  # Second line smaller
        
        # Use theme colors
        primary_color = self.primary_text_color
        secondary_color = self.secondary_text_color
        
        # Calculate vertical positioning
        text_area_center_y = frame_info['text_area_start'] + frame_info['text_area_height'] // 2
        
        if self.layout == "full":
            # Full layout: center-aligned text like original instant camera style
            # Combine camera and settings into single centered text blocks
            camera_info_text = f"{exif_data.camera_full_name}"
            if exif_data.lens_model and exif_data.lens_model != "Unknown Lens":
                camera_info_text += f" / {exif_data.lens_model}"
            
            settings_info_text = exif_data.format_settings()
            if exif_data.format_datetime():
                settings_info_text += f" • {exif_data.format_datetime()}"
            
            # Calculate text positioning for center alignment
            large_line_height = int(base_font_size * 1.4)
            small_line_height = int(small_font_size * 1.4)
            total_height = large_line_height + small_line_height
            
            start_y = text_area_center_y - total_height // 2
            frame_center_x = frame_info['new_size'][0] // 2
            
            # Draw camera info (larger, bold)
            self._draw_text_center(draw, camera_info_text, frame_center_x, start_y, base_font_size, bold=True, text_color=primary_color)
            
            # Draw settings info (smaller, lighter)
            self._draw_text_center(draw, settings_info_text, frame_center_x, start_y + large_line_height, small_font_size, bold=False, text_color=secondary_color)
            
        else:
            # Compact layout: left/right aligned text
            camera_lines = camera_lens_text.split('\n')
            
            # Calculate actual text heights for proper centering
            large_line_height = int(base_font_size * 1.2)
            small_line_height = int(small_font_size * 1.2)
            
            # Calculate total height for left side
            total_left_height = 0
            if len(camera_lines) > 0:
                total_left_height += large_line_height  # First line
            if len(camera_lines) > 1:
                total_left_height += small_line_height  # Second line
            
            start_y_left = text_area_center_y - total_left_height // 2
            current_y = start_y_left
            
            for i, line in enumerate(camera_lines):
                if i == 0:  # First line (camera) - larger, bold, white
                    self._draw_text_left(draw, line, left_margin, current_y, base_font_size, bold=True, text_color=primary_color)
                    current_y += large_line_height
                else:  # Second line (lens) - smaller, light, gray
                    self._draw_text_left(draw, line, left_margin, current_y, small_font_size, bold=False, text_color=secondary_color)
                    current_y += small_line_height
            
            # Draw right side text (settings and datetime)
            right_lines = right_side_text.split('\n')
            
            # Calculate total height for right side
            total_right_height = 0
            if len(right_lines) > 0:
                total_right_height += large_line_height  # First line
            if len(right_lines) > 1:
                total_right_height += small_line_height  # Second line
            
            start_y_right = text_area_center_y - total_right_height // 2
            current_y = start_y_right
            
            for i, line in enumerate(right_lines):
                if i == 0:  # First line (settings) - larger, bold, white
                    self._draw_text_right(draw, line, frame_info['new_size'][0] - right_margin, current_y, base_font_size, bold=True, text_color=primary_color)
                    current_y += large_line_height
                else:  # Second line (datetime) - smaller, light, gray
                    self._draw_text_right(draw, line, frame_info['new_size'][0] - right_margin, current_y, small_font_size, bold=False, text_color=secondary_color)
                    current_y += small_line_height
        
        # Save with specified quality
        framed_image.save(output_path, quality=self.quality, optimize=True)
        
        return output_path