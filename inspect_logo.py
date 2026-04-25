from PIL import Image
import numpy as np

# Load both logos and compare
orig = Image.open('/home/ubuntu/printprosg/img/logo-transparent.png').convert('RGBA')
white = Image.open('/home/ubuntu/printprosg/img/logo-white.png').convert('RGBA')

print(f"Transparent logo size: {orig.size}")
print(f"White logo size: {white.size}")

# Check pixel values in the "P" region (left side of image)
# The "P" in "Print" starts at approximately x=10-50, y=10-100
orig_data = np.array(orig)
white_data = np.array(white)

# Sample some pixels in the P area
print("\nSample pixels in 'P' area (x=10-60, y=20-80) - orig:")
for y in [30, 50, 70]:
    for x in [15, 25, 35, 45]:
        r,g,b,a = orig_data[y,x]
        if a > 10:
            print(f"  ({x},{y}): R={r} G={g} B={b} A={a}")

print("\nSample pixels in 'P' area (x=10-60, y=20-80) - white:")
for y in [30, 50, 70]:
    for x in [15, 25, 35, 45]:
        r,g,b,a = white_data[y,x]
        if a > 10:
            print(f"  ({x},{y}): R={r} G={g} B={b} A={a}")

# Count dark pixels in orig vs white pixels in white logo
orig_dark = np.sum((orig_data[:,:,0] < 100) & (orig_data[:,:,1] < 100) & (orig_data[:,:,2] < 100) & (orig_data[:,:,3] > 50))
white_bright = np.sum((white_data[:,:,0] > 200) & (white_data[:,:,1] > 200) & (white_data[:,:,2] > 200) & (white_data[:,:,3] > 50))

print(f"\nDark pixels in original: {orig_dark}")
print(f"White pixels in white logo: {white_bright}")

# Check if there are semi-transparent/grey pixels that should be white
grey_pixels = np.sum((white_data[:,:,0] > 50) & (white_data[:,:,0] < 200) & (white_data[:,:,3] > 50) & 
                     (white_data[:,:,1] < 100) & (white_data[:,:,2] < 100))
print(f"Grey/semi-dark pixels in white logo (should be white): {grey_pixels}")
