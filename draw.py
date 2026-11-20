#!/usr/bin/env python3
"""Render the 20 November 2026 world-news summary as a 1024x1024 PNG.

A newspaper-style infographic drawn entirely with Pillow vectors and
short text labels: no faces, no generated imagery, so the page stays
sharp when shrunk to about 300 px and no glyph ever comes out garbled.
Running draw.py writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

PALETTE = {
    "deep": (13, 27, 62),
    "steel": (24, 48, 96),
    "gold": (201, 162, 39),
    "crimson": (178, 34, 34),
    "teal": (0, 128, 128),
    "ink": (18, 18, 18),
    "grey": (90, 90, 90),
    "paper": (245, 243, 238),
    "white": (255, 255, 255),
    "rule": (210, 205, 195),
    "pale_gold": (255, 214, 90),
    "pale_blue": (180, 200, 235),
    "river": (90, 140, 200),
}


def load_font(path, size):
    return ImageFont.truetype(path, size)


def split_lines(draw, text, font, width):
    """Greedy word wrap: returns the lines that fit inside width."""
    words = text.split()
    out, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def text_block(draw, x, y, text, font, color, width, leading):
    """Draw wrapped text starting at (x, y); returns the y below it."""
    for line in split_lines(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def red_kicker(draw, x, y, text):
    draw.text((x, y), text, font=load_font(SANS_BOLD, 22), fill=PALETTE["crimson"])
    return y + 30


def draw_masthead(draw):
    draw.rectangle([0, 0, CANVAS, 118], fill=PALETTE["deep"])
    draw.text((36, 22), "WORLD NEWS", font=load_font(SERIF_BOLD, 54), fill=PALETTE["white"])
    draw.text((36, 82), "FRIDAY  20  NOVEMBER  2026", font=load_font(SANS_BOLD, 30), fill=PALETTE["pale_gold"])
    for label, top in (("THE DAY", 34), ("IN SIX STORIES", 66)):
        font = load_font(SANS_BOLD, 26)
        width = draw.textlength(label, font=font)
        draw.text((CANVAS - 36 - width, top), label, font=font, fill=PALETTE["pale_blue"])


def draw_bridge_icon(draw, bx, by):
    """Three bridge spans over a river, drawn as plain strokes."""
    deep = PALETTE["steel"]
    draw.line([bx, by + 40, bx + 132, by + 40], fill=deep, width=6)
    for i in range(3):
        x0 = bx + i * 46
        draw.line([x0, by - 18, x0, by + 40], fill=deep, width=4)
        draw.line([x0, by - 18, x0 + 23, by + 40], fill=deep, width=3)
    draw.line([bx - 6, by + 62, bx + 138, by + 62], fill=PALETTE["river"], width=8)


def draw_hero(draw):
    x, y, w, h = 36, 140, 952, 300
    draw.rectangle([x, y, x + w, y + h], fill=PALETTE["white"], outline=PALETTE["rule"], width=2)
    draw.rectangle([x, y, x + w, y + 6], fill=PALETTE["gold"])
    draw_bridge_icon(draw, x + 30, y + 150)
    tx = x + 196
    y = y + 22
    y = red_kicker(draw, tx, y, "1  \u2022  KYIV  \u2022  THE BIG STORY")
    y = text_block(draw, tx, y, "Hours after the peace summit, Russia hits Kyiv",
                   load_font(SERIF_BOLD, 40), PALETTE["ink"], w - 232, 48)
    y += 8
    text_block(draw, tx, y, "Missiles and drones hit three bridges over the Dnipro; at least five dead in Kyiv and Lviv.",
               load_font(SANS, 27), PALETTE["grey"], w - 232, 36)


PANELS = [
    {
        "kick": "2  \u2022  NORTH KOREA",
        "head": ("Missile fired toward", "the Sea of Japan"),
        "body": "North Korea launches a ballistic missile, South Korea reports.",
        "color": "crimson",
    },
    {
        "kick": "3  \u2022  MARKETS",
        "head": ("Anthropic closes", "up 17% on debut"),
        "body": "Shares end near $97 after the $83 IPO; Asian markets slide.",
        "color": "teal",
    },
    {
        "kick": "4  \u2022  UKRAINE AID",
        "head": ("UK sends \u00a3260m,", "1,000+ drones"),
        "body": "London pledges long-range drones and more aid for Kyiv.",
        "color": "steel",
    },
    {
        "kick": "5  \u2022  WASHINGTON",
        "head": ("Trump pardons", "Pete Rose"),
        "body": "Posthumous pardon for the late baseball star; Senate rejects Iran war-powers measure 51\u201348.",
        "color": "crimson",
    },
]


def draw_grid(draw):
    ox, oy = 36, 462
    cw, ch, gap = 466, 218, 20
    for i, panel in enumerate(PANELS):
        x = ox + (i % 2) * (cw + gap)
        yy = oy + (i // 2) * (ch + gap)
        color = PALETTE[panel["color"]]
        draw.rectangle([x, yy, x + cw, yy + ch], fill=PALETTE["white"], outline=PALETTE["rule"], width=2)
        draw.rectangle([x, yy, x + 8, yy + ch], fill=color)
        px = x + 28
        y = yy + 18
        draw.text((px, y), panel["kick"], font=load_font(SANS_BOLD, 20), fill=color)
        y += 32
        for line in panel["head"]:
            draw.text((px, y), line, font=load_font(SERIF_BOLD, 32), fill=PALETTE["ink"])
            y += 40
        y += 6
        text_block(draw, px, y, panel["body"], load_font(SANS, 22), PALETTE["grey"], cw - 52, 28)


def draw_footer(draw):
    fy = 462 + 2 * 218 + 20 + 8
    draw.rectangle([36, fy, 988, fy + 78], fill=PALETTE["deep"])
    draw.text((56, fy + 12), "ALSO TODAY", font=load_font(SANS_BOLD, 22), fill=PALETTE["pale_gold"])
    text_block(draw, 56, fy + 40, "Houthi missile hits Riyadh tower  \u2022  COP31 Antalya  \u2022  Van Gogh sells for $190.4m",
               load_font(SANS, 22), PALETTE["white"], 912, 28)


def render():
    page = Image.new("RGB", (CANVAS, CANVAS), PALETTE["paper"])
    draw = ImageDraw.Draw(page)
    draw_masthead(draw)
    draw_hero(draw)
    draw_grid(draw)
    draw_footer(draw)
    page.save(TARGET, "PNG", optimize=True)
    print(TARGET, page.size, os.path.getsize(TARGET), "bytes")


if __name__ == "__main__":
    render()
