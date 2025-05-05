import requests
import json
import re
import math
import cv2
import numpy as np
import pytesseract
import os
from PIL import Image

#--------------------------------------------------------------------------------------------------------------------#

# Eagle API call that gets list of all items

def fetch_item_list(tags=None):
    url = "http://localhost:41595/api/item/list"
    params = {
        "limit": 20,
    }

    if tags is not None:
        params["tags"] = tags

    try:
        response = requests.get(url, params=params, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        return data['data']  # Return the list of items if needed
    
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    
#--------------------------------------------------------------------------------------------------------------------#

# Eagle API call that gets list of all the items excluding the tags

def fetch_all_items_excluding_partial_tag(exclude_substring):
    url = "http://localhost:41595/api/item/list"
    limit = 200
    offset = 0
    all_items = []

    while True:
        params = {
            "limit": limit,
            "offset": offset
        }

        try:
            response = requests.get(url, params=params, allow_redirects=True)
            response.raise_for_status()
            data = response.json().get('data', [])

            if not data:
                break

            # Exclude items where any tag contains the substring 
            filtered_data = [
                item for item in data
                if not any(exclude_substring in tag for tag in item.get('tags', []))
            ]
            all_items.extend(filtered_data)

            offset += 1  # Go to the next batch

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            break

    return all_items

#--------------------------------------------------------------------------------------------------------------------#

# Function that processes the gap value

def process_gap_value(ocr_text, id, item_tags):
    # Extract Gap Value using regex
    gap_value_match = re.search(r"Gap Value\s*([\d.]+)\s*%", ocr_text)

    if gap_value_match:
        print("Gap Value:", gap_value_match.group(1), "%")
        gap_value = float(gap_value_match.group(1))
        gap_value = math.floor(gap_value)

        tag = get_gap_tag(gap_value)
        update_item_tags(id, tag, item_tags)
    else:
        update_item_tags(id, "no_gap_data", item_tags)

#--------------------------------------------------------------------------------------------------------------------#

# Function that processes the premarket volume 

def process_premarket_volume(ocr_text, id, item_tags):
    # Extract Premarket Volume using regex
    premarket_volume_match = re.search(r"Premarket Volume\s*([\d.,]+)\s*([KM]?)", ocr_text)

    if premarket_volume_match:
        print("Premarket Volume:", premarket_volume_match.group(1), premarket_volume_match.group(2))
        premarket_volume = float(premarket_volume_match.group(1)) # group(1) of the match would be the number of the volume
        premarket_volume = math.floor(premarket_volume)
        volume_scale = premarket_volume_match.group(2) # group(2) of the match would be 'K' or 'M' of the volume

        tag = get_premarket_volume_tag(premarket_volume, volume_scale)
       
        update_item_tags(id, tag, item_tags)
    else:
        update_item_tags(id, "no_PMV_data", item_tags)

#--------------------------------------------------------------------------------------------------------------------#

# Eagle API call that will update/tag item

def update_item_tags(item_id, tags, item_tags):
    url = "http://localhost:41595/api/item/update"
    headers = {
        "Content-Type": "application/json"
    }
    item_tags.append(tags)
    data = {
        "id": item_id,
        "tags": item_tags
    }

    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        data = result['data']
        print("✅ Update successful:", f"ID: {data['id']}, Name: {data['name']}, Tags: {data.get('tags', [])}")
        return result
    except requests.exceptions.RequestException as e:
        print("❌ Error updating item:", e)
        return None

#--------------------------------------------------------------------------------------------------------------------#

# Function that loops through gap values and tags it

def get_gap_tag(gap_value):
    ranges = [
        (40, 49, "gap_40"),
        (50, 59, "gap_50"),
        (60, 69, "gap_60"),
        (70, 79, "gap_70"),
        (80, 89, "gap_80"),
        (90, 99, "gap_90"),
        (100, 150, "gap_100_150"),
        (151, 200, "gap_150_200"),
        (201, float("inf"), "gap_200+"),
    ]
    
    for lower, upper, tag in ranges:
        if lower <= gap_value <= upper:
            return tag
    return "no_gap_data"

#--------------------------------------------------------------------------------------------------------------------#

# Function that loops through premarket volume values and tags it

def get_premarket_volume_tag(premarket_volume, volume_scale):
    ranges = [
        (1, 5, "PMV 1-5 M"),
        (6, 10, "PMV 6-10 M"),
        (11, 15, "PMV 11-15 M"),
        (16, 20, "PMV 16-20 M"),     
        (21, 25, "PMV 21-25 M"),
        (26, 30, "PMV 26-30 M"),
        (31, float("inf"), "PMV 31+"),
    ]
    if volume_scale == 'K':
        return 'PMV < 1M'
        
    for lower, upper, tag in ranges:
        if lower <= premarket_volume <= upper:
            return tag
        
    return "no_PMV_data"

#--------------------------------------------------------------------------------------------------------------------#

# Function that loops through premarket volume values and tags it

def get_price_open_tag(price_open):
    ranges = [
        (0, 1, "Price < 1"),
        (1, 2, "Price 1-2"),
        (2, 3, "Price 2-3"),
        (3, 5, "Price 3-5"),     
        (5, 7, "Price 5-7"),
        (7, 10, "Price 7-10"),
        (10, float("inf"), "Price 10+"),
    ]
        
    for lower, upper, tag in ranges:
        if lower <= price_open <= upper:
            return tag
        
    return "recheck_price_open_data"

#--------------------------------------------------------------------------------------------------------------------#

# Yellow color processing

def yellow_processing(image):

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define yellow range
    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([40, 255, 255])

    # Mask for yellow regions
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_region = cv2.bitwise_and(image, image, mask=mask)

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(yellow_region, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Invert the image to make text dark on light background
    # inverted = 255 - thresh

    # Optional: Find contours and crop around the yellow box
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest contour is the yellow box
    if contours:
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)
        cropped = image[y:y+h, x:x+w]
        
        # Convert cropped area to PIL image for OCR
        pil_cropped = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

        # OCR with relaxed config (for single line of text)
        text = pytesseract.image_to_string(pil_cropped, config='--psm 7')
        print("Open Price:", text.strip())
        return text.strip()
    else:
        print("No yellow box found.")

#--------------------------------------------------------------------------------------------------------------------#

# Function that process price open value 

def process_price_open(img_path, id, item_tags):
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError(f"Could not load image from path: {img_path}")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define yellow range
    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([40, 255, 255])

    # Mask for yellow regions
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    yellow_region = cv2.bitwise_and(image, image, mask=mask)

    # Retrieving price from the yellow region
    price = yellow_processing(yellow_region)

    try:
        price_value = float(price)
        tag = get_price_open_tag(price_value)
        update_item_tags(id, tag, item_tags)
    except ValueError:
        print(f"Cannot convert '{price}' to an integer.")
        update_item_tags(id, "no_price_open_data", item_tags)


#--------------------------------------------------------------------------------------------------------------------#

# All Yellow Processing Functions

def load_image(path):
    return cv2.imread(path)

def find_yellow_regions(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 100, 150])
    upper_yellow = np.array([35, 255, 255])
    return cv2.inRange(hsv, lower_yellow, upper_yellow)

