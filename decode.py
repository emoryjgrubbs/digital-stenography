from PIL import Image

def extract_message_from_image(image_path):
    image = Image.open(image_path)
    pixels = image.load()
    
    width, height = image.size
    
    binary_message = ""
    end_of_message = '1111111111111110'
    
    # Loop through pixels
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            binary_message += str(r & 1)
            
            # Check if the end of the message is reached
            if binary_message.endswith(end_of_message):
                binary_message = binary_message[:-len(end_of_message)]
                return binary_to_text(binary_message)

    return "No hidden message found."

def binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def main():
    image_path = "clone.png"
    hidden_message = extract_message_from_image(image_path)
    print(f"Hidden message: {hidden_message}")

if __name__ == "__main__":
    main()