# Image Pixel Modifier

This Python script allows you to access and modify pixel values of an image while keeping the image header intact. It uses the `Pillow` library to manipulate images and provides a simple example of color inversion.

## Prerequisites

Make sure you have Python installed on your system. You also need the `Pillow` library to run this script.

## Installation

1. Clone this repository or download the files.
2. Install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Python program to encode the message

Example:
    ```bash
    python embed.py [input image] [output image] [message]
    ```
    
    input image: the cover image to be modified
    output image: the modified stego image (if unspecified, default to output.png)
    message: the text to be hidden (either simple string text or the path to a file ending in .txt)

    flags can be used as an alternative format, they can appear in any order, and any unflagged input will be matched in the standard order to the needed input
    --input-image [input image]
        -i [input image]
    --output-image [output image]
        -o [output image]
    --string [message]
        -s [message]
    --text-file [message]
        -t [message]

    -f: overwrite the image specified by the [output image]

2. Run the Python program to decode the message
    
    ```bash
    python decode.py [input image]
    ```

    input image: the stego image to decode


## Files

- `embed.py`: Program to encode the stego image
- `decode.py`: Program to decode the stego image
- `requirements.txt`: Lists the required Python packages (`Pillow`).
- `README.md`: This file.
