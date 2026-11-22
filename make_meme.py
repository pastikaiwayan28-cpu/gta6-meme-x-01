#!/usr/bin/env python3
"""Build the GTA 6 meme for make.fun bounty gta6-meme-x-01.

Concept: a GTA fan waited 13 years for GTA 6, while make.fun's ghost
mascot already earned the game's price in a day on make.fun.

Input:  base scene (Vice City sunset balcony, 1920x1080 webp)
        make.fun ghost mark (1024x1024 transparent PNG)
Output: meme.png — square 1080x1080 PNG.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
BASE = ASSETS / "media-generation-vice-city-sunset-base-0-6d7fda68-d7ee-4309-ac36-bbadb44de261.webp"
GHOST = ASSETS / "mark-1024.png"
OUT = HERE / "meme.png"

SIZE = 1080
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_TEXT = "WAITED 13 YEARS FOR GTA 6"
BOTTOM_TEXT = "THE GHOST EARNED IT IN A DAY"
TOP_SIZE = 64
BOTTOM_SIZE = 58
MAX_TEXT_WIDTH = 1010


def wrap_text(draw, text, font, max_width):
    """Wrap to lines that fit max_width, balanced so no orphan word
    ends up alone on the last line."""
    words = text.split()
    if draw.textlength(text, font=font) <= max_width:
        return [text]
    # Try every split point; pick the one with the smallest max line width.
    best, best_score = None, None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        wa = draw.textlength(a, font=font)
        wb = draw.textlength(b, font=font)
        if wa > max_width or wb > max_width:
            continue
        score = max(wa, wb)
        if best_score is None or score < best_score:
            best, best_score = [a, b], score
    if best:
        return best
    # Fallback: greedy wrap.
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_caption(draw, lines, font, top_y, stroke=5):
    """Centered white bold text with thick black outline + soft shadow."""
    line_h = int(font.size * 1.18)
    for i, line in enumerate(lines):
        y = top_y + i * line_h
        w = draw.textlength(line, font=font)
        x = (SIZE - w) / 2
        # soft drop shadow
        draw.text((x + 3, y + 4), line, font=font, fill=(0, 0, 0, 255),
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255),
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
    return top_y + len(lines) * line_h


def main():
    base = Image.open(BASE).convert("RGB")
    if base.size != (1920, 1080):
        base = base.resize((1920, 1080), Image.LANCZOS)
    # Center-crop to square 1080x1080 (x 420..1500 keeps gamer + skyline).
    img = base.crop((420, 0, 1500, 1080)).convert("RGBA")

    # Ghost: large, sitting on the desk at the lower-right of the gamer.
    ghost = Image.open(GHOST).convert("RGBA")
    ghost_size = 330
    ghost = ghost.resize((ghost_size, ghost_size), Image.LANCZOS)
    gx, gy = 715, 620  # bottom edge at 950, leaves room for bottom caption
    # soft shadow under the ghost so it sits on the desk
    shadow = Image.new("RGBA", (ghost_size, ghost_size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.ellipse((18, 18, ghost_size - 18, ghost_size - 18), fill=(0, 0, 0, 140))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(shadow, (gx + 6, gy + 8))
    img.alpha_composite(ghost, (gx, gy))

    draw = ImageDraw.Draw(img)

    top_font = ImageFont.truetype(FONT_PATH, TOP_SIZE)
    bottom_font = ImageFont.truetype(FONT_PATH, BOTTOM_SIZE)

    top_lines = wrap_text(draw, TOP_TEXT, top_font, MAX_TEXT_WIDTH)
    draw_caption(draw, top_lines, top_font, 36)

    bottom_lines = wrap_text(draw, BOTTOM_TEXT, bottom_font, MAX_TEXT_WIDTH)
    line_h = int(BOTTOM_SIZE * 1.18)
    bottom_y = SIZE - 24 - len(bottom_lines) * line_h
    draw_caption(draw, bottom_lines, bottom_font, bottom_y)

    img.convert("RGB").save(OUT, "PNG")
    print(f"saved {OUT} ({SIZE}x{SIZE})")
    print(f"top lines: {top_lines}")
    print(f"bottom lines: {bottom_lines}")


if __name__ == "__main__":
    sys.exit(main())
