from PIL import Image
import sys


def extract_message_from_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    width, height = image.size

    binary_message = ""
    end_of_message = '1111111111111110'

    # Loop through pixels
    for s in range(0, 8):
        for c in range(0, 2):
            for y in range(height):
                for x in range(width):
                    # TODO fix for greyscale
                    r, g, b = pixels[x, y]
                    filter = 2**s
                    match c:
                        # red
                        case 0:
                            binary_message += str((r & filter) >> s)
                        # green
                        case 1:
                            binary_message += str((g & filter) >> s)
                        # blue
                        case 2:
                            binary_message += str((b & filter) >> s)

                    # Check if the end of the message is reached
                    if binary_message.endswith(end_of_message):
                        print(binary_to_text(binary_message[:-len(end_of_message)]))
                        return
                    elif len(binary_message) == 512:
                        print(binary_to_text(binary_message), end='')
                        binary_message = ''

    return "No hidden message found."


def binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def main():
    if len(sys.argv) == 2:
        image_path = sys.argv[1]
        extract_message_from_image(image_path)
    else:
        print("No Image Path Provided.")


if __name__ == "__main__":
    main()
