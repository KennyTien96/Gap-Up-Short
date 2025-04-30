import requests
import json

#-----------------------------------------------------------------------------------------------#

# Getting the info of Eagle app

# try:
#     response = requests.get("http://localhost:41595/api/application/info")
#     data = response.json()
#     print(data)
# except Exception as e:
#     print("Error:", e)

#-----------------------------------------------------------------------------------------------#

# Getting the info of current Eagle library

# try:
#     response = requests.get("http://localhost:41595/api/library/info")
#     result = response.json()
#     print(result)
# except Exception as error:
#     print("Error:", error)

#-----------------------------------------------------------------------------------------------#

# Getting the list of all images in Eagle library

url = "http://localhost:41595/api/item/list"
params = {
    "limit": 200,
    "offset": 0  
}

try:
    response = requests.get(url, params=params, allow_redirects=True)
    response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
    data = response.json()
    # Extract and print only ID and name
    for idx, item in enumerate(data['data'], start=1):
        print(f"{idx}. ID: {item['id']}, Name: {item['name']}, Tags: {item['tags']}")
except requests.exceptions.RequestException as e:
    print("Error:", e)


#-----------------------------------------------------------------------------------------------#

# Updating image

# url = "http://localhost:41595/api/item/update"

# data = {
#     "id": "MA389GJA4DAMZ",
#     "tags": ["Design1", "Design2"]
# }

# headers = {
#     "Content-Type": "application/json"
# }

# try:
#     response = requests.post(url, data=json.dumps(data), headers=headers, allow_redirects=True)
#     response.raise_for_status()
#     result = response.json()
#     print(result)
# except requests.exceptions.RequestException as e:
#     print("Error:", e)

#-----------------------------------------------------------------------------------------------#

# Getting list of folders

# url = "http://localhost:41595/api/folder/list"

# try:
#     response = requests.get(url, allow_redirects=True)
#     response.raise_for_status()  # Raise an exception for HTTP errors
#     result = response.json()
#     print(result)
# except requests.exceptions.RequestException as error:
#     print("error", error)