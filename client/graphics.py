from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def load_image(path):
    with Image.open(path) as img:
        return img.copy()


def crop_to_fit(img, base_height=480, max_width=800):

    w, h = img.size

    # create background layer
    bg = Image.new(mode="RGB", size=(800, 480))

    ratio = (base_height / float(h))
    width = int(w*ratio)
    cropped_img = img.resize((width, base_height), Image.Resampling.LANCZOS)

    if(width > max_width):
        left = (width - max_width)/2
        right = width - ((width - max_width)/2)
        cropped_img = img.crop((left, upper, right, bottom))
    else:
        left = int((max_width - width)/2)
        right = max_width - ((max_width - width)/2)
        upper = 0
        bottom = base_height
        bg.paste(cropped_img, (left, 0))


    return bg

def add_text(image, text):
    # Initialize the drawing context
    draw = ImageDraw.Draw(image)

    # Set font properties
    font = ImageFont.truetype('frontend/src/assets/ovo.ttf', size=45)
    
    #add scroll overlay
    scroll = Image.open(r'frontend/src/assets/scroll.png')
    scroll = crop_to_fit(scroll, base_height=100)
    image.paste(scroll, (0,0), mask=scroll)

    # Position of the text
    (x, y) = (50, 50)
    text_color = 'rgb(255, 255, 255)' # white

    # Draw the text on the image
    draw.text((x, y), text, fill=text_color, font=font)

    return image

def process_image(name, text, root_folder="/var/www/uploads"):
    
    path = f"{root_folder}/{name}"
    image = load_image(path)
    
    # All image processing goes here
    im_crop = crop_to_fit(image)
    im_text = add_text(im_crop, text)
    
    # Save the image as png
    image_tag = name.rsplit(".", 1)[0].lower()
    new_name = f"{image_tag}.png"
    new_path = f"{root_folder}/{new_name}"
    im_text.save(new_path)
    os.remove(path)

    return new_name

#process_image("test.png")
