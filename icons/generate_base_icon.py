from PIL import Image, ImageDraw, ImageFont
import os

def create_base_icon():
    # Create a 1024x1024 image with gradient background
    img = Image.new('RGB', (1024, 1024), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Add circular background
    draw.ellipse([100, 100, 924, 924], fill='#3498db')
    
    # Add text
    try:
        font = ImageFont.truetype("/System/Library/Fonts/SFPro-Bold.ttf", 400)
    except:
        font = ImageFont.load_default()
    
    draw.text((512, 512), "F", font=font, fill='white', anchor="mm")
    
    # Save the image
    img.save('icons/friday.png')

if __name__ == "__main__":
    if not os.path.exists('icons'):
        os.makedirs('icons')
    create_base_icon()
