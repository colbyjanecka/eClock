#!/usr/bin/env python3
import requests
import time
import os

USER = "hiplandic"
SERVER_BASE = "http://heyanniewei.com"  # or internal IP if on LAN only
META_URL = f"{SERVER_BASE}/api/latest"
IMAGE_URL = f"{SERVER_BASE}/api/latest/image"
SAVE_DIR = "/home/hiplandic/"
POLL_INTERVAL = 30  # seconds

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_latest_metadata():
    r = requests.get(META_URL, timeout=5)
    if r.status_code != 200:
        print("No image yet or error:", r.status_code, r.text)
        return None
    return r.json()

def fetch_latest_image(filename_hint):
    r = requests.get(IMAGE_URL, stream=True, timeout=20)
    if r.status_code != 200:
        print("Failed to fetch image:", r.status_code, r.text)
        return None

    # Save as fixed path (for display) and as timestamped backup
    fixed_path = os.path.join(SAVE_DIR, "latest.jpg")
    with open(fixed_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Updated image:", fixed_path)
    return fixed_path

def convert_for_display(image):
    return

def main():
    last_seen_filename = None

    while True:
        try:
            meta = fetch_latest_metadata()
            if meta:
                fname = meta["filename"]
                if fname != last_seen_filename:
                    print("New image detected:", fname)
                    path = fetch_latest_image(fname)
                    if path:
                        last_seen_filename = fname
                        # Here you could trigger display / processing
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

