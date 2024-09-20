# Image Pixel Modifier

This Python script allows you to access and modify pixel values of an image while keeping the image header intact. It uses the `Pillow` library to manipulate images and provides a simple example of color inversion.

## Features

- **Access pixel data**: Modify each pixel's RGB values.
- **Preserve the image header**: The header information remains unchanged when saving the modified image.

## Prerequisites

Make sure you have Python installed on your system. You also need the `Pillow` library to run this script.

## Installation

1. Clone this repository or download the files.
2. Install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your image in the project directory (e.g., `test.png`).
2. Run the Python script to modify the image:

    ```bash
    python modify_image.py
    ```

    The script will create a new image file (e.g., `clone_with_mods.png`) with modified pixel values.

### Example Modification

In the example provided, the script inverts the colors of the image by subtracting the RGB values from 255. You can customize the modification logic within the script as needed.

## Files

- `modify_image.py`: The Python script to modify the image pixels.
- `requirements.txt`: Lists the required Python packages (`Pillow`).
- `README.md`: This file.
