import json
import requests
from datetime import datetime, timezone

with open("channels.json", encoding="utf-8") as f:
    channels = json.load(f)["channels"]

playlist = ["#EXTM3U"]

for channel in channels:
    url = channel["url"]

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        if "#EXTM3U" not in response.text:
            print("Invalid playlist:", channel["name"])
            continue

        playlist.append(
            f'#EXTINF:-1 group-title="{channel["group"]}",'
            f'{channel["name"]}'
        )
        playlist.append(url)

        print("Validated:", channel["name"])

    except requests.RequestException as error:
        print("Failed:", channel["name"], error)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(playlist) + "\n")

print("Updated:", datetime.now(timezone.utc).isoformat())
