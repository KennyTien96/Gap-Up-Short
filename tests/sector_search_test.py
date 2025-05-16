from PIL import Image
import pytesseract
import sys
import os
import yfinance as yf

# Dynamically add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Try importing now
from Eagle_Functions import *

# Load image
img = Image.open(r"C:\Users\Game-Rm\Downloads\GUS copy unsorted\GUS copy unsorted\Gap_Up_Short 2025-04-24 at 09.06.38@2x.png")
width, height = img.size

# Define the crop box for the top left portion that includes "$ONCO"
# This will be an approximate region (tweak as needed)
left = 0
top = 0
right = int(width * 0.25)
bottom = int(height * 0.08)

# Perform the crop
cropped_img = img.crop((left, top, right, bottom))
# cropped_img.show()

# Run OCR on the cropped image
ocr_text = pytesseract.image_to_string(cropped_img, config='--psm 7') #psm 3 for premarket volume and gap value processing, psm 6 for market cap processing, psm7 for stock search

# Print OCR results for reference
print("Full OCR Text:\n", ocr_text)

#-----------------------------------------------------------------------------------------------------#

# Extract symbol using regex

symbol_match = re.search(r'\bS(\w+)\b', ocr_text)

#-----------------------------------------------------------------------------------------------------#

# Output results

if symbol_match:
    print("Symbol:", symbol_match.group(1))
else:
    print("❌ Symbol not found.")

#-----------------------------------------------------------------------------------------------------#
symbols = [symbol_match.group(1)]

for symbol in symbols:
    stock = yf.Ticker(symbol)
    info = stock.info
    # print(f"{symbol} - Sector: {info.get('sector')}, Industry: {info.get('industry')}")
    print(f"{symbol} - Country: {info.get('country')}")
    print(info)