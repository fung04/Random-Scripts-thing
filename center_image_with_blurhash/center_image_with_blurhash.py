import os
from PIL import Image
import blurhash
import numpy as np

def generate_blurhash(image_path, components_x=4, components_y=3):
    with Image.open(image_path) as img:
        rgb_img = img.convert("RGB")
    img_array = np.array(rgb_img)
    return blurhash.encode(img_array, components_x, components_y)

def decode_blurhash(hash_string, width, height):
    #img_array = np.array(blurhash.decode(hash_string, width, height))
    
    # img_array = (img_array * 255).astype(np.uint8)
    return Image.fromarray(np.array(blurhash.decode(hash_string, width, height)).astype('uint8'))

def center_image_on_canvas(image_path, canvas_size=(500, 500)):
    canvas_blurhash = generate_blurhash(image_path)
    print(canvas_blurhash)
    canvas = decode_blurhash(canvas_blurhash, *canvas_size) 
    # Open the image
    with Image.open(image_path) as img:
        # fit image to the canva
        img.thumbnail(canvas_size)

        # Calculate position to paste the image (center)
        paste_position = (
            (canvas_size[0] - img.width) // 2,
            (canvas_size[1] - img.height) // 2
        )
        
        # Paste the image onto the canvas
        canvas.paste(img, paste_position)
    
    return canvas

def process_images_in_directory(directory):
    # Ensure the output directory exists
    output_dir = os.path.join(directory, 'centered_images')
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each image in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(directory, filename)
            centered_image = center_image_on_canvas(image_path)
            
            # Save the centered image
            output_path = os.path.join(output_dir, f'{filename}')
            centered_image.save(output_path, quality=100, subsampling=0)
            print(f"Processed: {filename}")

# Usage
root_directory = '.'  # Current directory
process_images_in_directory(root_directory)