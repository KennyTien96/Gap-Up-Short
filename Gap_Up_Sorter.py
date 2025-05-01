from PIL import Image
from Eagle_Functions import *
from dotenv import load_dotenv
import pytesseract
import requests
import os


load_dotenv()
folder_path = os.getenv("FOLDER_PATH")

try:
    # items = fetch_item_list()
    items = fetch_all_items_excluding_partial_tag('gap') 

    # Extract and print only ID and name
    for idx, item in enumerate(items, start=1):
        id = item['id']
        name = item['name']
        item_tags = item['tags']
        print(f"{idx}. ID: {id}, Name: {name}")

        # Load image
        filename = name + ".png"

        # Join the path and filename
        full_path = os.path.join(folder_path, filename)

        # Open the image
        img = Image.open(full_path)
        width, height = img.size

        # Crop right panel (right 55% of the image)
        right_crop = img.crop((int(width * 0.55), 0, width, height))

        # Run OCR on the cropped image
        ocr_text = pytesseract.image_to_string(right_crop, config='--psm 3')

        # Print OCR results for reference
        # print("Full OCR Text:\n", ocr_text)

        # Processes gap value and updates item with appropriate tag
        process_gap_value(ocr_text, id, item_tags)

        # Processes premarket volume and updates item with appropriate tag
        # process_premarket_volume(ocr_text, id, item_tags)

except requests.exceptions.RequestException as e:
    print("Error:", e)







