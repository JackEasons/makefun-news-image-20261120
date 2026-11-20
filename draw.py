#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Friday 20 November 2026.

One 1024x1024 PNG summing up the day's world news: 3 big illustrated
features, 10 small illustrated stories, 20 briefs, a world map with
numbered dots, a big-number strip, region counts and a DATE CHECK bar.
Every fact was checked against the outlet named beside it; two
candidate stories were left out because they could not be verified
(see STORIES.md). Pure PIL, no network, no clock, no randomness:
the same run always writes the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (17, 17, 17)
PAPER = (255, 255, 255)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GREY = (107, 114, 128)
LIGHT = (242, 242, 242)
PANEL = (247, 243, 234)
YELLOW = (255, 247, 214)
SEA = (220, 235, 245)
LAND = (217, 217, 217)
GOLD = (180, 130, 20)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(size, bold=False, serif=False):
    key = (size, bold, serif)
    if key not in _cache:
        path = SERIF if serif else (SANSB if bold else SANS)
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    lines = wrap(text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, y, weight=2, x0=16, x1=1008):
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)


# ---------------------------------------------------------------- data
# region order for the strip; counts are computed from the stories below.
REGIONS = ["ASIA", "EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "OCEANIA", "GLOBAL"]

BIG = [
    dict(n=1, region="ASIA", kick="1  ·  INDIA — CYCLONE",
         head="AKVAN HITS INDIA: 300,000 FLEE",
         body=("Cyclone Akvan crossed the Odisha–Andhra coast near Gopalpur "
               "early Friday, winds gusting to 90 km/h. Odisha moved 372,000 "
               "people to 9,341 shelters and cancelled 69 trains. "
               "No deaths reported."),
         src="REUTERS · IMD · SAMBAD"),
    dict(n=2, region="EUROPE", kick="2  ·  UKRAINE — WAR",
         head="KYIV'S BRIDGES HIT IN NIGHT BARRAGE",
         body=("Russia fired 110+ missiles and 404 drones overnight, hours "
               "after the Shenzhen summit. Three Dnipro bridges were hit; "
               "8 killed, 28 hurt. Poland scrambled jets as debris fell "
               "on its soil."),
         src="CNN · REUTERS · THE TIMES"),
    dict(n=3, region="EUROPE", kick="3  ·  THE HAGUE — JUSTICE",
         head="MYANMAR GUILTY OF GENOCIDE",
         body=("The World Court ruled 9–6 that Myanmar committed genocide "
               "against the Rohingya — the first such finding against a "
               "state. Judges found mass killings and sexual violence "
               "in Rakhine."),
         src="ICJ · REUTERS"),
]

SMALL = [
    dict(n=4, region="EUROPE", kick="ANTALYA",
         head="ANTALYA — COP31: fossil fuels vanish",
         body=("Draft drops fossil fuels and $120bn. "
               "Turkey lands $26bn+."),
         src="REUTERS"),
    dict(n=5, region="ASIA", kick="SHENZHEN",
         head="SHENZHEN — Trump, Xi, Putin: no deal",
         body=("70 min, joint declaration — no deal "
               "on Ukraine or Iran."),
         src="CNN"),
    dict(n=6, region="GLOBAL", kick="MARKETS",
         head="MARKETS — Stocks sink; Anthropic holds",
         body=("Nikkei −4.8%, Dow −1,101. "
               "Anthropic holds +17%."),
         src="WSJ · REUTERS"),
    dict(n=7, region="EUROPE", kick="BERLIN",
         head="BERLIN — Britain arms Kyiv: £260m",
         body=("1,000+ drones, 1,000 km range, "
               "announced in Berlin."),
         src="GOV.UK"),
    dict(n=8, region="MIDDLE EAST", kick="RIYADH",
         head="RIYADH — Houthi missile hits tower",
         body=("PIF tower damaged; Saudi intercepts "
               "a missile, 5 drones."),
         src="ONE TURN"),
    dict(n=9, region="AMERICAS", kick="WASHINGTON",
         head="WASHINGTON — Rose pardoned; Iran bid fails",
         body=("Rose pardoned (4,256 hits); Senate "
               "rejects Iran bid 51–48."),
         src="REUTERS"),
    dict(n=10, region="AMERICAS", kick="SENATE",
         head="SENATE — Energy bill passes 62–33",
         body=("Faster approvals for plants, grids, "
               "mines and data centres."),
         src="BANGLADESH CHRONICLE"),
    dict(n=11, region="EUROPE", kick="ROME",
         head="ROME — Italy fines Meta €805m",
         body=("Fine over Android photo access."),
         src="MORNING BRIEFING"),
    dict(n=12, region="AMERICAS", kick="VICE CITY",
         head="VICE CITY — GTA VI out, rated 99",
         body=("Out Thursday: Vice City returns, "
               "Metacritic 99."),
         src="PEOPLE · USA TODAY"),
    dict(n=13, region="GLOBAL", kick="YOUTH",
         head="YOUTH — Strike in 25+ countries",
         body=("Striking Friday over living costs "
               "and militarisation."),
         src="ONE TURN"),
]

BRIEFS = [
    (14, "EUROPE", "POLAND — Jets scrambled as debris falls in Poland.", "CNN"),
    (15, "GLOBAL", "IMF — Global public debt nears 100% of GDP.", "IMF"),
    (16, "AMERICAS", "USA — FAA ground stop strands 1.5m travellers.", "MORNING BRIEFING"),
    (17, "AMERICAS", "FLORIDA — St. Johns River in record flood.", "WPC"),
    (18, "AFRICA", "AFRICA — Ethiopia, Eritrea mass troops on border.", "SOMALIA TODAY"),
    (19, "AFRICA", "SOMALIA — Expels UAE ambassador, citing 'invasion'.", "REUTERS"),
    (20, "OCEANIA", "PACIFIC — First US deep-sea mining sale near Samoa.", "GUARDIAN"),
    (21, "GLOBAL", "ENERGY — IEA: AI data centres may lift emissions.", "IEA"),
    (22, "ASIA", "CYBER — China-linked spies hit VMware zero-day.", "MORNING BRIEFING"),
    (23, "AMERICAS", "VIRGINIA — Quits Trump school-choice tax plan.", "MORNING BRIEFING"),
    (24, "OCEANIA", "NIUE — Pacific island wins Earthshot 2026 award.", "SMC"),
    (25, "AFRICA", "AFRICA — Rescued rhinos, relocated giraffes.", "MORNING BRIEFING"),
    (26, "AMERICAS", "NEW YORK — Trump $15bn NYT suit survives dismissal.", "FOX"),
    (27, "AMERICAS", "WASHINGTON — Trump fires cyber director Cairncross.", "FOX"),
    (28, "AMERICAS", "TEXAS — Execution lasts over an hour amid IV issues.", "FOX"),
    (29, "MIDDLE EAST", "IRAQ — Forces deploy near Hezbollah stronghold.", "BANGLADESH CHRONICLE"),
    (30, "ASIA", "BANGLADESH — Tense after shutdown and violence.", "BANGLADESH CHRONICLE"),
    (31, "ASIA", "PAKISTAN — Forces kill 22 militants near border.", "BANGLADESH CHRONICLE"),
    (32, "EUROPE", "LONDON — UK, Norway fund two £100m attack boats.", "EUROPESAYS"),
    (33, "AMERICAS", "WALL ST — Anthropic debut mints millionaires.", "FOX"),
]

BIG_NUMBERS = [
    ("300,000+", "EVACUATED IN INDIA"),
    ("110+", "MISSILES AT KYIV"),
    ("9–6", "GENOCIDE RULING"),
    ("−4.8%", "NIKKEI FALLS"),
    ("$120bn", "CUT FROM COP31 DRAFT"),
]

# map dots: (story number, longitude, latitude) — only well-separated
# places get a numbered dot; the Europe and USA stories share clusters.
MAP_DOTS = [
    (1, 84.0, 19.5),
    (5, 114.1, 22.5),
    (8, 46.7, 24.7),
]
MAP_EUROPE = [(30.5, 50.4), (4.3, 52.1), (30.7, 36.9), (13.4, 52.5), (12.5, 41.9)]
MAP_USA = [(-74.0, 40.7), (-86.8, 36.2)]
EUROPE_LEGEND = "EUROPE: 2 KYIV · 3 THE HAGUE · 4 ANTALYA · 7 BERLIN · 11 ROME"
USA_LEGEND = "USA: 6 NEW YORK · 12 NASHVILLE"

DATE_CHECK = (
    "DATE CHECK ✓ — Akvan landfall, Kyiv barrage, COP31 final day, markets slide, Houthi strike: "
    "all Friday 20 Nov. Announced Thu 19 Nov: Shenzhen summit, ICJ ruling, UK drone package, "
    "Rose pardon, Senate Iran vote, Anthropic debut, GTA VI launch. LEFT OUT: Kenya's last Ebola "
    "patient went home 11 Nov — not Friday's news. A reported North Korea missile launch could "
    "not be verified — left out. Every number here was checked against the outlet named beside it."
)


# ------------------------------------------------------- illustrations
# Every picture is drawn from shapes: no photos, no copied artwork.

def ill_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=2)
    cx, cy = x + w // 2 - 8, y + h // 2 + 4
    for r, col in ((52, TEAL), (40, BLUE), (28, TEAL), (16, BLUE)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    for dx, dy in ((w - 34, 12), (w - 52, 30), (w - 24, 44)):
        d.line([x + dx, y + dy, x + dx - 5, y + dy + 12], fill=BLUE, width=3)
        d.ellipse([x + dx - 7, y + dy + 13, x + dx - 1, y + dy + 19], fill=BLUE)
    d.text((x + 8, y + h - 20), "BAY OF BENGAL", font=font(10, bold=True), fill=INK)


def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 37, 84), outline=INK, width=2)
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 26), (x, y + h - 40)],
              fill=(52, 68, 120))
    for bx in (x + 30, x + w // 2 - 10, x + w - 70):
        d.arc([bx, y + h - 62, bx + 56, y + h - 6], 180, 360, fill=(226, 232, 240), width=4)
        d.line([bx, y + h - 34, bx + 56, y + h - 34], fill=(226, 232, 240), width=3)
    for sx, sy, ln in ((x + 20, y + 14, 46), (x + 120, y + 8, 60), (x + 230, y + 20, 40)):
        d.line([sx, sy, sx + ln, sy + ln // 2], fill=(251, 146, 60), width=4)
        d.ellipse([sx + ln - 4, sy + ln // 2 - 4, sx + ln + 4, sy + ln // 2 + 4],
                  fill=(253, 224, 71))
    d.text((x + 8, y + h - 20), "DNIPRO · 3 BRIDGES HIT", font=font(10, bold=True),
           fill=(255, 255, 255))


def ill_hague(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.polygon([(x + w // 2 - 62, y + 26), (x + w // 2 + 62, y + 26), (x + w // 2, y + 6)],
              fill=RED)
    for i in range(4):
        cx = x + 52 + i * 62
        d.rectangle([cx, y + 30, cx + 14, y + h - 34], fill=INK)
    d.rectangle([x + 30, y + h - 34, x + w - 30, y + h - 24], fill=INK)
    d.line([x + w // 2, y + 44, x + w // 2, y + 78], fill=GOLD, width=3)
    d.line([x + w // 2 - 34, y + 48, x + w // 2 + 34, y + 48], fill=GOLD, width=3)
    for sgn in (-1, 1):
        px = x + w // 2 + sgn * 34
        d.line([px, y + 48, px, y + 62], fill=GOLD, width=2)
        d.polygon([(px - 13, y + 62), (px + 13, y + 62), (px, y + 76)], fill=GOLD)
    d.text((x + 8, y + h - 20), "9–6 · FIRST OF ITS KIND", font=font(10, bold=True), fill=INK)


def ill_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 252, 231), outline=INK, width=2)
    cx, cy = x + 62, y + h // 2 + 6
    d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], fill=(34, 197, 94), outline=INK, width=2)
    d.arc([cx - 44, cy - 44, cx + 44, cy + 44], 200, 340, fill=INK, width=2)
    d.ellipse([cx - 44, cy - 12, cx + 44, cy + 12], outline=INK, width=2)
    d.line([cx, cy - 44, cx, cy + 44], fill=INK, width=2)
    d.rectangle([x + w - 52, y + 18, x + w - 38, y + h - 22], fill=(255, 255, 255),
                outline=RED, width=2)
    d.ellipse([x + w - 56, y + 8, x + w - 34, y + 30], fill=RED)
    d.line([x + w - 45, y + 30, x + w - 45, y + h - 22], fill=RED, width=4)
    d.text((x + 8, y + h - 20), "1.5°C LIMIT AT RISK", font=font(10, bold=True), fill=INK)


def ill_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    fw, fh, gap = 56, 40, 8
    x0 = x + (w - (3 * fw + 2 * gap)) // 2
    y0 = y + (h - fh) // 2 - 8
    for i in range(7):  # US stripes
        d.rectangle([x0, y0 + i * fh // 7, x0 + fw, y0 + (i + 1) * fh // 7],
                    fill=RED if i % 2 == 0 else PAPER)
    d.rectangle([x0, y0, x0 + 24, y0 + fh * 4 // 7], fill=BLUE)
    cx = x0 + fw + gap  # China
    d.rectangle([cx, y0, cx + fw, y0 + fh], fill=RED)
    for sx, sy in ((8, 8), (22, 6), (26, 14), (22, 22), (8, 20)):
        d.regular_polygon((cx + sx, y0 + sy, 4), 5, rotation=0, fill=(253, 224, 71))
    cx = x0 + 2 * (fw + gap)  # Russia
    for i, col in enumerate((PAPER, BLUE, RED)):
        d.rectangle([cx, y0 + i * fh // 3, cx + fw, y0 + (i + 1) * fh // 3], fill=col)
    d.text((x + 8, y + h - 20), "FIRST THREE-WAY SUMMIT", font=font(10, bold=True), fill=INK)


def ill_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    base = y + h - 30
    vals = [52, 44, 34, 26, 16]
    bw = 22
    x0 = x + 18
    for i, v in enumerate(vals):
        bx = x0 + i * (bw + 8)
        d.rectangle([bx, base - v, bx + bw, base], fill=RED)
    d.line([x + 12, base - 58, x + w - 12, base - 10], fill=INK, width=3)
    d.polygon([(x + w - 12, base - 10), (x + w - 26, base - 16), (x + w - 22, base - 4)],
              fill=INK)
    d.text((x + 8, y + h - 20), "NIKKEI −4.8% · DOW −1,101", font=font(10, bold=True), fill=INK)


def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=2)
    cx, cy = x + w // 2, y + h // 2 - 4
    for dx, dy in ((-34, -22), (34, -22), (-34, 22), (34, 22)):
        d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=3)
        d.ellipse([cx + dx - 13, cy + dy - 4, cx + dx + 13, cy + dy + 4], fill=GREY)
    d.ellipse([cx - 16, cy - 11, cx + 16, cy + 11], fill=INK)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.text((x + 8, y + h - 20), "RANGE 1,000 KM", font=font(10, bold=True), fill=INK)


def ill_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 243, 199), outline=INK, width=2)
    tx = x + w // 2 - 16
    d.polygon([(tx, y + 22), (tx + 32, y + 22), (tx + 16, y + 6)], fill=INK)
    d.rectangle([tx, y + 22, tx + 32, y + h - 22], fill=(148, 163, 184))
    for wy in range(y + 30, y + h - 26, 12):
        d.rectangle([tx + 5, wy, tx + 27, wy + 5], fill=(253, 224, 71))
    d.line([x + 14, y + 12, x + w - 30, y + 40], fill=RED, width=4)
    d.ellipse([x + w - 34, y + 36, x + w - 26, y + 44], fill=RED)
    d.text((x + 8, y + h - 20), "PIF TOWER, RIYADH", font=font(10, bold=True), fill=INK)


def ill_baseball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.line([x + 34, y + h - 16, x + w - 40, y + 22], fill=(146, 64, 14), width=9)
    cx, cy = x + w // 2 + 28, y + h // 2 + 14
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=PAPER, outline=RED, width=2)
    d.arc([cx - 18, cy - 18, cx + 2, cy + 18], 300, 60, fill=RED, width=2)
    d.arc([cx - 2, cy - 18, cx + 18, cy + 18], 120, 240, fill=RED, width=2)
    d.text((x + 8, y + h - 20), "4,256 HITS", font=font(10, bold=True), fill=INK)


def ill_dome(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    cx = x + w // 2
    d.pieslice([cx - 34, y + 14, cx + 34, y + 82], 180, 360, fill=INK)
    d.rectangle([cx - 3, y + 4, cx + 3, y + 16], fill=INK)
    for i in range(3):
        px = cx - 30 + i * 24
        d.rectangle([px, y + 52, px + 10, y + h - 26], fill=INK)
    d.rectangle([cx - 40, y + h - 26, cx + 40, y + h - 18], fill=INK)
    d.text((x + 8, y + h - 20), "62–33 · BIPARTISAN", font=font(10, bold=True), fill=INK)


def ill_phone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=2)
    px, py = x + w // 2 - 24, y + 10
    d.rounded_rectangle([px, py, px + 48, py + 62], 8, fill=INK)
    d.rounded_rectangle([px + 5, py + 8, px + 43, py + 54], 4, fill=PAPER)
    d.ellipse([px + 16, py + 20, px + 32, py + 36], outline=BLUE, width=3)
    d.ellipse([px + 21, py + 25, px + 27, py + 31], fill=BLUE)
    d.text((x + 8, y + h - 20), "€805m FINE", font=font(10, bold=True), fill=INK)


def ill_palm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 237, 213), outline=INK, width=2)
    d.ellipse([x + w - 58, y + 8, x + w - 14, y + 52], fill=(251, 146, 60))
    tx, ty = x + 52, y + h - 24
    d.line([tx, ty, tx + 8, y + 34], fill=(146, 64, 14), width=6)
    for ang, ln in ((-52, 34), (-24, 40), (6, 38), (34, 32), (58, 26)):
        import math
        ex = tx + 8 + ln * math.cos(math.radians(ang - 90))
        ey = y + 34 + ln * math.sin(math.radians(ang - 90)) * 0.6
        d.line([tx + 8, y + 34, ex, ey], fill=(21, 128, 61), width=4)
    d.text((x + 8, y + h - 20), "METACRITIC 99", font=font(10, bold=True), fill=INK)


def ill_sign(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.rectangle([x + w // 2 - 46, y + 10, x + w // 2 + 46, y + 44], fill=RED)
    d.text((x + w // 2 - 30, y + 14), "STRIKE", font=font(15, bold=True),
           fill=(255, 255, 255))
    d.line([x + w // 2, y + 44, x + w // 2, y + h - 22], fill=INK, width=4)
    for dx in (-52, -26, 26, 52):
        d.ellipse([x + w // 2 + dx - 7, y + h - 30, x + w // 2 + dx + 7, y + h - 16],
                  fill=INK)
    d.text((x + 8, y + h - 20), "25+ COUNTRIES", font=font(10, bold=True), fill=INK)


ILL = {1: ill_cyclone, 2: ill_kyiv, 3: ill_hague, 4: ill_cop, 5: ill_flags,
       6: ill_chart, 7: ill_drone, 8: ill_tower, 9: ill_baseball, 10: ill_dome,
       11: ill_phone, 12: ill_palm, 13: ill_sign}


# ------------------------------------------------------------- world map
# Coarse continent outlines in (lon, lat); equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-82, 66), (-76, 62),
     (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-84, 30), (-90, 21), (-97, 26), (-105, 30), (-117, 34),
     (-124, 42), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-79, 9), (-62, 9), (-52, 5), (-50, -5), (-40, -10), (-35, -18),
     (-40, -28), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-74, -44),
     (-73, -30), (-77, -18), (-81, -6), (-80, 2)],
    [(-17, 15), (-10, 30), (-6, 35), (10, 37), (20, 32), (32, 31),
     (35, 28), (43, 12), (48, 11), (51, 12), (44, -2), (40, -12),
     (36, -20), (33, -28), (26, -34), (19, -35), (15, -27), (12, -17),
     (9, -2), (9, 4), (-8, 5)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 58),
     (18, 56), (21, 55), (24, 59), (28, 62), (30, 70), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (100, 77), (120, 73), (140, 72),
     (160, 70), (178, 66), (178, 62), (162, 60), (158, 52), (142, 50),
     (140, 40), (132, 35), (127, 35), (122, 31), (120, 25), (110, 20),
     (108, 12), (105, 9), (100, 8), (97, 8), (94, 17), (91, 22), (88, 22),
     (86, 20), (80, 13), (77, 8), (74, 20), (70, 22), (66, 25), (61, 25),
     (57, 26), (52, 26), (48, 29), (44, 29), (40, 31), (36, 36), (30, 36),
     (27, 40), (23, 36), (19, 42), (15, 44), (12, 44), (8, 44), (3, 43),
     (-1, 44), (-2, 48)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (153, -24), (146, -19),
     (142, -11), (137, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    lon0, lon1, lat0, lat1 = -170, 190, 72, -55

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=GREY)
    for lon, lat in MAP_EUROPE + MAP_USA:
        px, py = proj(lon, lat)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED, outline=PAPER, width=1)
    d.text((x + 6, y + h - 24), EUROPE_LEGEND, font=font(8, bold=True), fill=INK)
    d.text((x + 6, y + h - 13), USA_LEGEND, font=font(8, bold=True), fill=INK)
    for n, lon, lat in MAP_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=PAPER, width=1)
        f = font(9, bold=True)
        tw = f.getlength(str(n))
        d.text((px - tw / 2, py - 6), str(n), font=f, fill=(255, 255, 255))


# -------------------------------------------------------------- layout

def region_line():
    counts = {r: 0 for r in REGIONS}
    for s in BIG + SMALL:
        counts[s["region"]] += 1
    for _n, region, _t, _s in BRIEFS:
        counts[region] += 1
    total = sum(counts.values())
    assert total == 33, total
    parts = ["%s %d" % (r, counts[r]) for r in REGIONS]
    return "  ·  ".join(parts) + "   —   33 STORIES COUNTED"


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=INK)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(44, serif=True)
    d.text(((W - tf.getlength(title)) / 2, 12), title, font=tf, fill=INK)
    df = font(16, bold=True)
    d.text((16, 64), "FRIDAY 20 NOVEMBER 2026", font=df, fill=RED)
    rf = font(13, bold=True)
    right = "33 STORIES · 6 CONTINENTS · ALL FROM THIS ONE DAY"
    d.text((1008 - rf.getlength(right), 66), right, font=rf, fill=INK)
    rule(d, 88, 3)
    rule(d, 93, 1)

    # big-number strip
    bw, gap = 192, 8
    for i, (num, label) in enumerate(BIG_NUMBERS):
        x = 16 + i * (bw + gap)
        d.rectangle([x, 99, x + bw, 155], fill=PANEL, outline=INK, width=1)
        nf = font(24, bold=True)
        d.text((x + (bw - nf.getlength(num)) / 2, 105), num, font=nf, fill=RED)
        lf = font(10, bold=True)
        d.text((x + (bw - lf.getlength(label)) / 2, 136), label, font=lf, fill=INK)
    cf = font(11)
    rl = region_line()
    d.text(((W - cf.getlength(rl)) / 2, 161), rl, font=cf, fill=GREY)
    rule(d, 178, 2)

    # big three
    colw = 325
    for i, s in enumerate(BIG):
        x = 16 + i * (colw + 8)
        d.text((x, 186), s["kick"], font=font(11, bold=True), fill=RED)
        ILL[s["n"]](d, x, 202, colw, 148)
        y = block(d, x, 356, s["head"], font(19, bold=True), colw, leading=23,
                  max_lines=2)
        y = block(d, x, y + 4, s["body"], font(12), colw, leading=15, max_lines=5)
        d.text((x, 470), s["src"], font=font(9, bold=True), fill=GREY)
    rule(d, 490, 2)

    # ten more, drawn
    d.text((16, 498), "TEN MORE, DRAWN", font=font(15, bold=True), fill=INK)
    note = "EVERY PICTURE DRAWN FROM THE REPORT"
    d.text((1008 - font(10).getlength(note), 502), note, font=font(10), fill=GREY)
    cw, cg = 190, 10
    for i, s in enumerate(SMALL):
        col, row = i % 5, i // 5
        x = 16 + col * (cw + cg)
        y0 = 522 + row * 110
        SMALL_ILL[s["n"]](d, x, y0, cw, 40)
        block(d, x, y0 + 44, s["head"], font(12, bold=True), cw, leading=14,
              max_lines=2)
        block(d, x, y0 + 74, s["body"], font(10), cw, leading=12, max_lines=2)
        d.text((x, y0 + 100), s["src"], font=font(8, bold=True), fill=GREY)
    rule(d, 748, 2)

    # map + briefs
    d.text((16, 756), "WHERE IT HAPPENED", font=font(13, bold=True), fill=INK)
    d.text((342, 756), "ALSO ON FRIDAY — 20 MORE IN BRIEF", font=font(13, bold=True),
           fill=INK)
    draw_map(d, 16, 778, 314, 140)
    bf = font(10)
    for i, (n, _region, text, src) in enumerate(BRIEFS):
        col, row = i // 10, i % 10
        x = 342 + col * 340
        y = 780 + row * 14
        d.text((x, y), "%d." % n, font=font(10, bold=True), fill=RED)
        d.text((x + 20, y), text, font=bf, fill=INK)
    rule(d, 926, 2)

    # date check
    d.rectangle([16, 932, 1008, 994], fill=YELLOW, outline=INK, width=1)
    block(d, 26, 938, DATE_CHECK, font(11), 962, leading=14, max_lines=4)
    ff = font(10, bold=True)
    foot = "ALL STORIES FROM FRIDAY 20 NOVEMBER 2026 · SOURCES NAMED BESIDE EACH STORY"
    d.text(((W - ff.getlength(foot)) / 2, 1000), foot, font=ff, fill=GREY)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)
    return img


def main():
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, "PNG")
    print("wrote %s  %dx%d  %d bytes" % (out, img.width, img.height,
                                         os.path.getsize(out)))


# ------------------------------------------- compact illustrations (190x40)
# Small emblems for the ten drawn briefs: same subjects, simplified.

def s_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=1)
    cx, cy = x + 34, y + h // 2
    for r, col in ((15, TEAL), (10, BLUE), (5, TEAL)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    for dx in (86, 104, 122):
        d.line([x + dx, y + 8, x + dx - 4, y + 20], fill=BLUE, width=3)
        d.ellipse([x + dx - 6, y + 21, x + dx - 1, y + 26], fill=BLUE)
    d.text((x + 140, y + 12), "90 km/h", font=font(10, bold=True), fill=INK)


def s_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 37, 84), outline=INK, width=1)
    for bx in (x + 16, x + 78, x + 140):
        d.arc([bx, y + h - 22, bx + 40, y + h + 2], 180, 360,
              fill=(226, 232, 240), width=3)
    d.line([x + 20, y + 8, x + 52, y + 20], fill=(251, 146, 60), width=3)
    d.line([x + 110, y + 6, x + 150, y + 18], fill=(253, 224, 71), width=3)


def s_hague(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    d.polygon([(x + 22, y + 12), (x + 66, y + 12), (x + 44, y + 2)], fill=RED)
    for i in range(3):
        cx = x + 28 + i * 16
        d.rectangle([cx, y + 13, cx + 7, y + h - 6], fill=INK)
    d.line([x + 96, y + 8, x + 96, y + 30], fill=GOLD, width=2)
    d.line([x + 84, y + 11, x + 108, y + 11], fill=GOLD, width=2)
    d.polygon([(x + 80, y + 22), (x + 88, y + 22), (x + 84, y + 30)], fill=GOLD)
    d.polygon([(x + 104, y + 22), (x + 112, y + 22), (x + 108, y + 30)], fill=GOLD)
    d.text((x + 122, y + 12), "9–6", font=font(13, bold=True), fill=INK)


def s_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 252, 231), outline=INK, width=1)
    cx, cy = x + 34, y + h // 2
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(34, 197, 94), outline=INK,
              width=1)
    d.ellipse([cx - 15, cy - 4, cx + 15, cy + 4], outline=INK, width=1)
    d.line([cx, cy - 15, cx, cy + 15], fill=INK, width=1)
    d.rectangle([x + 84, y + 10, x + 92, y + h - 8], fill=PAPER, outline=RED, width=1)
    d.ellipse([x + 82, y + 4, x + 94, y + 14], fill=RED)
    d.text((x + 102, y + 12), "1.5°C", font=font(11, bold=True), fill=INK)


