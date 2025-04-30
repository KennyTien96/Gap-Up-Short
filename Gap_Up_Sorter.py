from PIL import Image
import pytesseract
import re

# Load image
img = Image.open("CleanShot 2025-04-11 at 10.00.24@2x.png")
width, height = img.size

# Crop right panel (right 50% of the image)
right_crop = img.crop((int(width * 0.55), 0, width, height))

# Run OCR on the cropped image
ocr_text = pytesseract.image_to_string(right_crop, config='--psm 3')

# Print OCR results for reference
print("Full OCR Text:\n", ocr_text)

# Extract Volume and Gap Value using regex
volume_match = re.search(r"Volume\s*([\d.]+)\s*M", ocr_text)
gap_value_match = re.search(r"Gap Value\s*([\d.]+)\s*%", ocr_text)

# Output results
if volume_match:
    print("📊 Volume:", volume_match.group(1), "M")
else:
    print("❌ Volume not found.")

if gap_value_match:
    print("📈 Gap Value:", gap_value_match.group(1), "%")
else:
    print("❌ Gap Value not found.")
