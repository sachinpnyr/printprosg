from PIL import Image
import numpy as np

# Load the transparent logo
img = Image.open('/home/ubuntu/printprosg/img/logo-transparent.png').convert('RGBA')
data = np.array(img, dtype=np.float32)

r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

# Identify "text" pixels: greyscale (R≈G≈B) and opaque
# These are the dark text and its anti-aliasing (grey edges)
grey_diff = (np.abs(r - g) < 20) & (np.abs(g - b) < 20) & (np.abs(r - b) < 20)
opaque = a > 30

# Text pixels = greyscale + opaque
text_mask = grey_diff & opaque

# For text pixels: invert the grey value to white
# Dark pixel (value=50) -> bright white (255)
# Grey anti-alias (value=200) -> near-white (255) with adjusted alpha
# The trick: set RGB to 255, and set alpha proportional to how dark the pixel was
# alpha_new = alpha * (1 - brightness/255)  -- darker pixels = more opaque white

brightness = (r + g + b) / 3.0  # 0=black, 255=white

# For text pixels: make them white with alpha based on darkness
# A pixel that was R=50 (dark) -> very opaque white
# A pixel that was R=200 (light grey, anti-alias) -> semi-transparent white
new_alpha = a * (1.0 - brightness / 255.0) * 3.5  # amplify
new_alpha = np.clip(new_alpha, 0, 255)

result = data.copy()
result[text_mask, 0] = 255  # R -> white
result[text_mask, 1] = 255  # G -> white
result[text_mask, 2] = 255  # B -> white
result[text_mask, 3] = new_alpha[text_mask]

# Non-text (coloured ink strokes) stay unchanged
result_img = Image.fromarray(result.astype(np.uint8))
result_img.save('/home/ubuntu/printprosg/img/logo-white.png')
print(f"Saved improved logo-white.png: {result_img.size}")

# Verify: check the P area pixels
result_data = np.array(result_img)
print("\nFixed white logo - P area pixels (x=10-60, y=20-80):")
for y in [30, 50, 70, 90]:
    for x in [15, 25, 35, 45]:
        r2,g2,b2,a2 = result_data[y,x]
        if a2 > 10:
            print(f"  ({x},{y}): R={r2} G={g2} B={b2} A={a2}")
