from PIL import Image
import pytesseract
import re
import math
import sys
import os

# Dynamically add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try importing now
from Eagle_Functions import *

# Load image
img = Image.open("tests/Gap_Up_Short 2025-04-27 at 22.38.51@2x.png")
width, height = img.size

# Crop right panel (right 50% of the image)
right_crop = img.crop((int(width * 0.55), 0, width, height))

# Run OCR on the cropped image
ocr_text = pytesseract.image_to_string(right_crop, config='--psm 6')

# Print OCR results for reference
print("Full OCR Text:\n", ocr_text)

#-----------------------------------------------------------------------------------------------------#

# Extract Volume and Gap Value using regex

# volume_match = re.search(r"Volume\s*([\d.]+)\s*M", ocr_text)

# gap_value_match = re.search(r"Gap Value\s*([\d.]+)\s*%", ocr_text)

# premarket_volume_match = re.search(r"Premarket Volume\s*([\d.,]+)\s*([KM]?)", ocr_text)

market_cap_match = re.search(r"Market Cap\s*\$?\s*([\d,.]+)\s*([MK]?)", ocr_text)

#-----------------------------------------------------------------------------------------------------#

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

if market_cap_match:
    print("Market Cap:", market_cap_match.group(1), market_cap_match.group(2))
else:
    print("❌ Market Cap not found.")


#-----------------------------------------------------------------------------------------------------#

# print(fetch_item_list('test'))
# process_premarket_volume(ocr_text, 'MA4YFRD2JHED3', ['test'])