from PIL import Image
import pillow_heif
import os

# Register HEIF opener
pillow_heif.register_heif_opener()

# Get all HEIC and WebP files
image_files = [f for f in os.listdir('.') if f.lower().endswith(('.heic', '.webp'))]

for img_file in image_files:
    # Read image
    image = Image.open(img_file)
    
    # Create JPG filename
    jpg_file = os.path.splitext(img_file)[0] + '.jpg'
    print(jpg_file)
    
    # Convert to RGB if necessary (for WebP with transparency)
    if image.mode in ('RGBA', 'LA'):
        background = Image.new('RGB', image.size, 'white')
        background.paste(image, mask=image.split()[-1])
        image = background
    
    # Save as JPG
    image.save(jpg_file, 'JPEG')