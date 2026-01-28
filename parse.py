import requests
import os
import json

date_scrape = '270126'

json_file_path = f'./scraping_data/{date_scrape}.json'
download_folder = f'./results/{date_scrape}/'

os.makedirs(download_folder, exist_ok=True)

with open(json_file_path, 'r') as file:
    response_data = json.load(file)

alarm_list = response_data.get('data', {}).get('list', [])

total_mp4_files = 0
downloaded_success = 0
downloaded_failed = 0
skipped_jpg = 0

for alarm in alarm_list:
    device_id = alarm.get('deviceID', 'unknown')
    alarm_time = alarm.get('alarmTime', 'unknown')
    alarm_type = alarm.get('alarmTypeValue', 'unknown')
    
    alarm_files = alarm.get('alarmFile', [])
    for file_entry in alarm_files:
        if file_entry.get('fileType') == '4':
            skipped_jpg += 1
            continue
        
        total_mp4_files += 1
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
                downloaded_success += 1
                print(f"Downloaded: {file_name}")
            else:
                downloaded_failed += 1
                print(f"Failed to download {file_name}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            downloaded_failed += 1
            print(f"Network error downloading {file_name}: {str(e)[:100]}")
            continue

print("\n" + "="*60)
print("DOWNLOAD SUMMARY")
print("="*60)
print(f"Total MP4 files found: {total_mp4_files}")
print(f"Successfully downloaded: {downloaded_success}")
print(f"Failed to download: {downloaded_failed}")
print(f"JPG files skipped: {skipped_jpg}")
print(f"Success rate: {(downloaded_success/total_mp4_files*100) if total_mp4_files > 0 else 0:.1f}%")
print("="*60)
