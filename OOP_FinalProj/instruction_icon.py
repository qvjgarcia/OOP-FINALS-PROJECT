from PIL import Image
import os

try:
    # ----- Instructions Icon -----
    img = Image.open("instructions_icon.ico")

    img.size = max(img.info.get("sizes", {img.size}))

    img.save("instructions_icon.png", "PNG")
    img.save("instructions_icon_128.ico", format="ICO")
    print("Success: Generated instructions_icon.png and instructions_icon_128.ico from instructions_icon.ico!")
except Exception as e:
    print(f"Error processing image: {e}")