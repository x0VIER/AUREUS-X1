import sys
from PIL import Image

def crop_image(image_path, output_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        width, height = img.size
        
        # We want a very slim profile, e.g., 3:1 or 4:1 aspect ratio.
        # Let's crop the top and bottom to make it focused on the center.
        target_height = int(width / 4)
        
        left = 0
        right = width
        top = (height - target_height) // 2
        bottom = top + target_height
        
        # Crop the center horizontal strip
        img_cropped = img.crop((left, top, right, bottom))
        
        # Now let's try to remove some of the dark background to make it 'transparent'
        # if the user requested background-free. The banner we copied was probably a solid 
        # color background. Let's make the darkest pixels transparent or semi-transparent.
        data = img_cropped.getdata()
        new_data = []
        for item in data:
            # item is (R, G, B, A)
            # If the pixel is very dark (close to black), make it transparent
            # Calculate brightness
            brightness = (item[0] + item[1] + item[2]) / 3
            if brightness < 20: # Very dark threshold
                new_data.append((item[0], item[1], item[2], 0))
            else:
                new_data.append(item)
                
        img_cropped.putdata(new_data)
        
        img_cropped.save(output_path, "PNG")
        print(f"Successfully slimmed and processed banner to {width}x{target_height}. Saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python crop_banner.py <input> <output>")
        sys.exit(1)
        
    crop_image(sys.argv[1], sys.argv[2])
