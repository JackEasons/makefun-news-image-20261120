#!/usr/bin/env python3
"""press.py — prints one front page of THE WORLD TODAY for Friday 20 November 2026.

Everything on the page is drawn with Pillow: masthead, a big-number strip,
three large illustrated features, ten small illustrated stories, twenty
one-line briefs, a world map with numbered dots, a markets box and a
DATE CHECK bar. Run it once and it writes entry.png next to this file.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
SOFT = (74, 72, 66)
RED = (163, 18, 18)
BLUE = (29, 78, 137)
GOLD = (150, 104, 8)
TEAL = (14, 110, 110)
RULE = (30, 30, 30)
FAINT = (205, 198, 182)
TINT_RED = (244, 226, 220)
TINT_BLUE = (222, 232, 242)
TINT_GOLD = (246, 236, 208)
TINT_TEAL = (220, 238, 236)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
MONO_B = FONT_DIR + "DejaVuSansMono-Bold.ttf"
MONO = FONT_DIR + "DejaVuSansMono.ttf"

_cache = {}


def fnt(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def text_w(draw, s, font):
    return draw.textlength(s, font=font)


def split_lines(draw, s, font, width):
    """Greedy word wrap; returns a list of lines that fit inside width."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, s, font, width, fill=INK, lead=1.22, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    lines = split_lines(draw, s, font, width)
    if max_lines:
        lines = lines[:max_lines]
    step = int(font.size * lead)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += step
    return y


def hline(draw, x, y, w, weight=2, fill=RULE):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=fill)


def vline(draw, x, y, h, weight=1, fill=FAINT):
    draw.rectangle([x, y, x + weight - 1, y + h], fill=fill)


def disc(draw, cx, cy, r, fill, outline=None):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                 outline=outline, width=2 if outline else 1)


def circ_num(draw, cx, cy, r, n, fill=RED):
    disc(draw, cx, cy, r, fill)
    t = str(n)
    fo = fnt(SANS_B, r + 2 if len(t) == 1 else r - 1)
    tw = text_w(draw, t, fo)
    th = fo.size
    draw.text((cx - tw / 2, cy - th / 2 - 1), t, font=fo, fill=(255, 255, 255))


def kick(draw, x, y, s, fill=RED):
    fo = fnt(SANS_B, 11)
    draw.text((x, y), s.upper(), font=fo, fill=fill)
    return y + 15


# ---------------------------------------------------------------- illustrations
def art_cyclone(d, x, y, w, h):
    """A spiral storm over a coastline: arcs, rain bands, a small shore."""
    d.rectangle([x, y, x + w, y + h], fill=(208, 226, 238))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(226, 214, 178))
    d.line([x, y + h - 26, x + w, y + h - 26], fill=TEAL, width=2)
    cx, cy = x + w * 0.58, y + h * 0.46
    for k in range(5):
        r = 12 + k * 9
        d.arc([cx - r, cy - r, cx + r, cy + r], start=40 + k * 55,
              end=300 + k * 55, fill=(18, 90, 130), width=3)
    disc(d, cx, cy, 6, (255, 255, 255), outline=(18, 90, 130))
    for i in range(6):
        rx = x + 12 + i * 26
        d.line([rx, y + 12, rx - 6, y + 30], fill=(90, 140, 170), width=2)
    d.text((x + 8, y + h - 22), "GOPALPUR", font=fnt(SANS_B, 10), fill=(40, 60, 60))


