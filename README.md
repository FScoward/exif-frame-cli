# exif-frame-cli

A command-line interface tool for creating stylish black frames with EXIF metadata on digital photos.

## Features

Creates minimalist black frames for digital photos using EXIF metadata. The tool extracts and displays the following information:

**Left Side:**
- **Camera Model** - The camera used to take the photo (bold, white text)
- **Lens Information** - Lens model and specifications (smaller, gray text)

**Right Side:**
- **Technical Settings** - Focal length, aperture, shutter speed, and ISO (bold, white text)
- **Date & Time** - When the photo was taken (smaller, gray text)

The frame features a clean black background with no top, left, or right margins - only a bottom area for metadata display, creating a modern and professional look.

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/FScoward/exif-frame-cli.git
cd exif-frame-cli

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/FScoward/exif-frame-cli.git
cd exif-frame-cli

# Install globally (can use `exif-frame-cli` command anywhere)
pip install -e .

# Uninstall
pip uninstall exif-frame-cli -y
```

## Usage

### Basic Usage

```bash
# Process a single image (creates photo_framed.jpg)
exif-frame-cli photo.jpg

# Create white frame instead of black
exif-frame-cli photo.jpg --theme white

# Specify custom output file
exif-frame-cli photo.jpg --output framed_photo.jpg

# Enable verbose output to see EXIF details
exif-frame-cli photo.jpg --verbose
```

### Command Options

- `INPUT_FILE`: Path to the image file to process (required)
- `--output, -o`: Output file path (optional, defaults to `{input}_framed.{ext}`)
- `--theme`: Frame color theme - `black` (default) or `white`
- `--verbose, -v`: Enable verbose output to display extracted EXIF data
- `--help`: Show help message
- `--version`: Show version information

### Examples

```bash
# Process with default settings (black frame)
exif-frame-cli vacation_photo.jpg
# Output: vacation_photo_framed.jpg

# Create white frame with black text
exif-frame-cli vacation_photo.jpg --theme white

# Custom output location
exif-frame-cli vacation_photo.jpg -o ~/Desktop/framed_vacation.jpg

# View EXIF data extraction process
exif-frame-cli portrait.jpg --verbose
```

### Sample Output

The tool creates a frame with:
- **Image positioned at the top** with no margins
- **Bottom area** containing metadata (15% of image height)
- **Left side**: Camera name (bold) and lens model (lighter)
- **Right side**: Settings like "70mm f/2.8 1/4s ISO6400" (bold) and timestamp (lighter)
- **100px margins** from left and right edges for text positioning

**Theme Options:**
- `--theme black` (default): Black frame with white/light gray text
- `--theme white`: White frame with black/dark gray text

## Requirements

- Python 3.8 or higher
- PIL/Pillow for image processing and EXIF extraction
- Click for CLI interface

## Development

```bash
# Install development dependencies
poetry install

# Run formatting
poetry run black src/

# Run linting
poetry run flake8 src/

# Run tests (when available)
poetry run pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

FScoward
