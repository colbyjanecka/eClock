import csv
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
#from pudzu.pillar import Image, ImageDraw, ImageFont, sans
import textwrap

def split_quote_with_tag(quote, tag):
    """Split quote into [before, tag, after] - returns 3 parts as list"""
    idx = quote.find(tag)
    if idx == -1:
        # Tag not found: return whole quote as first part, empty tag/after
        return [quote, "", ""]
    
    return [
        quote[:idx],      # before tag
        tag,              # the tag itself
        quote[idx + len(tag):]  # after tag
    ]

def generate_clock_image():
    font = ImageFont.truetype(font='lib/StardewValley.ttf', size=50)
    font_large = ImageFont.truetype(font='lib/StardewValley.ttf', size=30)
    img = Image.new(mode = "RGB", size = (800, 480), color = (255, 255, 255))

    entry = get_quote()
    quote = entry['quote']
    source = entry['source'] + ", " + entry['author']

    quote_spit = split_quote_with_tag(quote, entry['tag'])
    print(quote_spit)

    quote = textwrap.fill(text=quote, width=37)

    draw = ImageDraw.Draw(im=img)
    draw.text(xy=(25, 25), text=quote, font=font, fill='#000000')
    draw.text(xy=(75, 430), text=source, font=font_large, fill='#000000')

    book_icon = Image.open("lib/book.png")  # or Image.open("book.png")
    
    # After creating your main img with quote/source
    img.paste(book_icon, (5, 410), book_icon)

    print("saving clock image file")
    img.save("latest.png")



def get_quote():

    matches = []
    now_str = datetime.now().strftime("%H:%M")  # e.g. "13:25"
    #now_str = "13:25"

    with open("data.csv", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")  # uses first row as headers
        for row in reader:
            # row["time"] is a string from the CSV
            if row["time"] == now_str:
                matches.append(row)
        #return(row)
    if matches:
        chosen = random.choice(matches)
        return(chosen)
        # Example: access another column
        # print(chosen["some_other_column"])
    else:
        print(f"No rows with time = {now_str}")


