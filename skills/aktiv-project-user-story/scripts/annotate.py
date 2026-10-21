# -*- coding: utf-8 -*-
"""Annotate a screenshot with red arrows + red text labels (Aktiv convention).

    from annotate import annotate
    annotate("raw.png", "out.png",
             notes=[
               # label sits at xy; arrow (optional) points FROM the label TO target
               {"xy": (60, 40), "text": "New customs summary page", "to": (400, 120)},
               {"xy": (900, 300), "text": "Group by H.S. Code", "to": (1000, 250)},
             ],
             crop=(0, 80, 1275, 700))   # optional (left,top,right,bottom)
"""
from PIL import Image, ImageDraw, ImageFont

RED = (200, 25, 25)


def _font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _arrow(draw, start, end, width=4):
    draw.line([start, end], fill=RED, width=width)
    import math
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    L = 16
    for da in (math.radians(155), math.radians(-155)):
        draw.line(
            [end, (end[0] + L * math.cos(ang + da),
                   end[1] + L * math.sin(ang + da))],
            fill=RED, width=width,
        )


def annotate(src, dst, notes, crop=None, font_size=26):
    img = Image.open(src).convert("RGB")
    if crop:
        img = img.crop(crop)
        ox, oy = crop[0], crop[1]
    else:
        ox = oy = 0
    draw = ImageDraw.Draw(img)
    font = _font(font_size)
    for n in notes:
        x, y = n["xy"][0] - ox, n["xy"][1] - oy
        text = n["text"]
        tb = draw.textbbox((x, y), text, font=font)
        pad = 6
        draw.rectangle([tb[0] - pad, tb[1] - pad, tb[2] + pad, tb[3] + pad],
                       fill=(255, 255, 255), outline=RED, width=3)
        draw.text((x, y), text, fill=RED, font=font)
        if n.get("to"):
            tx, ty = n["to"][0] - ox, n["to"][1] - oy
            # start the arrow at the middle-bottom of the label box
            sx = (tb[0] + tb[2]) / 2
            sy = tb[3] + pad
            _arrow(draw, (sx, sy), (tx, ty))
    img.save(dst)
    return dst
