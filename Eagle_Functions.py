import requests
import json

# Eagle API call that gets list of all items
def fetch_item_list():
    url = "http://localhost:41595/api/item/list"
    params = {
        "limit": 20
    }

    try:
        response = requests.get(url, params=params, allow_redirects=True)
        response.raise_for_status()
        data = response.json()
        return data['data']  # Return the list of items if needed
    
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Eagle API call that will update/tag item
def update_item_tags(item_id, tags):
    url = "http://localhost:41595/api/item/update"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "id": item_id,
        "tags": [tags]
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

