# YouTube History Converter for YT re:Watch

A Python script that converts YouTube history (exported via Google Takeout as JSON) into a format that YT re:Watch can understand.

## What You'll Need:
1. **Python** installed on your computer
2. Your **YouTube history** exported from Google Takeout in JSON format (file name: `watch-history.json`)
3. The **YT re:Watch Extension** installed in your browser (Make sure you have it set up and ready to go)
4. The **`youtube_history_convert.py`** script from this repository (for converting the history file)

## Installation

### Step 1: Download Your YouTube History
1. Go to [Google Takeout](https://takeout.google.com/).
2. Select **YouTube and YouTube Music** as the data you want to download.
3. **Important:** When choosing data, **only select History** (ensure "All YouTube data included" is **not** selected, as you only need history data).
4. Choose **JSON format** for the export file type.
5. Click **Next** and download the file once it’s ready. This will be your `watch-history.json`.

### Step 2: Download the Python Script
1. Download the **`youtube_history_convert.py`** script from this repository.

### Step 3: Place Files in the Same Folder
1. Put the downloaded **`watch-history.json`** file (your YouTube history) and the **`youtube_history_convert.py`** script into the same folder.

### Step 4: Run the Script
1. Double-click on **`youtube_history_convert.py`** to run the script.
2. The script will automatically create a new file called **`yt_rewatch_import.json`** in the same folder.

## Usage

### Step 5: Import to YT re:Watch
1. After the script finishes, the file **`yt_rewatch_import.json`** will be generated.
2. Open the **YT re:Watch Extension** in your browser.
3. Import the **`yt_rewatch_import.json`** file into YT re:Watch
