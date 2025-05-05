from PIL import Image
import pytesseract
import re
import math
import sys
import os
import cv2

#-----------------------------------------------------------------------------------------------#

# Dynamically add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try importing now
from Eagle_Functions import *
from Gap_Up_Sorter import *

#-----------------------------------------------------------------------------------------------#

# Load image
img_path = "tests/Gap_Up_Short 2025-04-28 at 08.44.43@2x.png" 

img = Image.open(img_path)
width, height = img.size

# Crop right panel (right 50% of the image)
right_crop = img.crop((int(width * 0.10), 0, width, height))

# Run OCR on the cropped image
ocr_text = pytesseract.image_to_string(right_crop, config='--psm 3')

# Print OCR results for reference
print("Full OCR Text:\n", ocr_text)

#-----------------------------------------------------------------------------------------------#

# Extract Volume and Gap Value using regex

# volume_match = re.search(r"Volume\s*([\d.]+)\s*M", ocr_text)
# gap_value_match = re.search(r"Gap Value\s*([\d.]+)\s*%", ocr_text)
# premarket_volume_match = re.search(r"Premarket Volume\s*([\d.,]+)\s*([KM]?)", ocr_text)

#-----------------------------------------------------------------------------------------------#

# Output results

# if volume_match:
#     print("📊 Volume:", volume_match.group(1), "M")
# else:
#     print("❌ Volume not found.")

# if gap_value_match:
#     print("📈 Gap Value:", gap_value_match.group(1), "%")
# else:
#     print("❌ Gap Value not found.")

# if premarket_volume_match:
#     # premarket_volume = float(premarket_volume_match.group(1))
#     # premarket_volume = math.floor(premarket_volume)
#     print("📊 Premarket Volume:", premarket_volume_match.group(1))

# else:
#     print("❌ Premarket Volume not found.")

#-----------------------------------------------------------------------------------------------#

# print(fetch_item_list('test'))
# process_premarket_volume(ocr_text, 'MA4YFRD2JHED3', ['test'])

#-----------------------------------------------------------------------------------------------#