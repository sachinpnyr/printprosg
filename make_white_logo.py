from PIL import Image
import numpy as np

# Load the transparent logo
img = Image.open('/home/ubuntu/printprosg/img/logo-transparent.png').convert('RGBA')
data = np.array(img)

# Make a white-text version:
# - Dark pixels (the "Print Pr" text, R<100, G<100, B<100) -> white
# - Coloured pixels (the ink strokes) -> keep as-is
# - Transparent pixels -> keep transparent

r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

# Dark text pixels: low R, G, B and opaque
dark_text = (r < 100) & (g < 100) & (b < 100) & (a > 50)

# Make dark text white
data_white = data.copy()
data_white[dark_text, 0] = 255  # R
data_white[dark_text, 1] = 255  # G
data_white[dark_text, 2] = 255  # B

result = Image.fromarray(data_white)
result.save('/home/ubuntu/printprosg/img/logo-white.png')
print(f"Saved logo-white.png: {result.size}")
