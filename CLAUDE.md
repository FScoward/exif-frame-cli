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

The repository is minimal and contains only:
- README.md with project description and feature overview
- LICENSE (MIT)
- No source code or build configuration yet

## Development Notes

Since this project is in its infancy:
- The programming language and build system are not yet determined
- No package managers, dependencies, or build tools are configured
- The architecture and implementation approach are still to be decided

When developing this project, consider:
- CLI framework selection (e.g., Click for Python, clap for Rust, Commander.js for Node.js)
- Image processing library for frame generation
- EXIF data extraction library
- Output format options (PNG, JPEG with embedded frames)
- Cross-platform compatibility requirements