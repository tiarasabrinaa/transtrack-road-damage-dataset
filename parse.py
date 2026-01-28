import requests
import os
import json

json_file_path = './scraping_data/280126.json'
download_folder = './results'

os.makedirs(download_folder, exist_ok=True)

with open(json_file_path, 'r') as file:
    response_data = json.load(file)

for entry in response_data:
    download_url = entry['downUrl']
    file_name = entry['fileName']
    
    response = requests.get(download_url)
    
    if response.status_code == 200:
        file_path = os.path.join(download_folder, file_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_name}")
    else:
        print(f"Failed to download {file_name}. Status code: {response.status_code}")

print("All files downloaded.")