def art_bridges(d, x, y, w, h):
    """Three river bridges under missile trails and bursts."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 214, 190))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(120, 160, 190))
    for i, bx in enumerate([0.18, 0.48, 0.78]):
        cx = x + w * bx
        d.arc([cx - 34, y + h * 0.42, cx + 34, y + h * 0.86],
              start=180, end=360, fill=(60, 60, 60), width=4)
        d.line([cx - 34, y + h * 0.64, cx + 34, y + h * 0.64],
               fill=(60, 60, 60), width=3)
    for i in range(3):
        sx = x + 20 + i * 55
        d.line([sx, y + 8, sx + 26, y + 34], fill=RED, width=3)
        disc(d, sx + 30, y + 40, 5, (255, 190, 40), outline=RED)
        for a in range(6):
            ang = a * math.pi / 3
            d.line([sx + 30, y + 40,
                    sx + 30 + 9 * math.cos(ang), y + 40 + 9 * math.sin(ang)],
                   fill=RED, width=2)
    d.text((x + 8, y + h - 18), "DNIPRO RIVER", font=fnt(SANS_B, 10),
           fill=(40, 60, 60))


def art_globe(d, x, y, w, h):
    """A warming globe beside a thermometer; the word FOSSIL struck out."""
    d.rectangle([x, y, x + w, y + h], fill=TINT_TEAL)
    cx, cy, r = x + w * 0.30, y + h * 0.52, min(w, h) * 0.34
    disc(d, cx, cy, r, (90, 160, 200), outline=BLUE)
    for k in range(-2, 3):
        d.arc([cx - r, cy - r + k * 12, cx + r, cy + r + k * 12],
              start=200, end=340, fill=(40, 110, 60), width=2)
    d.ellipse([cx - r * 0.55, cy - r * 0.7, cx - r * 0.1, cy - r * 0.25],
              fill=(60, 140, 80))
    d.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.6, cy + r * 0.55],
              fill=(60, 140, 80))
    tx = x + w * 0.66
    d.rectangle([tx, y + 12, tx + 12, y + h - 22], outline=RED, width=3)
    d.rectangle([tx + 2, y + h - 30, tx + 10, y + h - 22], fill=RED)
    disc(d, tx + 6, y + h - 14, 8, RED)
    fo = fnt(SANS_B, 15)
    d.text((x + w * 0.60, y + h - 44), "1.5C", font=fo, fill=RED)
    d.text((x + 10, y + 8), "FOSSIL", font=fnt(SANS_B, 13), fill=(120, 30, 30))
    d.line([x + 8, y + 16, x + 62, y + 16], fill=RED, width=3)


def art_trio(d, x, y, w, h):
    """Three suited figures at a table, three small flags behind them."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 224, 205))
    flags = [((200, 40, 40), (255, 255, 255), (30, 60, 160)),
             ((220, 30, 30), (255, 210, 0), (220, 30, 30)),
             ((200, 40, 40), (255, 255, 255), (255, 255, 255))]
    for i, (c1, c2, c3) in enumerate(flags):
        fx = x + 4 + i * (w // 3)
        fw = w // 3 - 6
        d.rectangle([fx, y + 8, fx + fw, y + 16], fill=c1)
        d.rectangle([fx, y + 16, fx + fw, y + 24], fill=c2)
        d.rectangle([fx, y + 24, fx + fw, y + 32], fill=c3)
    for i in range(3):
        px = x + w * (0.22 + i * 0.28)
        disc(d, px, y + h * 0.52, 13, (222, 196, 160), outline=INK)
        d.polygon([(px - 20, y + h - 8), (px + 20, y + h - 8),
                   (px + 12, y + h * 0.66), (px - 12, y + h * 0.66)],
                  fill=(40, 50, 70))
        d.polygon([(px - 4, y + h * 0.68), (px + 4, y + h * 0.68),
                   (px, y + h * 0.82)], fill=RED)


def art_poland(d, x, y, w, h):
    """A map pin over a field, a missile streak crossing the corner."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 236, 222))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 170, 110))
    cx, cy = x + w * 0.45, y + h * 0.5
    d.polygon([(cx, cy + 16), (cx - 13, cy - 8), (cx + 13, cy - 8)], fill=RED)
    disc(d, cx, cy - 10, 12, RED, outline=(255, 255, 255))
    disc(d, cx, cy - 10, 4, (255, 255, 255))
    d.line([x + w - 8, y + 6, x + w * 0.55, y + h * 0.42], fill=(90, 90, 90),
           width=3)
    disc(d, x + w * 0.55, y + h * 0.42, 4, (255, 190, 40), outline=RED)


def art_scales(d, x, y, w, h):
    """A courthouse front with scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    d.polygon([(x + 6, y + 26), (x + w / 2, y + 4), (x + w - 6, y + 26)],
              fill=(120, 110, 90))
    for i in range(4):
        px = x + 12 + i * (w - 24) // 3
        d.rectangle([px, y + 28, px + 5, y + h - 8], fill=(120, 110, 90))
    d.rectangle([x + 6, y + h - 8, x + w - 6, y + h - 4], fill=(120, 110, 90))
    cx, cy = x + w * 0.5, y + h * 0.52
    d.line([cx, cy - 12, cx, cy + 10], fill=INK, width=2)
    d.line([cx - 14, cy - 10, cx + 14, cy - 10], fill=INK, width=2)
    d.arc([cx - 20, cy - 2, cx - 8, cy + 10], start=0, end=180, fill=INK,
          width=2)
    d.arc([cx + 8, cy - 2, cx + 20, cy + 10], start=0, end=180, fill=INK,
          width=2)


def art_bottle(d, x, y, w, h):
    """A bottle beside a hospital cross."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 232, 220))
    bx, by = x + w * 0.30, y + h * 0.22
    d.rectangle([bx, by, bx + 16, by + h * 0.6], fill=(90, 60, 40))
    d.rectangle([bx + 5, by - 10, bx + 11, by], fill=(90, 60, 40))
    d.rectangle([bx - 4, by + 8, bx + 20, by + h * 0.6], outline=(60, 40, 30),
                width=2)
    cx, cy = x + w * 0.72, y + h * 0.5
    d.rectangle([cx - 5, cy - 14, cx + 5, cy + 14], fill=RED)
    d.rectangle([cx - 14, cy - 5, cx + 14, cy + 5], fill=RED)


def art_chart(d, x, y, w, h):
    """A falling market line with red bars."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 232))
    nb = 5
    step = (w - 16) // nb
    for i, bh in enumerate([0.25, 0.4, 0.55, 0.7, 0.85]):
        bx = x + 8 + i * step
        bw = max(2, step - 3)
        d.rectangle([bx, y + h - 8 - bh * (h - 20), bx + bw, y + h - 8],
                    fill=RED if i >= 3 else (120, 120, 120))
    pts = [(x + 8 + i * ((w - 16) // 6), y + 12 + i * (h - 28) // 6)
           for i in range(7)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(pts[-1][0] - 7, pts[-1][1] - 2), (pts[-1][0] + 5, pts[-1][1] + 4),
               (pts[-1][0] - 3, pts[-1][1] + 8)], fill=RED)


def art_cards(d, x, y, w, h):
    """Three cards under a padlock."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    for i in range(3):
        cw = (w - 20) // 3
        cx = x + 10 + i * cw
        d.rounded_rectangle([cx, y + h * 0.42, cx + cw - 4,
                             y + h - 8], radius=4, fill=(250, 248, 240),
                            outline=(40, 60, 90), width=2)
        d.rectangle([cx + 2, y + h * 0.5, cx + cw - 2,
                     y + h * 0.56], fill=(200, 170, 60))
    cx, cy = x + w * 0.5, y + h * 0.26
    d.arc([cx - 9, cy - 10, cx + 9, cy + 6], start=180, end=360, fill=INK,
          width=3)
    d.rectangle([cx - 12, cy - 2, cx + 12, cy + 12], fill=(40, 40, 40))


def art_tanker(d, x, y, w, h):
    """An oil tanker on a strait between two headlands."""
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 238))
    d.polygon([(x, y), (x + w * 0.3, y), (x + w * 0.22, y + h * 0.5),
               (x, y + h * 0.5)], fill=(190, 170, 130))
    d.polygon([(x + w, y), (x + w * 0.72, y), (x + w * 0.8, y + h * 0.5),
               (x + w, y + h * 0.5)], fill=(190, 170, 130))
    d.polygon([(x + w * 0.28, y + h * 0.55), (x + w * 0.72, y + h * 0.55),
               (x + w * 0.68, y + h * 0.72), (x + w * 0.32, y + h * 0.72)],
              fill=(120, 40, 40))
    d.rectangle([x + w * 0.55, y + h * 0.40, x + w * 0.66, y + h * 0.55],
                fill=(240, 240, 240), outline=INK)
    for i in range(3):
        wx = x + w * (0.2 + i * 0.25)
        d.arc([wx, y + h - 16, wx + 26, y + h - 2], start=180, end=360,
              fill=(40, 90, 130), width=2)


def art_bridge_gap(d, x, y, w, h):
    """A bridge span snapped in the middle, smoke rising."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(120, 160, 190))
    d.line([x + 6, y + h * 0.55, x + w * 0.42, y + h * 0.55], fill=(60, 60, 60),
           width=4)
    d.line([x + w * 0.58, y + h * 0.55, x + w - 6, y + h * 0.55],
           fill=(60, 60, 60), width=4)
    d.line([x + w * 0.42, y + h * 0.55, x + w * 0.5, y + h * 0.72],
           fill=(60, 60, 60), width=3)
    d.line([x + w * 0.58, y + h * 0.55, x + w * 0.5, y + h * 0.72],
           fill=(60, 60, 60), width=3)
    for i in range(3):
        disc(d, x + w * 0.5, y + 14 + i * 10, 7 - i, (150, 150, 150))


def art_pad(d, x, y, w, h):
    """A game controller with a dollar sign."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 44))
    d.rounded_rectangle([x + 8, y + h * 0.3, x + w - 8, y + h * 0.8], radius=12,
                        fill=(70, 70, 100), outline=(200, 200, 220), width=2)
    disc(d, x + w * 0.3, y + h * 0.55, 5, (255, 255, 255))
    disc(d, x + w * 0.7, y + h * 0.55, 5, (255, 200, 60))
    d.text((x + w * 0.42, y + h * 0.36), "$", font=fnt(SANS_B, 18),
           fill=(120, 220, 120))


def art_ball(d, x, y, w, h):
    """A baseball with red stitching."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    cx, cy, r = x + w / 2, y + h / 2, min(w, h) * 0.36
    disc(d, cx, cy, r, (255, 255, 255), outline=RED)
    d.arc([cx - r + 6, cy - r + 4, cx + r - 14, cy + r - 4], start=300,
          end=60, fill=RED, width=2)
    d.arc([cx + r - 22, cy - r + 4, cx + r + 10, cy + r - 4], start=120,
          end=240, fill=RED, width=2)


ICONS = {
    "trio": art_trio, "poland": art_poland, "scales": art_scales,
    "bottle": art_bottle, "chart": art_chart, "cards": art_cards,
    "tanker": art_tanker, "bridge_gap": art_bridge_gap, "pad": art_pad,
    "ball": art_ball,
}


# ---------------------------------------------------------------- world map
LAND = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 62),
     (-55, 47), (-70, 42), (-80, 32), (-85, 30), (-97, 26), (-105, 20),
     (-115, 28), (-125, 40), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -22), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-75, -40), (-80, -20), (-80, -5)],
    [(-10, 36), (-2, 37), (3, 43), (8, 44), (12, 45), (18, 40), (23, 36),
     (28, 41), (30, 46), (20, 55), (18, 60), (10, 62), (5, 58), (-5, 50),
     (-10, 43)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (28, -33),
     (20, -35), (15, -28), (12, -18), (9, -1), (8, 4), (-8, 5), (-13, 9)],
    [(30, 46), (40, 45), (50, 40), (55, 38), (60, 25), (66, 25), (72, 20),
     (77, 8), (80, 7), (85, 20), (90, 22), (95, 16), (100, 8), (103, 1),
     (105, 10), (109, 15), (108, 20), (115, 23), (120, 28), (122, 32),
     (127, 35), (130, 42), (135, 45), (142, 50), (158, 60), (170, 66),
     (178, 65), (170, 60), (160, 55), (142, 45), (135, 40), (127, 38),
     (122, 30), (115, 20), (108, 12), (103, 5), (98, 10), (92, 15),
     (88, 22), (80, 15), (75, 8), (72, 20), (66, 25), (60, 25), (55, 26),
     (50, 29), (48, 30), (44, 29), (40, 32), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (137, -12), (135, -15), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]

