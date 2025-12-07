#!/usr/bin/env python3
import json
import re
from datetime import datetime
import os
import sys

# === CONFIG ===
INPUT_FILENAME = "watch-history.json"
OUTPUT_FILENAME = "yt_rewatch_import.json"

# Determine path of script and input / output files
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, INPUT_FILENAME)
output_path = os.path.join(script_dir, OUTPUT_FILENAME)

if not os.path.exists(input_path):
    print(f"ERROR: '{input_path}' not found.")
    print("Make sure watch-history.json is in the same folder as this script.")
    sys.exit(1)

with open(input_path, 'r', encoding='utf-8') as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON: {e}")
        sys.exit(1)

print(f"Loaded {len(data)} entries from {INPUT_FILENAME}")

def get_video_id(url):
    match = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})(?:[&?]|$)', url)
    return match.group(1) if match else None

def iso_to_timestamp_ms(iso_str):
    # Expect ISO like "2023-08-01T12:34:56Z" or with timezone
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    except Exception:
        # fallback: try parsing without timezone
        dt = datetime.fromisoformat(iso_str)
    return int(dt.timestamp() * 1000)

history = []

for entry in data:
    url = entry.get("titleUrl")
    if not url or "watch?v=" not in url:
        continue

    vid = get_video_id(url)
    if not vid:
        continue

    raw_title = entry.get("title", "")
    title = raw_title.replace("Watched ", "", 1) if raw_title.startswith("Watched ") else raw_title
    timestamp = iso_to_timestamp_ms(entry.get("time", ""))

    # Channel / uploader
    channel_name = "Unknown"
    channel_id = ""
    subtitles = entry.get("subtitles")
    if subtitles and isinstance(subtitles, list) and len(subtitles) > 0:
        channel_name = subtitles[0].get("name", channel_name)
        ch_url = subtitles[0].get("url", "")
        # Some logic to guess channelId — but you may need to review/fix this yourself
        if "/channel/" in ch_url:
            channel_id = ch_url.split("/channel/")[-1]
        elif "@" in ch_url:
            channel_id = ch_url.split("@")[-1]
            channel_id = "@" + channel_id
        else:
            # fallback based on cleaned-up channel name
            cleaned = "".join(c.lower() for c in channel_name if c.isalnum())
            channel_id = "@" + cleaned[:20]

    # Estimate duration & watched time — you may adjust these heuristics
    is_short = ("short" in title.lower()) or (len(title) < 55)
    duration = 60.0 if is_short else 900.0
    watched = 55.0 if is_short else 810.0

    history.append({
        "videoId": vid,
        "title": title,
        "time": watched,
        "duration": duration,
        "timestamp": timestamp,
        "url": url,
        "channelName": channel_name,
        "channelId": channel_id
    })

if not history:
    print("No valid entries found to convert. Exiting.")
    sys.exit(1)

history.sort(key=lambda h: h["timestamp"], reverse=True)

final = {
    "_metadata": {
        "exportDate": datetime.utcnow().isoformat() + "Z",
        "extensionVersion": "converted-by-python",
        "totalVideos": len(history),
        "totalPlaylists": 0,
        "exportFormat": "json",
        "dataVersion": "1.1"
    },
    "history": history,
    "playlists": [],
    "stats": {
        "totalWatchSeconds": sum(h["time"] for h in history),
        "daily": {},
        "hourly": [0]*24,
        "lastUpdated": history[0]["timestamp"],
        "counters": {
            "videos": len(history),
            "shorts": sum(1 for h in history if h["duration"] <= 60),
            "totalDurationSeconds": sum(h["duration"] for h in history),
            "completed": sum(1 for h in history if h["time"] >= h["duration"]*0.95)
        },
        "stats_synced": True,
        "lastFullRebuild": int(datetime.utcnow().timestamp()*1000)
    }
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print("DONE — output saved to", output_path)
print("You can now try importing this file in YT re:Watch (Merge or Replace mode).")
