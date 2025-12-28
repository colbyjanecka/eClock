#!/usr/bin/env python3
import requests
import time
import os
import sys
import logging
import subprocess
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'client/lib')
print(libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd7in3e
from PIL import Image,ImageDraw,ImageFont
import traceback
from wand.image import Image as WandImage

logging.basicConfig(level=logging.DEBUG)

USER = "pi"
SERVER_BASE = "http://heyanniewei.com"  # or internal IP if on LAN only
META_URL = f"{SERVER_BASE}/api/latest"
IMAGE_URL = f"{SERVER_BASE}/api/latest/image"
SAVE_DIR = "/home/pi/client/"
POLL_INTERVAL = 5  # seconds

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
    fixed_path = os.path.join(SAVE_DIR, "latest.png")
    with open(fixed_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("Updated image:", fixed_path)
    return fixed_path

def edge(input_image_path, output_path):
    with WandImage(filename=input_image_path) as img:
        img.transform_colorspace("gray")
        img.edge(radius=3)
        img.save(filename=output_path)

def update_display(epd):
    cmd = [
        "magick", "convert",
        "latest.png",
        "-resize", "800x480^",
        "-gravity", "center",
        "-extent", "800x480",
        "-brightness-contrast", "0,30",
        "-modulate", "100,200,100",
        "-dither", "FloydSteinberg",
        "-remap", "palette.png",
        "-type", "truecolor",
        "-set", "filename:myname", "%t",
        "%[filename:myname].bmp",
    ]
    # im = imread(fname)
    logging.info("1.Drawing on the image...")
    #edge("latest.png","latest.png")
    subprocess.run(cmd, check=True)
    print("Converting Image Colors")
    time.sleep(2)
    Himage = Image.open(os.path.join(SAVE_DIR, "latest.bmp"))
    epd.display(epd.getbuffer(Himage))
    return

def main():
    last_seen_filename = None
    epd = epd7in3e.EPD()   
    epd.init()
    # font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    while True:
        try:
            meta = fetch_latest_metadata()
            if meta:
                fname = meta["filename"]
                if fname != last_seen_filename:
                    print("New image detected:", fname)
                    path = fetch_latest_image(fname)
                    if path:
                        print("NEW IMAGE FNAME: ", fname)
                        last_seen_filename = fname

                        # Here you could trigger display / processing
                        update_display(epd)
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()

