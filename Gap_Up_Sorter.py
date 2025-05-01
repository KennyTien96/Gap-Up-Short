from PIL import Image
from Eagle_Functions import *
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pytesseract
import requests
import os
import time

load_dotenv()
folder_path = os.getenv("FOLDER_PATH")

def process_item(item):
    id = item['id']
    name = item['name']
    item_tags = item['tags']

    try:
        filename = name + ".png"
        full_path = os.path.join(folder_path, filename)

        img = Image.open(full_path)
        width, height = img.size
        right_crop = img.crop((int(width * 0.55), 0, width, height))

        ocr_text = pytesseract.image_to_string(right_crop, config='--psm 6')

        process_gap_value(ocr_text, id, item_tags)
        # process_premarket_volume(ocr_text, id, item_tags)

    except Exception as e:
        print(f"❌ Error processing {name}: {e}")

def main():
    try:
        items = fetch_all_items_excluding_partial_tag('gap')
        total_count = len(items)
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=6) as executor:
            list(tqdm(executor.map(process_item, items), total=total_count, desc="🔄 Processing"))

        elapsed_time = time.time() - start_time
        print(f"\n✅ Completed processing {total_count} items in {elapsed_time:.2f} seconds.")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
