import requests
import json

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