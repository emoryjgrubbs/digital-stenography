from PIL import Image
import sys
import os


def modify_image_string(input_image_path, output_image_path, binary_message):
    # variables
    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    img_x = 0
    img_y = 0
    lsb_color = 0  # 0 = red, 1 = green, 2 = blue
    lsb_bit = 0  # 2^lsb_bit is what gets modified

    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    binary_message += '1111111111111110'  # End of message delimiter

    # modify pixels with image data
    for message_index in range(len(binary_message)):
        pixels[img_x, img_y] = modify_pixel(pixels[img_x, img_y], binary_message[message_index], lsb_color, lsb_bit)
        # if lsb_bit == 8, the all bit of all colors of all pixels modified, ABORT
        if lsb_bit == 8:
            return -1
        if lsb_color == 2:
            lsb_bit += 1
            lsb_color = lsb_color % 2
        if img_y == height-1:
            lsb_color += 1
        if img_x == width-1:
            img_y += 1
            img_y = img_y % (height-1)
        img_x += 1
        img_x = img_x % (width-1)

    # ending clean up/saving
    image.save(output_image_path)
    return 0


def modify_image_txt(input_image_path, output_image_path, message_file_path):
    # variables
    get_eof = open(message_file_path, "a")
    eof = get_eof.tell()
    get_eof.close()
    message_text = open(message_file_path, 'rb')
    image = Image.open(input_image_path)
    pixels = image.load()

    width, height = image.size

    img_x = 0
    img_y = 0
    lsb_color = 0  # 0 = red, 1 = green, 2 = blue
    lsb_bit = 0  # 2^lsb_bit is what gets modified

    file_index = 0

    # loop through 512 byte chunks of text data, until file_index + 512 > eof
    while file_index + 512 > eof:
        # read data
        message_chunk = message_text.read(512)
        binary_message_chunk = text_to_binary(message_chunk)
        # modify pixels with image data
        for chunk_index in range(512):
            pixels[img_x, img_y] = modify_pixel(pixels[img_x, img_y], binary_message_chunk[chunk_index], lsb_color, lsb_bit)
            # if lsb_bit == 8, the all bit of all colors of all pixels modified, ABORT
            if lsb_bit == 8:
                return -1
                # "Aborting, Image Cannot Contain Message Data"
            # TODO fix for greyscale images
            if lsb_color == 2:
                lsb_bit += 1
                lsb_color = lsb_color % 2
            if img_y == height-1:
                lsb_color += 1
            if img_x == width-1:
                img_y += 1
                img_y = img_y % (height-1)
            img_x += 1
            img_x = img_x % (width-1)
        file_index += 512

    # do a final pass with the remaining bytes, appending the ending delimiter
    # read data
    message_chunk = message_text.read(eof - file_index)
    binary_message_chunk = text_to_binary(message_chunk)
    binary_message_chunk += '1111111111111110'  # End of message delimiter
    # modify pixels with image data
    for chunk_index in range(len(message_chunk)):
        pixels[img_x, img_y] = modify_pixel(pixels[img_x, img_y], binary_message_chunk[chunk_index], lsb_color, lsb_bit)
        # if lsb_bit == 8, the all bit of all colors of all pixels modified, ABORT
        if lsb_bit == 8:
            return -1
        # TODO fix for greyscale images
        if lsb_color == 2:
            lsb_bit += 1
            lsb_color = lsb_color % 2
        if img_y == height-1:
            lsb_color += 1
        if img_x == width-1:
            img_y += 1
            img_y = img_y % (height-1)
        img_x += 1
        img_x = img_x % (width-1)

    # ending clean up/saving
    image.save(output_image_path)
    message_text.close()
    return 0


def modify_pixel(pixel, data, color_channel, modify_bit):
    # TODO fix for greyscale images
    r, g, b = pixel

    # shift data to lowest unmodified bit
    shifted_data = int(data) << modify_bit

    # switch case for the color channel to be modified
    match color_channel:
        case 0:
            # Modify the least significant bit of the red channel
            new_r = (r & ~1) | int(shifted_data)
            new_g = g
            new_b = b
        case 1:
            # Modify the least significant bit of the green channel
            new_r = r
            new_g = (r & ~1) | int(shifted_data)
            new_b = b
        case 2:
            # Modify the least significant bit of the blue channel
            new_r = r
            new_g = g
            new_b = (r & ~1) | int(shifted_data)

    # return modified pixel data
    return (new_r, new_g, new_b)


def text_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])


def text_to_binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


def get_message_type(message):
    status = 0
    if len(message) > 4 and message[len(message)-4:] == '.txt':
        status = 2
    else:
        status = 1
    return status


# status -1 incorrect number of args
# status 0 nothing happened
# status 1 all good, secret message is a string
# status 2 all good, secret message is a txt
def handle_argv(argv):
    status = 0
    input_file = 'test-images/airplaneU2.png'
    output_file = 'output.png'
    secret_message = ''
    match len(argv):
        case 4:
            status = get_message_type(sys.argv[3])
            input_file = sys.argv[1]
            output_file = sys.argv[2]
            secret_message = sys.argv[3]
        case 3:
            status = get_message_type(sys.argv[2])
            input_file = sys.argv[1]
            secret_message = sys.argv[2]
        case 2:
            status = get_message_type(sys.argv[1])
            secret_message = sys.argv[1]
        case 1:
            status = -1
        case _:
            status = -2
    return [status, input_file, output_file, secret_message]


def main():
    standardized_argv = handle_argv(sys.argv)
    status = standardized_argv[0]
    input_file = standardized_argv[1]
    output_file = standardized_argv[2]
    secret_message = standardized_argv[3]

    match status:
        case -2:
            print("Error, Too Many Arguments")
        case -1:
            print("Error, Too Few Arguments")
        case 1:
            if not os.path.isfile(input_file):
                print("Error, Input Image Does Not Exist")
            # if os.path.isfile(output_file) and not force:
            #    print("Warning, Output Image Exists\n If Your Wish to Overwrite, Specify -f?")
            else:
                binary_message = text_to_binary(secret_message)
                modify_image_string(input_file, output_file, binary_message)
                print(f"Success, String Embeded in Image: {output_file}")
        case 2:
            if not os.path.isfile(input_file):
                print("Error, Input Image Does Not Exist")
            # if os.path.isfile(output_file) and not force:
            #    print("Warning, Output Image Exists\n If Your Wish to Overwrite, Specify -f?")
            if not os.path.isfile(secret_message):
                print("Error, Message File Does Not Exist")
            else:
                modify_image_txt(input_file, output_file, secret_message)
                print(f"Success, TXT File Contents Embeded in Image: {output_file}")
        case _:
            print("Error, Unknown Error")


if __name__ == "__main__":
    main()
