from PIL import Image
import os

try:
    # ----- Settings Icon -----
    img = Image.open("settings_icon.ico")

    img.size = max(img.info.get("sizes", {img.size}))

    img.save("settings_icon.png", "PNG")
    img.save("settings_icon_128.ico", format="ICO")
    print("Success: Generated settings_icon.png and settings_icon_128.ico from settings_icon.ico!")
except Exception as e:
    print(f"Error processing image: {e}")