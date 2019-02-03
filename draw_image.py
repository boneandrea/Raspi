import sys
import os
import random
from PIL import Image, ImageFont, ImageDraw, ImageTk, ImageColor
from tkinter import Tk

ppmfile = ""
SPACE = "　"
SPACE = ""
BLACK = ImageColor.getrgb("#223300")
HEIGHT = 32

"""文字数から幅計算
"""


# def get_config():
#     return {"height": HEIGHT}


def get_width(charData):
    HEIGHT = 32
#    print(HEIGHT if charData["size"] == "full" else HEIGHT / 2)
    return len(charData["char"] + SPACE) * (HEIGHT if charData["size"] == "full" else HEIGHT / 2)


def get_all_width(charDataList=[]):
    width = 0
    for c in charDataList:
        width += get_width(c)

    return width


def pick_font():
    file = "bin/fontlist"
    with open(file) as f:
        fonts = f.readlines()
        return ImageFont.truetype(random.choice(fonts).strip(), HEIGHT)


def full_chars(charData):

    width = get_width(charData)
    text_canvas = Image.new(
        'RGB', (width, HEIGHT), random_color(10))

    draw = ImageDraw.Draw(text_canvas)

    my_str=charData["char"].strip()
    for index in range(0,len(my_str)):
        put_one_char(index*32,0,my_str[index],text_canvas)

    # 半角に
    return text_canvas

def put_one_char(x,y,one_char, canvas):

    draw = ImageDraw.Draw(canvas)
    draw.text(
        (x,y),
        one_char,
        font=pick_font(),
        fill=random_color(-120)
    )

    return canvas


def half_chars(charData):

    width = get_width(charData)
    text_canvas = Image.new('RGB', (width * 2, HEIGHT),
                            charData["background"])

    draw = ImageDraw.Draw(text_canvas)
    draw.text((0, 0), charData["char"], font=font(),
              fill=ImageColor.getrgb(charData["color"]))

    # 半角に
    return text_canvas.resize((width, HEIGHT))


def random_color(max=max):
    if max > 0:
        return (random.randint(1, max), random.randint(1, max), random.randint(1, max))
    else:
        return (random.randint(255 + max, 255), random.randint(255 + max, 255), random.randint(255 + max, 255))


def create(msgArray=[],
           outputFile="src/img/text_img",
           height=32):
    HEIGHT = height
    all_width_height = (get_all_width(msgArray), height)
    canvas = Image.new('RGB',
                       all_width_height,
                       random_color(5))
    draw = ImageDraw.Draw(canvas)

    left_offset = 0
    for m in msgArray:

        if "background" not in m.keys():
            m["background"] = random_color(10)

        if m["size"] == "full":
            full_image = full_chars(m)
            canvas.paste(full_image, (left_offset, 0))
            left_offset += get_width(m)
        elif m["size"] == "half":
            half_image = half_chars(m)
            canvas.paste(half_image, (left_offset, 0))
            left_offset += get_width(m)
        else:
            raise Exception("bad data")
            sys.exit(1)

    global ppmfile
    # 保存
    try:
        canvas.save(outputFile + ".ppm", 'PPM', quality=100, optimize=True)
        canvas.save(outputFile + ".jpg", 'JPEG', quality=100, optimize=True)
        ppmfile = outputFile + ".ppm"
        with open(outputFile + ".ppm", "rb") as f:
            return f.read()

        return True

    except Exception as e:
        raise e
        return False


if __name__ == "__main__":
    HEIGHT = int(sys.argv[2])
    create([
        {
            "char": "上野駅 - 青森駅間を東北本線・高崎線・上越線・信越本線・羽越本線・奥羽本線を経由して運行していた寝台特急列車である。",
            "size": "full",
            "color": "#55aaff",
            "background": "#010211"
        },
    ],
        outputFile=sys.argv[1],
        height=int(sys.argv[2])
    )
