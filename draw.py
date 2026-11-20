#!/usr/bin/env python3
"""Draw the 20 Nov 2026 world-news summary image, 1024x1024 PNG.
Editorial infographic: crisp vector-style panels + short labels, no faces,
no AI-generated text, so it stays legible at 300px and nothing is garbled.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (0, 128, 128)
INK = (18, 18, 18)
GREY = (90, 90, 90)
LIGHT = (245, 243, 238)
WHITE = (255, 255, 255)
LINE = (210, 205, 195)

img = Image.new("RGB", (W, H), LIGHT)
d = ImageDraw.Draw(img)

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(x, y, text, font, color, max_w, lh):
    lines = wrap(d, text, font, max_w)
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += lh
    return y

def kicker(x, y, text, color=RED):
    d.text((x, y), text, font=F(SANS_B, 22), fill=color)
    return y + 30

# ---- header ----
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((36, 22), "WORLD NEWS", font=F(SERIF_B, 54), fill=WHITE)
d.text((36, 82), "FRIDAY  20  NOVEMBER  2026", font=F(SANS_B, 30), fill=(255, 214, 90))
for txt, yy in [("THE DAY", 34), ("IN SIX STORIES", 66)]:
    tw = d.textlength(txt, font=F(SANS_B, 26))
    d.text((W - 36 - tw, yy), txt, font=F(SANS_B, 26), fill=(180, 200, 235))

# ---- hero: Kyiv strikes ----
hx, hy, hw, hh = 36, 140, 952, 300
d.rectangle([hx, hy, hx + hw, hy + hh], fill=WHITE, outline=LINE, width=2)
d.rectangle([hx, hy, hx + hw, hy + 6], fill=GOLD)
# bridge icon: three spans over a river
bx, by = hx + 30, hy + 150
d.line([bx, by + 40, bx + 132, by + 40], fill=NAVY2, width=6)
for i in range(3):
    x0 = bx + i * 46
    d.line([x0, by - 18, x0, by + 40], fill=NAVY2, width=4)
    d.line([x0, by - 18, x0 + 23, by + 40], fill=NAVY2, width=3)
d.line([bx - 6, by + 62, bx + 138, by + 62], fill=(90, 140, 200), width=8)
tx = hx + 196
y = hy + 22
y = kicker(tx, y, "1  \u2022  KYIV  \u2022  THE BIG STORY")
y = para(tx, y, "Hours after the peace summit, Russia hits Kyiv", F(SERIF_B, 40), INK, hw - 232, 48)
y += 8
y = para(tx, y, "Missiles and drones hit three bridges over the Dnipro; at least five dead in Kyiv and Lviv.", F(SANS, 27), GREY, hw - 232, 36)

# ---- 2x2 grid ----
panels = [
    ("2  \u2022  NORTH KOREA", "Missile fired toward", "the Sea of Japan", "North Korea launches a ballistic missile, South Korea reports.", RED),
    ("3  \u2022  MARKETS", "Anthropic closes", "up 17% on debut", "Shares end near $97 after the $83 IPO; Asian markets slide.", TEAL),
    ("4  \u2022  UKRAINE AID", "UK sends \u00a3260m,", "1,000+ drones", "London pledges long-range drones and more aid for Kyiv.", NAVY2),
    ("5  \u2022  WASHINGTON", "Trump pardons", "Pete Rose", "Posthumous pardon for the late baseball star; Senate rejects Iran war-powers measure 51\u201348.", RED),
]
gx, gy = 36, 462
cw, ch, gap = 466, 218, 20
for i, (kick, l1, l2, body, col) in enumerate(panels):
    x = gx + (i % 2) * (cw + gap)
    yy = gy + (i // 2) * (ch + gap)
    d.rectangle([x, yy, x + cw, yy + ch], fill=WHITE, outline=LINE, width=2)
    d.rectangle([x, yy, x + 8, yy + ch], fill=col)
    px = x + 28
    y = yy + 18
    d.text((px, y), kick, font=F(SANS_B, 20), fill=col)
    y += 32
    d.text((px, y), l1, font=F(SERIF_B, 32), fill=INK)
    y += 40
    d.text((px, y), l2, font=F(SERIF_B, 32), fill=INK)
    y += 46
    para(px, y, body, F(SANS, 22), GREY, cw - 52, 28)

# ---- footer strip ----
fy = 462 + 2 * ch + gap + 8
d.rectangle([36, fy, 988, fy + 78], fill=NAVY)
d.text((56, fy + 12), "ALSO TODAY", font=F(SANS_B, 22), fill=(255, 214, 90))
para(56, fy + 40, "Houthi missile hits Riyadh tower  \u2022  COP31 Antalya  \u2022  Van Gogh sells for $190.4m",
     F(SANS, 22), WHITE, 912, 28)

img.save(OUT, "PNG", optimize=True)
print(OUT, img.size, os.path.getsize(OUT), "bytes")
