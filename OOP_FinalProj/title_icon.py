from PIL import Image
import os

try:
    # ----- PicklePlay Title Icon -----
    img = Image.open("pickleball1.jpg").convert("RGBA")
    
    img = img.resize((128, 128), Image.Resampling.LANCZOS)
    
    img.save("pickleball_icon.png", "PNG")
    img.save("pickleball_icon.ico", format="ICO")
    print("Success: Generated pickleball_icon.png and pickleball_icon.ico from pickleball1.jpg!")
except Exception as e:
    print(f"Error processing image: {e}")
