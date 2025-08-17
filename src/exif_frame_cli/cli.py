"""Command-line interface for exif-frame-cli."""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from PIL import Image

from .exif_reader import ExifReader
from .frame_generator import FrameGenerator
from .models import ExifData


@click.command()
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option(
    '--output', '-o',
    type=click.Path(),
    help='Output file path. If not specified, adds "_framed" to input filename.'
)
@click.option(
    '--style', '-s',
    type=click.Choice(['classic', 'modern'], case_sensitive=False),
    default='classic',
    help='Frame style to use (default: classic).'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output.'
)
@click.option(
    '--quality', '-q',
    type=click.IntRange(1, 100),
    default=95,
    help='JPEG quality (1-100, default: 95).'
)
@click.option(
    '--font-scale',
    type=click.FloatRange(0.5, 3.0),
    default=1.3,
    help='Font size scale factor (0.5-3.0, default: 1.3).'
)
@click.option(
    '--theme',
    type=click.Choice(['black', 'white'], case_sensitive=False),
    default='black',
    help='Frame color theme: black frame with white text, or white frame with black text (default: black).'
)
@click.option(
    '--layout',
    type=click.Choice(['compact', 'full'], case_sensitive=False),
    default='compact',
    help='Frame layout: compact (no top/sides margins) or full (margins on all sides) (default: compact).'
)
@click.version_option()
def main(input_file: str, output: Optional[str], style: str, verbose: bool, quality: int, font_scale: float, theme: str, layout: str):
    """Create instant camera-style frames for digital photos using EXIF metadata.
    
    INPUT_FILE: Path to the image file to process.
    """
    try:
        # Validate input file
        input_path = Path(input_file)
        if not input_path.exists():
            click.echo(f"Error: Input file '{input_file}' does not exist.", err=True)
            sys.exit(1)
        
        # Check if file is a supported image format
        try:
            with Image.open(input_path) as img:
                img.verify()
        except Exception:
            click.echo(f"Error: '{input_file}' is not a valid image file.", err=True)
            sys.exit(1)
        
        # Determine output path
        if output is None:
            output_path = input_path.parent / f"{input_path.stem}_framed{input_path.suffix}"
        else:
            output_path = Path(output)
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if verbose:
            click.echo(f"Processing: {input_path}")
            click.echo(f"Output: {output_path}")
            click.echo(f"Style: {style}")
            click.echo(f"Theme: {theme}")
            click.echo(f"Layout: {layout}")
            click.echo(f"Quality: {quality}")
            click.echo(f"Font scale: {font_scale}")
        
        # Extract EXIF data
        try:
            exif_reader = ExifReader(str(input_path))
            exif_data = exif_reader.extract_exif_data()
        except Exception as e:
            click.echo(f"Error reading EXIF data: {e}", err=True)
            # Continue with empty EXIF data
            exif_data = ExifData()
        
        if verbose:
            click.echo("\\nExtracted EXIF data:")
            click.echo(f"  Camera: {exif_data.camera_full_name}")
            click.echo(f"  Lens: {exif_data.lens_display_name}")
            click.echo(f"  Settings: {exif_data.format_settings()}")
        
        # Generate frame
        try:
            frame_generator = FrameGenerator(style=style, quality=quality, font_scale=font_scale, theme=theme, layout=layout)
            result_path = frame_generator.generate_frame(
                str(input_path), exif_data, str(output_path)
            )
            
            click.echo(f"✓ Frame generated successfully: {result_path}")
            
        except Exception as e:
            click.echo(f"Error generating frame: {e}", err=True)
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo("\\nOperation cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()