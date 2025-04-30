from PIL import Image
from Eagle_Functions import *
import pytesseract
import re
import requests
import json
import os

# retrive the list of all images in Eagle library
url_list = "http://localhost:41595/api/item/list"
folder_path = r"C:\Users\Game-Rm\Downloads\GUS copy unsorted\GUS copy unsorted"
params = {
    "limit": 20
}
try:
    response = requests.get(url_list, params=params, allow_redirects=True)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
    data = response.json()
    # Extract and print only ID and name
    for idx, item in enumerate(data['data'], start=1):
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
            
            if 50 <= gap_value <= 59:   
                update_item_tags(id, "gap_50")
            elif 60 <= gap_value <= 69:   
                update_item_tags(id, "gap_60")   
            elif 70 <= gap_value <= 79:
                update_item_tags(id, "gap_70")
            elif 80 <= gap_value <= 89:
                update_item_tags(id, "gap_80")
            elif 90 <= gap_value <= 99:
                update_item_tags(id, "gap_90")
            elif 100 <= gap_value <= 150:
                update_item_tags(id, "gap_100_150")
            elif 151 <= gap_value <= 200:
                update_item_tags(id, "gap_150_200")
            elif 201 <= gap_value:
                update_item_tags(id, "gap_200+")
            else:
                update_item_tags(id, "no_gap_data")

        else:
            print("❌ Gap Value not found.")

except requests.exceptions.RequestException as e:
    print("Error:", e)







