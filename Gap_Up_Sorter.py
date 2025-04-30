from PIL import Image
from Eagle_Functions import *
import pytesseract
import re
import requests
import os

folder_path = r"C:\Users\Game-Rm\Downloads\GUS copy unsorted\GUS copy unsorted"

try:
    items = fetch_item_list()

    # Extract and print only ID and name
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. ID: {item['id']}, Name: {item['name']}")
        id = item['id']

        # Load image
        filename = item['name'] + ".png"

        # Join the path and filename
        full_path = os.path.join(folder_path, filename)

        # Open the image
        img = Image.open(full_path)
        width, height = img.size

        # Crop right panel (right 50% of the image)
        right_crop = img.crop((int(width * 0.55), 0, width, height))

        # Run OCR on the cropped image
        ocr_text = pytesseract.image_to_string(right_crop, config='--psm 3')

        # Print OCR results for reference
        # print("Full OCR Text:\n", ocr_text)

        # Extract Gap Value using regex
        gap_value_match = re.search(r"Gap Value\s*([\d.]+)\s*%", ocr_text)

        # Output results
        if gap_value_match:
            print("📈 Gap Value:", gap_value_match.group(1), "%")
            gap_value = float(gap_value_match.group(1))
            
            tag = get_gap_tag(gap_value)
            update_item_tags(id, tag)
        else:
            print("❌ Gap Value not found.")

except requests.exceptions.RequestException as e:
    print("Error:", e)







