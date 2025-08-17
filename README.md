# exif-frame-cli

A command-line interface tool for creating stylish frames with EXIF metadata on digital photos, including cinematic letterbox effects.

## Features

Creates stylish frames and cinematic letterbox effects for digital photos using EXIF metadata. The tool offers two main modes:

### Standard Frame Mode
Creates minimalist frames for digital photos using EXIF metadata. The tool extracts and displays the following information:

**Left Side:**
- **Camera Model** - The camera used to take the photo (bold, white text)
- **Lens Information** - Lens model and specifications (smaller, gray text)

**Right Side:**
- **Technical Settings** - Focal length, aperture, shutter speed, and ISO (bold, white text)
- **Date & Time** - When the photo was taken (smaller, gray text)

The frame features a clean black background with no top, left, or right margins - only a bottom area for metadata display, creating a modern and professional look.

### Cinescope Mode
Creates cinematic letterbox effects with black bars on the top and bottom of images to achieve movie-like aspect ratios:

- **Aspect Ratios**: 2.35:1 (default), 2.40:1, or 1.85:1 cinematic formats
- **EXIF Display**: Shows camera, lens, settings, and timestamp information in the bottom letterbox bar
- **Center-aligned Layout**: Information is displayed in a classic instant camera style with centered text
- **Professional Look**: Creates the authentic cinematic experience with proper letterboxing

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

# Use full instant camera layout with margins on all sides
exif-frame-cli photo.jpg --layout full

# Create cinematic letterbox effect with 2.35:1 aspect ratio
exif-frame-cli photo.jpg --cinescope

# Create letterbox with different aspect ratio
exif-frame-cli photo.jpg --cinescope --aspect-ratio 2.40

# Specify custom output file
exif-frame-cli photo.jpg --output framed_photo.jpg

# Enable verbose output to see EXIF details
exif-frame-cli photo.jpg --verbose
```

### Command Options

#### Basic Options
- `INPUT_FILE`: Path to the image file to process (required)
- `--output, -o`: Output file path (optional, defaults to `{input}_framed.{ext}`)
- `--verbose, -v`: Enable verbose output to display extracted EXIF data
- `--help`: Show help message
- `--version`: Show version information

#### Frame Options
- `--theme`: Frame color theme - `black` (default) or `white`
- `--layout`: Frame layout - `compact` (default, no top/side margins) or `full` (margins on all sides)
- `--font-scale`: Font size scale factor (0.5-3.0, default: 1.3)
- `--quality`: JPEG quality (1-100, default: 95)

#### Cinescope Options
- `--cinescope`: Enable cinematic letterbox mode
- `--aspect-ratio`: Cinescope aspect ratio - `2.35` (default), `2.40`, or `1.85`

### Examples

```bash
# Process with default settings (compact black frame)
exif-frame-cli vacation_photo.jpg
# Output: vacation_photo_framed.jpg

# Create white frame with black text
exif-frame-cli vacation_photo.jpg --theme white

# Classic instant camera style with full margins
exif-frame-cli vacation_photo.jpg --layout full

# Combine options: white frame with full layout
exif-frame-cli vacation_photo.jpg --theme white --layout full

# Custom output location
exif-frame-cli vacation_photo.jpg -o ~/Desktop/framed_vacation.jpg

# Cinematic letterbox effects
exif-frame-cli movie_scene.jpg --cinescope
exif-frame-cli movie_scene.jpg --cinescope --aspect-ratio 2.40
exif-frame-cli movie_scene.jpg --cinescope --font-scale 1.8

# View EXIF data extraction process
exif-frame-cli portrait.jpg --verbose
```

### Sample Output

The tool creates different types of outputs depending on the mode:

#### Standard Frame Mode

**Layout Options:**
- `--layout compact` (default): Image fills the frame edge-to-edge with only bottom metadata area (15% of image height)
- `--layout full`: Classic instant camera style with margins on all sides (5% top/sides, 25% bottom)

**Theme Options:**
- `--theme black` (default): Black frame with white/light gray text
- `--theme white`: White frame with black/dark gray text

**Text Layout (Compact):**
- **Left side**: Camera name (bold) and lens model (lighter)
- **Right side**: Settings like "70mm f/2.8 1/4s ISO6400" (bold) and timestamp (lighter)

**Text Layout (Full):**
- **Center-aligned**: Camera and lens info on first line, settings and timestamp on second line

#### Cinescope Mode

**Letterbox Effect:**
- Adds black bars to top and bottom of image to create cinematic aspect ratios
- Preserves original image quality while adding cinematic feel

**EXIF Display:**
- **Center-aligned** in bottom letterbox bar
- **First line**: Camera model / Lens information (bold, white)
- **Second line**: Settings • Timestamp (lighter, gray)

**Aspect Ratios:**
- `2.35:1` - Classic anamorphic widescreen (default)
- `2.40:1` - Ultra widescreen format  
- `1.85:1` - Standard widescreen format

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