def extract_yellow_boxes(image, mask, min_area=200):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > min_area:
            boxes.append(image[y:y+h, x:x+w])
    return boxes

def enhance_for_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
    enhanced = clahe.apply(gray)
    
    binary = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY)[1]
    inverted = cv2.threshold(enhanced, 180, 255, cv2.THRESH_BINARY_INV)[1]
    
    resized_binary = cv2.resize(binary, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    resized_inverted = cv2.resize(inverted, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
    
    return resized_binary, resized_inverted

def extract_text_from_boxes(boxes, debug_dir="debug_crops"):
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    for i, box in enumerate(boxes):
        binary, inverted = enhance_for_ocr(box)
        cv2.imwrite(f"{debug_dir}/box_{i}_binary.png", binary)
        cv2.imwrite(f"{debug_dir}/box_{i}_inverted.png", inverted)

        for version_name, img in [("binary", binary), ("inverted", inverted)]:
            text = pytesseract.image_to_string(img, config='--psm 6 -c tessedit_char_whitelist=0123456789.')
            cleaned = re.findall(r"\d+\.\d+", text)
            if cleaned:
                # print(f"[OCR Success] Box {i} ({version_name}):", cleaned[0])
                return cleaned[0]
            # else:
            #     print(f"[OCR Fail] Box {i} ({version_name}):", repr(text.strip()))
    return None

def extract_yellow_price_from_image(path, id, item_tags):
    image = load_image(path)
    yellow_mask = find_yellow_regions(image)
    yellow_boxes = extract_yellow_boxes(image, yellow_mask)
    if not yellow_boxes:
        print("No yellow boxes found.")
        return None
    value = extract_text_from_boxes(yellow_boxes)
    if value is not None:
        price_value = float(value)
        tag = get_price_open_tag(price_value)
        update_item_tags(id, tag, item_tags)
    else:
        print(f"No value found")
        update_item_tags(id, "recheck_Price_open_data", item_tags)


