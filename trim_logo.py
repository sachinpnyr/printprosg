from PIL import Image
import numpy as np

# Load the original logo (white background, RGB)
img = Image.open('/home/ubuntu/printprosg/img/logo-original.png').convert('RGBA')
data = np.array(img)

# Find non-white pixels (white = R>240, G>240, B>240)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_mask = (r > 240) & (g > 240) & (b > 240)

# Make white pixels transparent
data[:,:,3] = np.where(white_mask, 0, 255)

# Crop to content bounding box
result = Image.fromarray(data)
bbox = result.getbbox()
print(f"Bounding box: {bbox}")
cropped = result.crop(bbox)
print(f"Cropped size: {cropped.size}")

# Save as transparent PNG
cropped.save('/home/ubuntu/printprosg/img/logo.png')
print("Saved logo.png (transparent)")

# Also save a version with some padding
padded = Image.new('RGBA', (cropped.width + 20, cropped.height + 20), (0,0,0,0))
padded.paste(cropped, (10, 10))
padded.save('/home/ubuntu/printprosg/img/logo-transparent.png')
print(f"Saved logo-transparent.png: {padded.size}")
