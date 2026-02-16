from PIL import Image, ImageDraw, ImageFont
import os

# Define path
media_path = os.path.join(os.getcwd(), 'media', 'avatars')
os.makedirs(media_path, exist_ok=True)
file_path = os.path.join(media_path, 'default.png')

# Create image
size = (200, 200)
img = Image.new('RGB', size, color='#cbd5e1') # Slate-300 background

# Draw
d = ImageDraw.Draw(img)
# Draw a circle for head
d.ellipse([50, 20, 150, 120], fill='white')
# Draw a semi-circle for body
d.chord([20, 130, 180, 280], start=180, end=0, fill='white')

# Save
img.save(file_path)
print(f"Created default avatar at {file_path}")
