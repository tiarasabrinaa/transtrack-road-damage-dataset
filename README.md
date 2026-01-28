# TransTrack Road Damage Dataset

A Python script to download MDVR (Mobile Digital Video Recorder) alarm video files from TransTrack's fleet management system. This tool parses JSON alarm data and downloads associated MP4 video files for analysis and documentation.

## Features

- 📹 Downloads MP4 video files from TransTrack alarm records
- 🚫 Automatically skips JPG image files
- 📊 Provides detailed download statistics
- ⚡ Handles network errors gracefully with timeout protection
- 📁 Organizes downloads by date

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/tiarasabrinaa/-transtrack-road-damage-dataset.git
cd transtrack
```

2. Install required dependencies:
```bash
pip install requests
```

## Usage

### 1. Prepare Your Data

Place your JSON data file in the `scraping_data/` directory with the format `DDMMYY.json`:
```
scraping_data/
  └── 280126.json  # Example: January 28, 2026
```

### 2. Configure the Date

Edit `parse.py` and set the `date_scrape` variable to match your JSON filename:
```python
date_scrape = '280126'  # Format: DDMMYY
```

### 3. Run the Script

Execute the download script:
```bash
python parse.py
```

### 4. Check Results

Downloaded MP4 files will be saved in:
```
results/
  └── 280126/
      ├── video1.mp4
      ├── video2.mp4
      └── ...
```

## JSON Data Structure

The script expects JSON data in the following format:
```json
{
  "status": 10000,
  "msg": "Success",
  "data": {
    "list": [
      {
        "deviceID": "867395078096688",
        "deviceName": "H632",
        "alarmType": "102",
        "alarmTypeValue": "Lane Departure Warning",
        "alarmTime": "2026-01-28 22:13:15",
        "alarmFile": [
          {
            "fileType": "2",
            "downUrl": "https://...",
            "channel": 1
          }
        ]
      }
    ]
  }
}
```

### File Types
- `fileType: "2"` - MP4 video files (downloaded)
- `fileType: "4"` - JPG image files (skipped)

## Output Summary

After execution, the script displays a summary:
```
============================================================
DOWNLOAD SUMMARY
============================================================
Total MP4 files found: 50
Successfully downloaded: 45
Failed to download: 5
JPG files skipped: 50
Success rate: 90.0%
============================================================
```

## Alarm Types

Common alarm types in TransTrack system:
- Lane Departure Warning (102)
- Headway Monitoring Warning
- Forward Collision Warning
- Driver Fatigue Detection
- And more...

## Error Handling

The script handles various errors:
- **Network timeouts**: 30-second timeout for each download
- **Connection errors**: Continues with next file if one fails
- **HTTP errors**: Logs status codes for failed downloads

## Troubleshooting

### No files downloaded
- Verify JSON file exists in `scraping_data/` directory
- Check that `date_scrape` variable matches your JSON filename
- Ensure network connectivity to TransTrack servers

### Partial downloads
- Check the download summary for failed file counts
- Network issues may cause some files to fail - rerun the script to retry
- Failed downloads are logged with error messages

### Connection timeouts
- TransTrack servers may rate-limit requests
- Wait a few minutes and retry
- Consider adding delays between downloads if needed

## Project Structure

```
transtrack/
├── parse.py              # Main download script
├── scraping_data/        # Input JSON files
│   └── 280126.json
├── results/              # Downloaded video files
│   └── 280126/
├── .gitignore
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is for research and documentation purposes.

## Acknowledgments

- TransTrack Fleet Management System
- MDVR Technology Platform
