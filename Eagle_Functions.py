import requests
import json
import re
import math

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
        print("📈 Gap Value:", gap_value_match.group(1), "%")
        gap_value = float(gap_value_match.group(1))
        gap_value = math.floor(gap_value)

        tag = get_gap_tag(gap_value)
        update_item_tags(id, tag, item_tags)
    else:
        print("❌ Gap Value not found.")
        update_item_tags(id, "no_gap_data", item_tags)

#--------------------------------------------------------------------------------------------------------------------#

# Function that processes the premarket volume 

def process_premarket_volume(ocr_text, id, item_tags):
    # Extract Premarket Volume using regex
    premarket_volume_match = re.search(r"Premarket Volume\s*([\d.,]+)\s*([KM]?)", ocr_text)

    if premarket_volume_match:
        print("📈 Premarket Volume:", premarket_volume_match.group(1), premarket_volume_match.group(2))
        premarket_volume = float(premarket_volume_match.group(1)) # group(1) of the match would be the number of the volume
        premarket_volume = math.floor(premarket_volume)
        volume_scale = premarket_volume_match.group(2) # group(2) of the match would be 'K' or 'M' of the volume

        tag = get_premarket_volume_tag(premarket_volume, volume_scale)
       
        update_item_tags(id, tag, item_tags)
    else:
        print("❌ Premarket Volume not found.")
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


