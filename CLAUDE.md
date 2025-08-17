# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an early-stage CLI tool for creating instant camera-style frames on digital photos using EXIF metadata. The project is currently in the initial setup phase with only basic documentation files present.

## Project Purpose

The tool extracts EXIF metadata from digital photos and overlays it on instant camera-style frames, displaying:
- Camera model and lens information
- Technical settings (focal length, aperture, shutter speed, ISO)

This creates a nostalgic instant camera aesthetic for digital photography.

## Current State

The project is implemented in Python with the following structure:
- `pyproject.toml` - Poetry configuration with dependencies
- `src/exif_frame_cli/` - Main package directory
- `cli.py` - Click-based command-line interface
- `exif_reader.py` - EXIF data extraction using Pillow
- `frame_generator.py` - Frame creation and text overlay
- `models.py` - Data classes for EXIF information

## Development Commands

```bash
# Install dependencies
poetry install

# Run the CLI tool
poetry run exif-frame-cli input.jpg

# Development mode
poetry shell
exif-frame-cli input.jpg

# Code formatting
poetry run black src/

# Linting
poetry run flake8 src/

# Run tests (when added)
poetry run pytest
```

## Architecture

- **CLI Framework**: Click for command-line interface
- **Image Processing**: Pillow (PIL) for EXIF extraction and frame generation
- **Package Management**: Poetry for dependency management
- **Entry Point**: Configured in pyproject.toml as `exif-frame-cli`

## Key Components

- `ExifData` model holds extracted metadata
- `ExifReader` extracts and formats EXIF data from images
- `FrameGenerator` creates instant camera-style frames with metadata overlay
- CLI supports multiple frame styles and verbose output