DOTS = [
    (1, 84.8, 19.1), (2, 30.5, 50.4), (3, 30.7, 36.9), (4, -77.0, 38.9),
    (5, 22.6, 51.2), (6, 4.3, 52.1), (7, 93.9, 24.8), (8, -74.0, 40.7),
    (10, 56.5, 26.5), (11, 36.5, 45.3),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    d.rectangle([x, y, x + w, y + h], outline=(120, 140, 160), width=2)
    for poly in LAND:
        pts = [(x + (lon + 170) / 360 * w, y + (75 - lat) / 130 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=(226, 214, 178), outline=(120, 110, 80))
    # nudge the tight Europe and US-east dots apart, with leader lines
    nudge = {2: (-8, -11), 3: (12, 9), 4: (-16, 10), 5: (-16, 1),
             6: (-13, -9)}
    for n, lon, lat in DOTS:
        px = x + (lon + 170) / 360 * w
        py = y + (75 - lat) / 130 * h
        dx, dy = nudge.get(n, (0, 0))
        if (dx, dy) != (0, 0):
            d.line([px, py, px + dx, py + dy], fill=RED, width=1)
        circ_num(d, px + dx, py + dy, 8, n)


# ---------------------------------------------------------------- the stories
# Every line below is written for this page. Figures are the ones reported
# on Friday 20 November 2026; where a figure was later updated, the Friday
# figure is the one printed and the update is noted in STORIES.md.

BIG = [
    dict(n=1, kick="INDIA · CYCLONE", art="cyclone", region="ASIA",
         head="440,000 FLEE AS AKVAN SLAMS INTO ODISHA",
         body=("Cyclone Akvan came ashore near Gopalpur between 7:30 and "
               "8:30 in the morning, weaker than feared, with winds of "
               "70 to 80 km/h. Odisha moved 440,461 people to safety and "
               "reported no deaths. In the shelters, 2,316 babies were "
               "born; 47 trains were cancelled."),
         src="IMD · The New Indian Express"),
    dict(n=2, kick="UKRAINE · WAR", art="bridges", region="EUROPE",
         head="111 MISSILES, 404 DRONES: KYIV'S BRIDGES HIT",
         body=("Russia fired its biggest air strike of the month overnight: "
               "27 ballistic and 84 cruise missiles and 404 drones. Eight "
               "people were killed. Three bridges over the Dnipro were "
               "damaged, power failed in parts of the capital, and two "
               "missiles fell in Poland."),
         src="Reuters · Al Jazeera · ISW"),
    dict(n=3, kick="CLIMATE · COP31", art="globe", region="GLOBAL",
         head="CLIMATE TALKS CLOSE WITH FOSSIL FUELS CUT FROM TEXT",
         body=("By the scheduled last day in Antalya, the summit's draft "
               "had dropped every mention of fossil fuels and lost its "
               "$120bn adaptation target. The 35-by-35 electricity goal "
               "survived. Negotiators left without the consensus the "
               "opening draft had promised."),
         src="Reuters · The Indian Express"),
]

SMALL = [
    dict(n=4, kick="USA · SUMMIT", art="trio", region="AMERICAS",
         head="Trump calls Shenzhen summit 'momentous'",
         body=("At the White House, Trump hailed the Xi–Putin meeting and "
               "held up their peace declaration."),
         src="Le Monde · HKFP"),
    dict(n=5, kick="POLAND · WAR", art="poland", region="EUROPE",
         head="Two Russian missiles crash on Polish soil",
         body=("A Kh-101 came down in Nowy Lipowiec; another missile and "
               "a drone fell in Lublin. No one was hurt."),
         src="Reuters · ISW"),
    dict(n=6, kick="THE HAGUE · JUSTICE", art="scales", region="ASIA",
         head="Myanmar guilty of Rohingya genocide",
         body=("The court ruled 9–6 that Myanmar committed genocide, a "
               "first for any state, and ordered reparations."),
         src="Al Jazeera · Dawn"),
    dict(n=7, kick="INDIA · HEALTH", art="bottle", region="ASIA",
         head="Bad liquor kills 13 in Manipur",
         body=("Thirteen died and 346 were in hospital by Friday night "
               "after drinking tainted liquor in Chandel."),
         src="The Hindu"),
    dict(n=8, kick="MARKETS · USA", art="chart", region="AMERICAS",
         head="Wall Street slides into correction",
         body=("The Dow fell 1.9%, the S&P 3.7% and the Nasdaq 5.3% in an "
               "AI sell-off — the worst week since 2020."),
         src="Nikkei · Reuters"),
    dict(n=9, kick="CYBER · BANKS", art="cards", region="GLOBAL",
         head="16,000 bank customers' data leaked",
         body=("The n0n group leaked vendor data from JPMorgan, Visa and "
               "Mastercard, including 16,000 JPMorgan emails."),
         src="Reuters · TechSpot"),
    dict(n=10, kick="GULF · OIL", art="tanker", region="MIDDLE EAST",
         head="Iran to test US blockade with tankers",
         body=("The US blockade held. Tehran said a tanker convoy would "
               "sail from Kharg Island to test it."),
         src="Saudi Gazette"),
    dict(n=11, kick="UKRAINE · WAR", art="bridge_gap", region="EUROPE",
         head="Kerch Bridge hit a third time in a week",
         body=("Ukrainian strikes hit the Crimea bridge again, knocking "
               "out rail spans. Moscow vowed retaliation."),
         src="CNN"),
    dict(n=12, kick="CULTURE · GAMES", art="pad", region="AMERICAS",
         head="GTA 6 sales pass $2.3bn",
         body=("The year's biggest game passed $2.3 billion in sales in "
               "its opening days — a record."),
         src="Saudi Gazette"),
    dict(n=13, kick="USA · SPORT", art="ball", region="AMERICAS",
         head="Trump pardons Pete Rose",
         body=("Trump posthumously pardoned Pete Rose, baseball's banned "
               "hits leader, barred from the Hall for betting."),
         src="Saudi Gazette"),
]

BRIEFS = [
    ("Cox's Bazar", "Rohingya refugees welcome the genocide verdict.", "Al Jazeera", "ASIA"),
    ("California", "State subpoenas Nvidia over China risks.", "IANS", "AMERICAS"),
    ("Washington", "Trump sacks cyber chief after tech outages.", "Saudi Gazette", "AMERICAS"),
    ("Washington", "US sanctions scam enablers in Cambodia and Myanmar.", "IANS", "ASIA"),
    ("Riyadh", "Saudi Arabia signs a labour-rights framework.", "Tribune Online", "MIDDLE EAST"),
    ("Paris", "Ex-PM de Villepin launches a presidential bid.", "Saudi Gazette", "EUROPE"),
    ("Israel", "A mosque is set on fire after alleged incitement.", "Saudi Gazette", "MIDDLE EAST"),
    ("Texas", "An execution is botched as staff struggle to find a vein.", "Saudi Gazette", "AMERICAS"),
    ("Tokyo", "China warns climbers after one goes missing on Fuji.", "Saudi Gazette", "ASIA"),
    ("Jakarta", "Daycare chief jailed five years over child abuse.", "Saudi Gazette", "ASIA"),
    ("Mexico City", "US: Chinese chemicals fuel the Sinaloa cartel.", "Standard Topic", "AMERICAS"),
    ("New Delhi", "India's US Treasury holdings rise to $228.2bn.", "IANS", "ASIA"),
    ("Rawalpindi", "Pakistan beat Sri Lanka by 8 wickets, take the series.", "Apex Sports", "ASIA"),
    ("Doha", "India A thrash Nepal by 306 runs in the Asia Cup Rising Stars.", "IANS", "ASIA"),
    ("Wellington", "NZ 368 (Nicholls 175*), India reply in 1st Test.", "Apex Sports", "OCEANIA"),
    ("Madrid", "Real Madrid extend goalkeeper Courtois to June 2028.", "IANS", "EUROPE"),
    ("New Delhi", "IEA: India is among the biggest drivers of energy growth.", "IANS", "ASIA"),
    ("Washington", "US Army delays detonating bomb chemicals.", "Saudi Gazette", "AMERICAS"),
    ("Johannesburg", "S. Africans protest, demand ban on Nigerians.", "Tribune Online", "AFRICA"),
    ("Washington", "Democrats propose ending old deportation orders.", "IANS", "AMERICAS"),
]

NUMBERS = [
    ("440,461", "people evacuated in Odisha"),
    ("0", "deaths reported from Akvan"),
    ("111", "missiles fired at Ukraine"),
    ("404", "drones in the same attack"),
    ("9–6", "ICJ vote on Myanmar genocide"),
    ("−5.3%", "Nasdaq fall on Friday"),
]


# ---------------------------------------------------------------- layout
def region_tally():
    order = ["ASIA", "EUROPE", "MIDDLE EAST", "AMERICAS", "AFRICA",
             "OCEANIA", "GLOBAL"]
    counts = {r: 0 for r in order}
    for s in BIG + SMALL:
        counts[s["region"]] += 1
    for _, _, _, r in BRIEFS:
        counts[r] += 1
    return [(r, counts[r]) for r in order if counts[r]]


def masthead(d, y):
    hline(d, 14, y, 996, 3)
    title = "THE WORLD TODAY"
    fo = fnt(SERIF_B, 58)
    tw = text_w(d, title, fo)
    d.text(((W - tw) / 2, y + 8), title, font=fo, fill=INK)
    sub = fnt(SANS_B, 15)
    d.text((14, y + 72), "FRIDAY 20 NOVEMBER 2026", font=sub, fill=INK)
    tally = " · ".join(f"{r} {c}" for r, c in region_tally())
    right = f"33 STORIES · {tally}"
    fo2 = fnt(SANS_B, 11)
    d.text((W - 14 - text_w(d, right, fo2), y + 76), right, font=fo2,
           fill=SOFT)
    return y + 90


def number_strip(d, y):
    hline(d, 14, y, 996, 1)
    cw = 996 / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = 14 + cw * i + cw / 2
        fo = fnt(MONO_B, 23)
        tw = text_w(d, num, fo)
        d.text((cx - tw / 2, y + 5), num, font=fo, fill=RED)
        fl = fnt(SANS, 10)
        tw2 = text_w(d, label, fl)
        d.text((cx - tw2 / 2, y + 33), label, font=fl, fill=SOFT)
        if i:
            vline(d, int(14 + cw * i), y + 5, 40)
    hline(d, 14, y + 48, 996, 1)
    return y + 54


def big_feature(d, x, y, w, s):
    circ_num(d, x + 11, y + 11, 11, s["n"])
    d.text((x + 28, y + 4), s["kick"], font=fnt(SANS_B, 11), fill=RED)
    yy = y + 26
    yy = block(d, x, yy, s["head"], fnt(SERIF_B, 20), w, lead=1.12)
    yy += 4
    if s["art"] == "cyclone":
        art_cyclone(d, x, yy, w, 72)
    elif s["art"] == "bridges":
        art_bridges(d, x, yy, w, 72)
    else:
        art_globe(d, x, yy, w, 72)
    yy += 78
    yy = block(d, x, yy, s["body"], fnt(SANS, 11.5), w, lead=1.2)
    yy += 3
    d.text((x, yy), "Source: " + s["src"], font=fnt(SANS, 10), fill=SOFT)
    return yy + 13


def big_row(d, y):
    cols = [14, 350, 686]
    bottom = y
    for cx, s in zip(cols, BIG):
        bottom = max(bottom, big_feature(d, cx, y, 324, s))
    hline(d, 14, bottom + 4, 996, 2)
    return bottom + 10


def small_cell(d, x, y, w, s):
    ICONS[s["art"]](d, x, y + 2, 46, 46)
    hx = x + 54
    yy = block(d, hx, y, s["head"], fnt(SANS_B, 13), w - 54, lead=1.15)
    yy = max(yy, y + 48)
    yy = block(d, x, yy + 2, s["body"], fnt(SANS, 11), w, lead=1.25)
    d.text((x, yy + 2), s["src"], font=fnt(SANS, 9), fill=SOFT)
    return yy + 15


def small_grid(d, y):
    row_h = 110
    for r in range(2):
        for c in range(5):
            s = SMALL[r * 5 + c]
            small_cell(d, 14 + c * 200, y + r * row_h, 195, s)
        if r == 0:
            hline(d, 14, y + row_h - 6, 996, 1, fill=FAINT)
    return y + 2 * row_h


def map_and_markets(d, y):
    hline(d, 14, y, 996, 2)
    y += 8
    d.text((14, y), "WHERE IT HAPPENED", font=fnt(SANS_B, 13), fill=INK)
    draw_map(d, 14, y + 20, 630, 108)
    mx = 656
    d.rectangle([mx, y, mx + 354, y + 128], outline=RULE, width=2)
    d.text((mx + 10, y + 6), "MARKETS & MONEY", font=fnt(SANS_B, 13),
           fill=INK)
    rows = [("DOW", "48,147", "−1.9%"), ("S&P 500", "6,910", "−3.7%"),
            ("NASDAQ", "22,618", "−5.3%")]
    ry = y + 30
    for name, val, chg in rows:
        d.text((mx + 10, ry), name, font=fnt(SANS_B, 13), fill=INK)
        d.text((mx + 150, ry), val, font=fnt(MONO_B, 14), fill=INK)
        d.text((mx + 260, ry), chg, font=fnt(MONO_B, 14), fill=RED)
        ry += 22
    block(d, mx + 10, ry + 2,
          "S&P and Dow in correction — 10% off peaks; worst week since 2020.",
          fnt(SANS, 11), 334, lead=1.25)
    return y + 132


def briefs(d, y):
    hline(d, 14, y, 996, 2)
    y += 8
    d.text((14, y), "ALSO ON FRIDAY — 14–33",
           font=fnt(SANS_B, 13), fill=INK)
    y += 18
    fo = fnt(SANS, 11.5)
    fb = fnt(SANS_B, 11.5)
    for i, (place, txt, src, _r) in enumerate(BRIEFS):
        col = i // 10
        row = i % 10
        bx = 14 + col * 504
        by = y + row * 14
        d.text((bx, by), f"{14 + i}. ", font=fb, fill=RED)
        off = text_w(d, f"{14 + i}. ", fb)
        d.text((bx + off, by), place + " — ", font=fb, fill=INK)
        off += text_w(d, place + " — ", fb)
        line = txt + " (" + src + ")"
        d.text((bx + off, by), line, font=fo, fill=INK)
    return y + 10 * 14 + 2


def footer(d, y):
    hline(d, 14, y, 996, 2)
    y += 6
    d.rectangle([14, y, 1010, y + 35], fill=TINT_RED)
    msg = ("DATE CHECK ✓ — Every story above happened or was first "
           "reported on Friday 20 November 2026, except: the ICJ verdict "
           "came on Thursday 19 Nov; Kenya's last Ebola patient left "
           "hospital on 11 Nov; no credible report of a North Korean "
           "missile launch on 19–20 Nov.")
    block(d, 22, y + 4, msg, fnt(SANS, 10.5), 972, lead=1.3)
    y += 41
    d.text((14, y), "HOW SURE ARE WE?  REPORTED = confirmed by two or more "
           "outlets  ·  CLAIM = one source, named  ·  Drawn by hand — no "
           "photographs. Sources on every story.",
           font=fnt(SANS, 10), fill=SOFT)
    return y + 14


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 8
    y = masthead(d, y)
    y = number_strip(d, y + 2)
    y = big_row(d, y + 2)
    y = small_grid(d, y + 2)
    y = map_and_markets(d, y + 2)
    y = briefs(d, y + 2)
    y = footer(d, y + 2)
    print("bottom y:", y, "of", H)
    return img


if __name__ == "__main__":
    import sys
    page = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    page.save(out, optimize=True)
    print("wrote", out)
