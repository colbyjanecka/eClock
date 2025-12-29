from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import textwrap
from collections import Counter

def load_image(path):
    with Image.open(path) as img:
        return img.copy()

def most_common_border_color(path, border_width=1):
    img = Image.open(path).convert("RGBA")  # or "RGB"
    w, h = img.size
    pixels = img.load()
    counts = Counter()

    # Top and bottom borders
    for x in range(w):
        for dy in range(border_width):
            counts[pixels[x, dy]] += 1              # top
            counts[pixels[x, h - 1 - dy]] += 1      # bottom

    # Left and right borders (excluding corners already counted)
    for y in range(border_width, h - border_width):
        for dx in range(border_width):
            counts[pixels[dx, y]] += 1              # left
            counts[pixels[w - 1 - dx, y]] += 1      # right

    # Most common color (RGBA or RGB tuple)
    return counts.most_common(1)[0][0]


def crop_to_fit(img, base_height=480, max_width=800, border=(0,0,0,0)):

    w, h = img.size

    # create background layer
    bg = Image.new(mode="RGBA", size=(800, 480), color=border)

    ratio = (base_height / float(h))
    width = int(w*ratio)
    cropped_img = img.resize((width, base_height), Image.Resampling.LANCZOS)

    upper = 0
    bottom = base_height

    if(width > max_width):
        left = (width - max_width)/2
        right = width - ((width - max_width)/2)
        bg = img.crop((left, upper, right, bottom))
    else:
        left = int((max_width - width)/2)
        right = max_width - ((max_width - width)/2)
        bg.paste(cropped_img, (left, 0))


    return bg

def draw_sample(self, dr, font, x, y, align, anchor):
    radius = 3
    text = f'The first line\nAnchor: {anchor}\nLine 3'
    dr.multiline_text((x, y), text=text,
        fill='blue', font=font, anchor=anchor, align=align)
    dr.ellipse((x - radius, y - radius, x + radius, y + radius),
        fill='yellow', outline='black')

def add_text(image, text):
    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Set font properties
    font = ImageFont.truetype('frontend/src/assets/ovo.ttf', size=20    )
    
    #add scroll overlay
    window = Image.open(r'frontend/src/assets/window.png').convert("RGBA")
    mask = window.split()[-1].convert('L')
    window = crop_to_fit(window, base_height=340)
    image.paste(window, (-245,205), mask=window)

    # Size of Text
    text = textwrap.fill(text, width=20, break_long_words=False)

    # Position of the text
    (x, y) = (160, 390)
    text_color = 'rgb(255, 255, 255)' # white

    # Draw the text on the image
    # draw.text((x, y), text, fill=text_color, font=font)
    draw.multiline_text((x, y), text, font=font, fill="black", spacing=6, align="center", anchor="mm")

    return image

def process_image(name, text, root_folder="/var/www/uploads"):
    
    path = f"{root_folder}/{name}"
    border_color = most_common_border_color(path)
    print(border_color)
    image = load_image(path)
    
    # All image processing goes here
    im_crop = crop_to_fit(image, border=border_color)
    if(text != "n/a"):
        im_crop = add_text(im_crop, text)
    
    # Save the image as png
    image_tag = name.rsplit(".", 1)[0].lower()
    new_name = f"{image_tag}.png"
    new_path = f"{root_folder}/{new_name}"
    im_crop.save(new_path)
    os.remove(path)

    return new_name

#process_image("test.png")
