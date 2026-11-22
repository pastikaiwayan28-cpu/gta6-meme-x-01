#!/usr/bin/env python3
"""Meme v2 for make.fun bounty gta6-meme-x-01 — fixes v1 complaints.

v1 problems: ghost badge was a giant flat sticker pasted on the desk
corner; DejaVu Bold type looked generic; bottom caption crowded the desk.
v2: Anton (condensed meme type), ghost floating in the sky over Vice City
with a soft magenta glow + 'make.fun' label under it, captions re-split
for punch. Output: meme-v2.png (1080x1080). v1 meme.png untouched.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
BASE = ASSETS / "media-generation-vice-city-sunset-base-0-6d7fda68-d7ee-4309-ac36-bbadb44de261.webp"
GHOST = ASSETS / "mark-1024.png"
OUT = HERE / "meme-v2.png"

SIZE = 1080
ANTON = str(ASSETS / "fonts" / "Anton-Regular.ttf")
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

TOP_LINES = ["WAITED 13 YEARS", "FOR GTA 6"]
BOTTOM_LINES = ["THE GHOST", "EARNED IT IN A DAY"]
TOP_SIZE = 96
BOTTOM_SIZE = 84


def draw_caption(draw, lines, font, top_y, stroke=6):
    line_h = int(font.size * 1.08)
    for i, line in enumerate(lines):
        y = top_y + i * line_h
        w = draw.textlength(line, font=font)
        x = (SIZE - w) / 2
        draw.text((x + 4, y + 5), line, font=font, fill=(0, 0, 0, 255),
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255),
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return top_y + len(lines) * line_h


def main():
    base = Image.open(BASE).convert("RGB")
    if base.size != (1920, 1080):
        base = base.resize((1920, 1080), Image.LANCZOS)
    img = base.crop((420, 0, 1500, 1080)).convert("RGBA")

    # Ghost floating in the sky, upper right over the city — a character
    # in the scene, not a sticker on the desk.
    ghost = Image.open(GHOST).convert("RGBA")
    gs = 215
    ghost = ghost.resize((gs, gs), Image.LANCZOS)
    gx, gy = 800, 268
    # soft magenta glow behind it
    glow = Image.new("RGBA", (gs + 90, gs + 90), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((15, 15, gs + 75, gs + 75), fill=(218, 41, 140, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    img.alpha_composite(glow, (gx - 45, gy - 45))
    # soft drop shadow
    shadow = Image.new("RGBA", (gs, gs), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((14, 14, gs - 14, gs - 14), fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    img.alpha_composite(shadow, (gx + 5, gy + 7))
    img.alpha_composite(ghost, (gx, gy))

    draw = ImageDraw.Draw(img)

    # 'make.fun' label under the ghost
    label_font = ImageFont.truetype(SANS_BOLD, 40)
    label = "make.fun"
    lw = draw.textlength(label, font=label_font)
    lx = gx + (gs - lw) / 2
    ly = gy + gs + 10
    draw.text((lx + 2, ly + 3), label, font=label_font, fill=(0, 0, 0, 255),
              stroke_width=5, stroke_fill=(0, 0, 0, 255))
    draw.text((lx, ly), label, font=label_font, fill=(255, 255, 255, 255),
              stroke_width=5, stroke_fill=(0, 0, 0, 255))

    top_font = ImageFont.truetype(ANTON, TOP_SIZE)
    bottom_font = ImageFont.truetype(ANTON, BOTTOM_SIZE)

    draw_caption(draw, TOP_LINES, top_font, 30)
    line_h = int(BOTTOM_SIZE * 1.08)
    bottom_y = SIZE - 28 - len(BOTTOM_LINES) * line_h
    draw_caption(draw, BOTTOM_LINES, bottom_font, bottom_y)

    img.convert("RGB").save(OUT, "PNG")
    print(f"saved {OUT} ({SIZE}x{SIZE})")


if __name__ == "__main__":
    sys.exit(main())
