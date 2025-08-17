# exif-frame-cli

A command-line interface tool for extracting EXIF data and creating frames from images.

## Features

Creates instant camera-style frames for digital photos using EXIF metadata. The tool extracts and displays the following information on photo frames:

- **Camera Model** - The camera used to take the photo
- **Lens Information** - Lens model and specifications  
- **Focal Length** - The focal length setting used
- **Aperture (f-stop)** - The f-value/aperture setting
- **Shutter Speed** - The exposure time
- **ISO Sensitivity** - The ISO setting used

This mimics the information typically printed on instant camera photo frames, giving your digital photos a nostalgic instant camera aesthetic.

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
# Process a single image
exif-frame-cli photo.jpg

# Specify output file
exif-frame-cli photo.jpg --output framed_photo.jpg

# Use different frame style
exif-frame-cli photo.jpg --style modern

# Enable verbose output
exif-frame-cli photo.jpg --verbose
```

### Command Options

- `INPUT_FILE`: Path to the image file to process (required)
- `--output, -o`: Output file path (optional, defaults to `{input}_framed.{ext}`)
- `--style, -s`: Frame style - `classic` or `modern` (default: classic)
- `--verbose, -v`: Enable verbose output
- `--help`: Show help message
- `--version`: Show version information

### Examples

```bash
# Process with default settings
exif-frame-cli vacation_photo.jpg

# Custom output location
exif-frame-cli vacation_photo.jpg -o ~/Desktop/framed_vacation.jpg

# Modern style with verbose output
exif-frame-cli portrait.jpg --style modern --verbose
```

## Requirements

- Python 3.8 or higher
- PIL/Pillow for image processing
- Click for CLI interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

FScoward