def s_flags(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    fw, fh = 44, 26
    x0, y0 = x + 14, y + (h - fh) // 2
    for i in range(7):
        d.rectangle([x0, y0 + i * fh // 7, x0 + fw, y0 + (i + 1) * fh // 7],
                    fill=RED if i % 2 == 0 else PAPER)
    d.rectangle([x0, y0, x0 + 18, y0 + fh * 4 // 7], fill=BLUE)
    cx = x0 + fw + 10
    d.rectangle([cx, y0, cx + fw, y0 + fh], fill=RED)
    d.regular_polygon((cx + 10, y0 + 9, 4), 5, fill=(253, 224, 71))
    cx = x0 + 2 * (fw + 10)
    for i, col in enumerate((PAPER, BLUE, RED)):
        d.rectangle([cx, y0 + i * fh // 3, cx + fw, y0 + (i + 1) * fh // 3], fill=col)


def s_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    base = y + h - 8
    vals = [24, 19, 13, 8]
    for i, v in enumerate(vals):
        bx = x + 22 + i * 26
        d.rectangle([bx, base - v, bx + 16, base], fill=RED)
    d.line([x + 14, base - 28, x + 118, base - 6], fill=INK, width=2)
    d.text((x + 128, y + 12), "−4.8%", font=font(11, bold=True), fill=RED)


def s_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=1)
    cx, cy = x + 40, y + h // 2
    for dx, dy in ((-20, -11), (20, -11), (-20, 11), (20, 11)):
        d.line([cx, cy, cx + dx, cy + dy], fill=INK, width=2)
        d.ellipse([cx + dx - 8, cy + dy - 2, cx + dx + 8, cy + dy + 2], fill=GREY)
    d.ellipse([cx - 9, cy - 6, cx + 9, cy + 6], fill=INK)
    d.text((x + 76, y + 12), "1,000 km", font=font(11, bold=True), fill=INK)


def s_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(254, 243, 199), outline=INK, width=1)
    tx = x + 30
    d.polygon([(tx, y + 8), (tx + 18, y + 8), (tx + 9, y + 2)], fill=INK)
    d.rectangle([tx, y + 8, tx + 18, y + h - 4], fill=(148, 163, 184))
    for wy in range(y + 12, y + h - 6, 7):
        d.rectangle([tx + 3, wy, tx + 15, wy + 3], fill=(253, 224, 71))
    d.line([x + 62, y + 6, x + 96, y + 22], fill=RED, width=3)
    d.text((x + 106, y + 12), "RIYADH", font=font(11, bold=True), fill=INK)


def s_baseball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    d.line([x + 16, y + h - 8, x + 66, y + 8], fill=(146, 64, 14), width=6)
    cx, cy = x + 92, y + h // 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=PAPER, outline=RED, width=2)
    d.arc([cx - 9, cy - 9, cx + 1, cy + 9], 300, 60, fill=RED, width=2)
    d.arc([cx - 1, cy - 9, cx + 9, cy + 9], 120, 240, fill=RED, width=2)
    d.text((x + 116, y + 12), "4,256", font=font(11, bold=True), fill=INK)


def s_dome(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    cx = x + 40
    d.pieslice([cx - 18, y + 6, cx + 18, y + 42], 180, 360, fill=INK)
    for i in range(3):
        px = cx - 16 + i * 13
        d.rectangle([px, y + 26, px + 6, y + h - 6], fill=INK)
    d.text((x + 70, y + 12), "62–33", font=font(12, bold=True), fill=INK)


def s_phone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(224, 242, 254), outline=INK, width=1)
    px, py = x + 26, y + 5
    d.rounded_rectangle([px, py, px + 24, py + 30], 4, fill=INK)
    d.rounded_rectangle([px + 3, py + 4, px + 21, py + 26], 2, fill=PAPER)
    d.ellipse([px + 8, py + 10, px + 16, py + 18], outline=BLUE, width=2)
    d.text((x + 62, y + 12), "€805m", font=font(12, bold=True), fill=INK)


def s_palm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 237, 213), outline=INK, width=1)
    d.ellipse([x + 118, y + 4, x + 140, y + 26], fill=(251, 146, 60))
    tx, ty = x + 40, y + h - 4
    d.line([tx, ty, tx + 5, y + 12], fill=(146, 64, 14), width=4)
    import math
    for ang, ln in ((-50, 20), (-18, 23), (12, 22), (42, 18)):
        ex = tx + 5 + ln * math.cos(math.radians(ang - 90))
        ey = y + 12 + ln * math.sin(math.radians(ang - 90)) * 0.6
        d.line([tx + 5, y + 12, ex, ey], fill=(21, 128, 61), width=3)
    d.text((x + 150, y + 12), "99", font=font(13, bold=True), fill=INK)


def s_sign(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=1)
    d.rectangle([x + 16, y + 6, x + 84, y + 24], fill=RED)
    d.text((x + 24, y + 9), "STRIKE", font=font(11, bold=True), fill=(255, 255, 255))
    d.line([x + 50, y + 24, x + 50, y + h - 4], fill=INK, width=3)
    for dx in (110, 132, 154):
        d.ellipse([x + dx - 5, y + h - 12, x + dx + 5, y + h - 2], fill=INK)
    d.text((x + 164, y + 12), "25+", font=font(11, bold=True), fill=INK)


SMALL_ILL = {4: s_cop, 5: s_flags, 6: s_chart, 7: s_drone, 8: s_tower,
             9: s_baseball, 10: s_dome, 11: s_phone, 12: s_palm, 13: s_sign,
             1: s_cyclone, 2: s_kyiv, 3: s_hague}


if __name__ == "__main__":
    main()
