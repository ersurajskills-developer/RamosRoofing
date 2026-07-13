import os
from PIL import Image

input_path = r"C:\Users\Om Laxshmi Narayan\.gemini\antigravity-ide\brain\0bd0a70e-57b4-4663-8fe0-1d72da3719da\media__1783919218648.png"
output_path = r"r:\AI Website Development\Professional\RamosRoofing-main\RamosRoofing-main\Images\ramos-logo.webp"

try:
    with Image.open(input_path) as img:
        img.save(output_path, "WEBP", quality=90)
    print(f"Successfully converted and saved to {output_path}")
except Exception as e:
    print(f"Error: {e}")
