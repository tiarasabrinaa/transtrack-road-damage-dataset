import requests
import os
import json

json_file_path = './scraping_data/280126.json'
download_folder = './results'

os.makedirs(download_folder, exist_ok=True)

with open(json_file_path, 'r') as file:
    response_data = json.load(file)

alarm_list = response_data.get('data', {}).get('list', [])

for alarm in alarm_list:
    device_id = alarm.get('deviceID', 'unknown')
    alarm_time = alarm.get('alarmTime', 'unknown')
    alarm_type = alarm.get('alarmTypeValue', 'unknown')
    
    alarm_files = alarm.get('alarmFile', [])
    for file_entry in alarm_files:
        if file_entry.get('fileType') == '4':
            continue
        
        download_url = file_entry.get('downUrl')
        
        
        if 'dn=' in download_url:
            file_name = download_url.split('dn=')[-1]
        else:
            file_type = 'jpg' if file_entry.get('fileType') == '4' else 'mp4'
            file_name = f"{device_id}_{alarm_time.replace(' ', '_').replace(':', '-')}_{file_entry.get('channel', 0)}.{file_type}"
        
        print(f"Downloading: {file_name} ({alarm_type})")
        
        try:
            response = requests.get(download_url, timeout=30)
            
            if response.status_code == 200:
                file_path = os.path.join(download_folder, file_name)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {file_name}")
            else:
                print(f"Failed to download {file_name}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Network error downloading {file_name}: {str(e)[:100]}")
            continue

print("\nAll files processed.")
