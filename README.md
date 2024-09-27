
# PNG Manipulation

This Python script allows you to access PNG files, alter the image data, and write the altered image to a secondary file.

## Features

- **Print Image Header**: The header information is printed, before being copied to the output file.
- **Alter IDAT Data**: The other chunks are read, and only the data segments of the IDAT chunks are decompressed and modified.

## Installation

1. Clone this repository or download the files.

## Usage

1. Place your image in the project directory (e.g., `test.png`).
2. Run the Python script to modify the image:

    ```bash
    python filter.py source.png
    ```

    The script will create a new image file (e.g., `out-test.png`) with modified information.

## Files

- `filter.py`: The Python script to modify the image pixels.
- `README.md`: This file.
