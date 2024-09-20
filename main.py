from PIL import Image

def clone_image(input_image_path, output_image_path):

    image = Image.open(input_image_path)
    pixels = image.load()
    
    width, height = image.size
    
    # Loop through pixels 
    for x in range(width):
        for y in range(height):
            pixels[x, y] = modify_pixel(pixels[x, y])
    

    image.save(output_image_path)
    print(f"Image saved as {output_image_path} 👍")

def modify_pixel(pixel):
    r, g, b = pixel
    
    #add lsb insertion here
    new_r = r
    new_g = g
    new_b = b
    
    return (new_r, new_g, new_b)

clone_image("test.png", "clone.png")
