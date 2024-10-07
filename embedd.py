from PIL import Image

def clone_image(input_image_path, output_image_path, binary_message):
    image = Image.open(input_image_path)
    pixels = image.load()
    
    width, height = image.size
    
    binary_message += '1111111111111110'  # End of message delimiter
    
    message_index = 0
    
    # Loop through pixels 
    for x in range(width):
        for y in range(height):
            if message_index < len(binary_message):
                pixels[x, y] = modify_pixel(pixels[x, y], binary_message[message_index])
                message_index += 1
            else:
                break
        if message_index >= len(binary_message):
            break

    image.save(output_image_path)
    print(f"Image saved as {output_image_path} 👍")

def modify_pixel(pixel, bit):
    r, g, b = pixel
    
    # Modify the least significant bit of the red channel
    new_r = (r & ~1) | int(bit)
    new_g = g
    new_b = b
    
    return (new_r, new_g, new_b)

def text_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])

def text_to_binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def main():
    secret_message = input("Enter the secret message to embed: ")
    binary_message = text_to_binary(secret_message)
    clone_image("test.png", "clone.png", binary_message)

if __name__ == "__main__":
    main()
