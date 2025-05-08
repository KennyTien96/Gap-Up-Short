from PIL import Image
from Eagle_Functions import *
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pytesseract
import requests
import os
import time
import threading

load_dotenv()
folder_path = os.getenv("FOLDER_PATH")

def process_item(item, total_count, progress_bar):
    id = item['id']
    name = item['name']
    item_tags = item['tags']

    try:
        # Loading and processing image through OCR 
        filename = name + ".png"
        full_path = os.path.join(folder_path, filename)

        img = Image.open(full_path)
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
        ocr_text = pytesseract.image_to_string(cropped_img, config='--psm 7')
        #-----------------------------------------------------------------------------------#

        # Add process function for desired tag here :

        # process_gap_value(ocr_text, id, item_tags)

        # process_premarket_volume(ocr_text, id, item_tags)

        # process_market_cap(ocr_text, id, item_tags)

        process_stock_symbol(ocr_text, id, item_tags)

        #-----------------------------------------------------------------------------------#

        progress_bar.set_postfix({"Processing": f"{progress_bar.n}/{total_count}"})
        progress_bar.update(1)

    except Exception as e:
        print(f"❌ Error processing {name}: {e}")
        progress_bar.update(1)

def main():
    try:
        items = fetch_all_items_excluding_partial_tag('MC') # <----- Update string to whatever tag you want filtered out when fetching list
        total_count = len(items)
        start_time = time.time()

        # Set up the tqdm lock for thread safety
        tqdm.set_lock(threading.Lock())

        with tqdm(total=total_count, desc="Processing Items", ncols=100, position=0, dynamic_ncols=True) as progress_bar:
            with ThreadPoolExecutor(max_workers=6) as executor:
                for count, item in enumerate(items, 1):
                    executor.submit(process_item, item, total_count, progress_bar)

        elapsed_time = time.time() - start_time
        print(f"\n✅ Completed processing {total_count} items in {elapsed_time:.2f} seconds.")

    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
