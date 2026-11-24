#!/usr/bin/env python3
"""Render the news-image-20261123 v2 poster: Monday 23 November 2026.

Local build tool only (Pillow + DejaVu). The graded entry is main.py,
which copies the bundled entry.png to /output/entry.png, stdlib only.

v2 rebuilds the poster from scratch after a verification pass found 28 of
v1's 39 stories wrongly dated (including the lead and three auto-loss
stories from before 13 Nov). Every story here was checked against a
primary source for its UTC date before inclusion: it happened, or was
first reported, on Monday 23 November 2026. See NOTES-v2.md for the
per-story source and date.

Layout: giant date masthead, 3-headline ticker, BY THE NUMBERS strip,
region bar, UTC timeline, 3 illustrated leads, 10 small illustrated
cards, world map + ALSO ON list, DATE CHECK box, HOW SURE legend,
sources footer. Cream newspaper theme, dark text. 39 stories.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
M = 22                       # side margin
CW = W - 2 * M               # content width = 980

PAPER = (247, 242, 230)
PANEL = (255, 252, 245)
INK = (28, 26, 22)
MUTED = (96, 89, 76)
RULE = (74, 66, 54)
RED = (164, 24, 34)
BLUE = (31, 78, 121)
SEA = (210, 228, 238)
LAND = (232, 219, 190)
LAND_EDGE = (178, 162, 126)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

F_MAST = font(SERIF_B, 38)
F_SUB = font(SANS_B, 10)
F_TICK = font(SANS_B, 12)
F_SEC = font(SANS_B, 11)
F_NUM_BIG = font(SANS_B, 21)
F_NUM_CAP = font(SANS, 9)
F_REG = font(SANS_B, 10)
F_TL_T = font(SANS_B, 10)
F_TL_E = font(SANS, 9)
F_TAG = font(SANS_B, 9)
F_LEAD_H = font(SERIF_B, 17)
F_LEAD_B = font(SANS, 10)
F_CARD_H = font(SANS_B, 11)
F_CARD_B = font(SANS, 9)
F_ALSO = font(SANS, 9)
F_ALSO_N = font(SANS_B, 9)
F_DC = font(SANS, 9)
F_DC_B = font(SANS_B, 9)
F_FOOT = font(SANS, 9)
F_FOOT_B = font(SANS_B, 10)
F_MAP_T = font(SANS_B, 11)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    if leading is None:
        leading = fnt.size + 3
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(d, x0, y, x1, width=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag_chip(d, x, y, text, color):
    """Small coloured tag; returns width used."""
    w = int(d.textlength(text, font=F_TAG)) + 12
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=color)
    d.text((x + 6, y + 2), text, font=F_TAG, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------------ regions
REGIONS = [
    ("EUROPE", (31, 78, 121)),
    ("MIDDLE EAST", (178, 96, 26)),
    ("ASIA-PACIFIC", (104, 44, 143)),
    ("AMERICAS", (164, 24, 34)),
    ("AFRICA", (30, 122, 52)),
    ("OCEANIA", (14, 124, 123)),
    ("SPORT", (123, 94, 0)),
    ("WORLD", (70, 70, 70)),
]
REGION_COLOR = dict(REGIONS)


# ------------------------------------------------------------------ stories
# Every story: number, region, headline, body, (lon, lat) map pin, art key.
# All dates verified against primary sources; see NOTES-v2.md.
LEADS = [
    {
        "n": 1, "region": "EUROPE", "lon": 20.1, "lat": 32.1,
        "tag": "WAR AT SEA  \u2022  OFF LIBYA",
        "head": "Ukraine sinks Russian corvette off Libya",
        "body": ("President Zelenskiy announced on Monday that seven "
                 "Ukrainian sea drones sank the Russian corvette Merkury "
                 "(commissioned 2023) off Benghazi, Libya. A Ka-27 "
                 "helicopter aboard was destroyed, and the cargo ship "
                 "MV Angara was hit. The strike was on the night of "
                 "21\u201322 Nov; the UN mission in Libya wants an "
                 "independent investigation."),
        "ill": "ship",
    },
    {
        "n": 2, "region": "EUROPE", "lon": 10.0, "lat": 54.0,
        "tag": "NATO  \u2022  BRUSSELS",
        "head": "NATO council meets over Poland missiles",
        "body": ("NATO's North Atlantic Council met in emergency session "
                 "in Brussels on Monday after Russian missiles fell in "
                 "Poland on Friday. Secretary General Mark Rutte said on "
                 "Saturday the alliance will defend every inch of Polish "
                 "territory. Poland said three Russian objects \u2014 "
                 "likely two Kh-101 missiles and a drone \u2014 violated "
                 "its airspace; bad weather prevented interception."),
        "ill": "nato",
    },
    {
        "n": 3, "region": "EUROPE", "lon": 30.2, "lat": 50.9,
        "tag": "KYIV  \u2022  DYMER",
        "head": "11 killed as Russian drones hit Dymer flats",
        "body": ("The death toll from a Russian drone strike on a "
                 "five-storey block in Dymer, Kyiv region, reached 11 "
                 "on Monday morning, a teenager among the dead. The "
                 "block was hit early Sunday in a 186-drone wave; a "
                 "seven-year-old was pulled alive from the rubble. "
                 "Separately, Russia launched 153 drones overnight; "
                 "134 were shot down or jammed."),
        "ill": "flats",
    },
]

CARDS = [
    {
        "n": 4, "region": "AMERICAS", "lon": -122.0, "lat": 37.4,
        "tag": "TECH", "head": "Nvidia board reinstates Jensen Huang as CEO",
        "body": ("Huang returns 11 days after resigning over an affair; "
                 "Trump called into the board meeting. Shares jumped 30%."),
        "ill": "chip",
    },
    {
        "n": 5, "region": "SPORT", "lon": 0.0, "lat": 47.0,
        "tag": "FOOTBALL", "head": "UK to host 2035 Women's World Cup, FIFA confirms",
        "body": ("First World Cup on UK soil since 1966. A US-led bid "
                 "gets the 2031 edition."),
        "ill": "football",
    },
    {
        "n": 6, "region": "EUROPE", "lon": 42.0, "lat": 46.0,
        "tag": "UKRAINE", "head": "Ukraine hits three Russian oil sites overnight",
        "body": ("Novoshakhtinsk, Lukoil Perm refineries and Kaleikino "
                 "station hit."),
        "ill": "refinery",
    },
    {
        "n": 7, "region": "ASIA-PACIFIC", "lon": 106.2, "lat": -6.1,
        "tag": "INDONESIA", "head": "Cikande factory fire: 24 killed, dozens missing",
        "body": ("Fire at a Cikande confectionery factory: 24 killed, "
                 "about 30 unaccounted for."),
        "ill": "fire",
    },
    {
        "n": 8, "region": "AMERICAS", "lon": -77.0, "lat": 38.9,
        "tag": "US POLITICS", "head": "Democrats clinch 258 House seats \u2014 biggest since 1992",
        "body": ("Best House result in decades; 47 seats flipped from "
                 "Republicans."),
        "ill": "capitol",
    },
    {
        "n": 9, "region": "ASIA-PACIFIC", "lon": 77.2, "lat": 28.6,
        "tag": "NEPAL\u2013INDIA", "head": "Nepal PM Balen Shah meets Modi in Delhi",
        "body": ("Bilateral talks on Monday: MoUs signed and a NPR 24,000 "
                 "crore package announced."),
        "ill": "flags",
    },
    {
        "n": 10, "region": "MIDDLE EAST", "lon": 34.5, "lat": 31.4,
        "tag": "GAZA", "head": "Gaza a 'toxic wasteland', experts find",
        "body": ("A new report finds toxic contamination across 99% of "
                 "Gaza after two years of war."),
        "ill": "rubble",
    },
    {
        "n": 11, "region": "ASIA-PACIFIC", "lon": 127.0, "lat": 37.5,
        "tag": "MARKETS", "head": "Asian chip stocks slide as AI rout spreads",
        "body": ("Kospi fell as much as 5.8% on Monday, closing down 3.3%; "
                 "Samsung \u22123.1%, SK Hynix \u22122.5%."),
        "ill": "chart",
    },
    {
        "n": 12, "region": "EUROPE", "lon": -8.0, "lat": 57.0,
        "tag": "MANCHESTER", "head": "Don Toliver concert evacuated after gas scare",
        "body": ("Co-op Live evacuated on Sunday night; London O2 show "
                 "postponed on Monday. One person hospitalised."),
        "ill": "arena",
    },
    {
        "n": 13, "region": "AMERICAS", "lon": -82.4, "lat": 23.1,
        "tag": "CUBA", "head": "WHO chief visits Cuba as health system breaks down",
        "body": ("The WHO director-general visited Cuba on Monday as the "
                 "island's healthcare system breaks down."),
        "ill": "clinic",
    },
]

# ALSO ON — numbered 14..39, short one-liners, two columns.
ALSO = [
    (14, "MIDDLE EAST", "Iran: will use 'all tools' vs US naval blockade"),
    (15, "EUROPE", "Russia lost 2,471 troops in a day, Kyiv claims"),
    (16, "OCEANIA", "Australia: calls for Bowen to quit after COP31"),
    (17, "AMERICAS", "US Army plans Iowa lead blast despite court order"),
    (18, "AMERICAS", "CrowdStrike to buy Zscaler in $43.9B all-stock deal"),
    (19, "MIDDLE EAST", "US discussing military training for Syrian forces"),
    (20, "AMERICAS", "US flash PMI eases to 54.6, a four-month low"),
    (21, "EUROPE", "GTA 6 hacker Kurtaj released on licence"),
    (22, "EUROPE", "Capita shares plunge 70% as boss quits"),
    (23, "SPORT", "Tyson Fury reveals schizophrenia diagnosis"),
    (24, "AMERICAS", "Amazon snaps up Decart's AI tech for $7.5B"),
    (25, "EUROPE", "BAFTA loses headline sponsor EE after 30 years"),
    (26, "EUROPE", "Burnham sets out 'landmark' UK-EU deal to MPs"),
    (27, "EUROPE", "Asylum seekers removed from UK faced 'intimidating' force"),
    (28, "AFRICA", "UN mission urges probe into Benghazi port attacks"),
    (29, "AMERICAS", "Trump vows 10% cap on credit card rates"),
    (30, "ASIA-PACIFIC", "Okinawa's Shuri Castle main hall reopens to public"),
    (31, "AMERICAS", "ICE detains father & daughter at Seattle airport"),
    (32, "AMERICAS", "Democrats plan 12 debates for 2028 primary"),
    (33, "EUROPE", "UK gigafactory plan in turmoil, loses 2nd builder"),
    (34, "AMERICAS", "Trump admin deported US citizen to Mexico, DoJ admits"),
    (35, "EUROPE", "European gas prices surge on cold snap fears"),
    (36, "OCEANIA", "Jetstar class action: 1.1m eligible over Covid refunds"),
    (37, "AMERICAS", "100+ writers form PEN America splinter group over Gaza"),
    (38, "WORLD", "US futures climb; world shares mixed as tech falls in Asia"),
    (39, "ASIA-PACIFIC", "Thai court cuts MP's royal defamation term to 3 years"),
]

NUMBERS = [
    ("7", "Ukrainian sea drones that sank the corvette Merkury"),
    ("153", "Russian drones launched overnight; 134 shot down or jammed"),
    ("258", "House seats won by Democrats, the most since 1992"),
    ("$43.9B", "CrowdStrike's all-stock deal to buy Zscaler"),
    ("24", "killed in the Cikande factory fire; about 30 missing"),
    ("2,471", "Russian troops lost in a day, Kyiv claims"),
]

TIMELINE = [
    ("~05:23", "Dymer death toll confirmed at 11"),
    ("~07:28", "Kyiv: Russia lost 2,471 troops in a day"),
    ("~09:15", "Zelenskiy confirms Merkury sinking"),
    ("~12:00", "NATO council meets in Brussels"),
    ("14:45", "US flash PMI falls to 54.6"),
    ("15:09", "FIFA confirms UK hosts 2035 Women's World Cup"),
]

DATE_CHECK = (
    "NOT from today \u2014 left out on purpose: COP31 collapsed Sunday in "
    "Antalya; Verstappen won the Las Vegas GP on Saturday night; Alcaraz "
    "won the ATP Finals on Sunday; the missiles that fell in Poland were "
    "Friday 20 Nov (today is the NATO meeting, not the strike); Bolsonaro "
    "entered ICU Friday 20 Nov; Russia's 186-drone attack was the night of "
    "21\u201322 Nov (today: 153 drones, Dymer toll). Merkury sank 21\u201322 "
    "Nov, announced Monday; the Cikande fire broke out Saturday, 24 dead "
    "confirmed Monday."
)

HOW_SURE = (
    ("CONFIRMED", "Merkury, Dymer toll, Cikande 24, Huang, FIFA."),
    ("OFFICIAL", "Zelenskiy, NATO, AP on 258 seats, Reuters PMI."),
    ("CLAIM", "2,471 troops/day (Kyiv); Iran 'all tools' (Tehran)."),
)


# ------------------------------------------------------------ illustrations
# Every illustration is an informative scene from the event itself:
# a place, a ship, a building, a court — never a logo or decoration.

def _sky(d, x, y, w, h, top, bot):
    """Vertical gradient sky."""
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def _smoke(d, cx, cy, s):
    """A small cluster of smoke puffs above (cx, cy)."""
    for dx, dy, r, col in ((-s, -s, s, (150, 148, 145)),
                           (0, -s * 2, s + 2, (120, 118, 115)),
                           (s, -s, s - 1, (150, 148, 145)),
                           (0, -s * 3, s, (105, 103, 100))):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=col)


def _flame(d, cx, cy, r):
    """A small stylised flame centred at (cx, cy)."""
    d.polygon([(cx - r, cy + r), (cx - r * 0.4, cy - r), (cx, cy - r * 1.6),
               (cx + r * 0.4, cy - r), (cx + r, cy + r)],
              fill=(232, 110, 20))
    d.polygon([(cx - r * 0.5, cy + r * 0.6), (cx, cy - r * 0.8),
               (cx + r * 0.5, cy + r * 0.6)], fill=(255, 210, 80))


def ill_ship(d, x, y, w, h):
    """Burning corvette Merkury off Benghazi, sea drones alongside."""
    _sky(d, x, y, w, h, (198, 214, 226), (150, 178, 196))
    sea_y = y + h * 0.62
    d.rectangle([x, sea_y, x + w, y + h], fill=(52, 96, 128))
    for k in range(5):
        wx = x + 12 + k * (w - 24) // 5
        d.arc([wx, sea_y + 6, wx + 26, sea_y + 16], 180, 360,
              fill=(200, 220, 232), width=2)
    # hull, listing and burning
    d.polygon([(x + 20, sea_y - 4), (x + w - 20, sea_y - 4),
               (x + w - 40, sea_y + 16), (x + 44, sea_y + 16)],
              fill=(52, 56, 62))
    d.rectangle([x + 70, sea_y - 26, x + 150, sea_y - 4], fill=(74, 78, 84))
    d.rectangle([x + 160, sea_y - 34, x + 176, sea_y - 4], fill=(74, 78, 84))
    d.polygon([(x + 176, sea_y - 34), (x + 190, sea_y - 18),
               (x + 176, sea_y - 18)], fill=(164, 24, 34))
    _smoke(d, x + 110, sea_y - 30, 12)
    _flame(d, x + 200, sea_y - 8, 12)
    _flame(d, x + 90, sea_y - 6, 9)
    # two sea drones closing in
    for dx in (x + 40, x + w - 60):
        d.ellipse([dx, sea_y + 8, dx + 22, sea_y + 16], fill=(30, 30, 30))
        d.line([(dx + 11, sea_y + 8), (dx + 11, sea_y - 2)],
               fill=(30, 30, 30), width=2)
    d.text((x + 10, y + 8), "BENGHAZI  \u2022  LIBYA",
           font=font(SANS_B, 10), fill=(28, 26, 22))


def ill_nato(d, x, y, w, h):
    """NATO star over a council table in Brussels."""
    _sky(d, x, y, w, h, (226, 220, 205), (200, 190, 168))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(96, 72, 46))
    for k in range(6):
        kx = x + 14 + k * (w - 28) // 6
        d.rectangle([kx, y + h - 34, kx + 16, y + h - 22],
                    fill=(140, 116, 78))
        d.ellipse([kx + 4, y + h - 44, kx + 12, y + h - 36],
                  fill=(60, 48, 36))
    cx, cy = x + w * 0.5, y + h * 0.32
    r = h * 0.24
    pts = []
    import math
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(31, 78, 121))
    d.text((x + 10, y + 6), "BRUSSELS", font=font(SANS_B, 10),
           fill=(28, 26, 22))


def ill_flats(d, x, y, w, h):
    """Five-storey block in Dymer, middle floors blown out, smoke rising."""
    _sky(d, x, y, w, h, (46, 52, 66), (120, 116, 108))
    bx, bw = x + w * 0.28, w * 0.5
    by, bh = y + 8, h - 8
    d.rectangle([bx, by, bx + bw, by + bh], fill=(168, 152, 128))
    for fl in range(5):
        fy = by + 6 + fl * ((bh - 12) / 5)
        for col in range(4):
            wx = bx + 8 + col * ((bw - 16) / 4)
            d.rectangle([wx, fy, wx + (bw - 16) / 4 - 5, fy + 12],
                        fill=(255, 222, 140))
    # blast damage across the middle floors
    d.polygon([(bx + bw * 0.2, by + bh * 0.35), (bx + bw * 0.8, by + bh * 0.35),
               (bx + bw * 0.7, by + bh * 0.62),
               (bx + bw * 0.3, by + bh * 0.62)], fill=(38, 34, 30))
    d.polygon([(bx + bw * 0.35, by + bh * 0.35), (bx + bw * 0.55, by + bh * 0.35),
               (bx + bw * 0.5, by + bh * 0.5)], fill=(232, 110, 20))
    _smoke(d, bx + bw * 0.5, by + bh * 0.3, 11)
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 6], fill=(70, 66, 60))
    d.text((x + 10, y + 6), "DYMER, KYIV REGION", font=font(SANS_B, 10),
           fill=(255, 252, 245))


def ill_chip(d, x, y, w, h):
    """A microchip: dark die, gold pins, green board."""
    _sky(d, x, y, w, h, (30, 46, 36), (52, 74, 58))
    cx, cy = x + w * 0.5, y + h * 0.5
    s = min(w, h) * 0.42
    # pins
    for k in range(5):
        px = cx - s + k * (2 * s) / 4
        d.rectangle([px - 2, cy - s - 8, px + 2, cy - s], fill=(212, 175, 55))
        d.rectangle([px - 2, cy + s, px + 2, cy + s + 8], fill=(212, 175, 55))
        py = cy - s + k * (2 * s) / 4
        d.rectangle([cx - s - 8, py - 2, cx - s, py + 2], fill=(212, 175, 55))
        d.rectangle([cx + s, py - 2, cx + s + 8, py + 2], fill=(212, 175, 55))
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(24, 24, 28),
                outline=(212, 175, 55), width=2)
    d.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                fill=(40, 110, 60))
    d.text((cx - s * 0.3, cy - 6), "AI", font=font(SANS_B, 12),
           fill=(255, 255, 255))


def ill_football(d, x, y, w, h):
    """A football pitch from above, ball on the spot, goal at the end."""
    _sky(d, x, y, w, h, (96, 160, 90), (70, 130, 66))
    d.rectangle([x + 6, y + 4, x + w - 6, y + h - 4], outline=(255, 255, 255),
                width=2)
    d.line([(x + w * 0.5, y + 4), (x + w * 0.5, y + h - 4)],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.5 - 14, y + h * 0.5 - 14, x + w * 0.5 + 14,
               y + h * 0.5 + 14], outline=(255, 255, 255), width=2)
    d.rectangle([x + w - 22, y + h * 0.3, x + w - 6, y + h * 0.7],
                outline=(255, 255, 255), width=2)
    d.ellipse([x + w * 0.62 - 6, y + h * 0.5 - 6, x + w * 0.62 + 6,
               y + h * 0.5 + 6], fill=(255, 255, 255), outline=(28, 26, 22))
    d.polygon([(x + w * 0.62, y + h * 0.5 - 3),
               (x + w * 0.62 + 3, y + h * 0.5 + 2),
               (x + w * 0.62 - 3, y + h * 0.5 + 2)], fill=(28, 26, 22))


def ill_refinery(d, x, y, w, h):
    """Refinery towers at night, one tank burning."""
    _sky(d, x, y, w, h, (60, 56, 52), (120, 108, 96))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(50, 46, 42))
    for k in range(3):
        tx = x + 12 + k * 34
        d.polygon([(tx, y + h - 10), (tx + 6, y + 8), (tx + 14, y + 8),
                   (tx + 20, y + h - 10)], fill=(150, 140, 125))
        _smoke(d, tx + 10, y + 10, 6)
    d.rectangle([x + w - 46, y + h * 0.4, x + w - 14, y + h - 10],
                fill=(110, 100, 86))
    _flame(d, x + w - 30, y + h * 0.4, 10)


def ill_fire(d, x, y, w, h):
    """Factory building on fire, thick smoke."""
    _sky(d, x, y, w, h, (70, 60, 54), (140, 120, 100))
    d.rectangle([x + 14, y + h * 0.45, x + w - 14, y + h - 6],
                fill=(120, 104, 84))
    d.rectangle([x + 14, y + h * 0.45, x + w - 14, y + h * 0.55],
                fill=(90, 78, 62))
    _flame(d, x + w * 0.35, y + h * 0.45, 12)
    _flame(d, x + w * 0.65, y + h * 0.45, 9)
    _smoke(d, x + w * 0.5, y + h * 0.3, 10)


def ill_capitol(d, x, y, w, h):
    """US Capitol dome against a pale sky."""
    _sky(d, x, y, w, h, (214, 222, 232), (178, 192, 208))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 130, 120))
    cx = x + w * 0.5
    base_y = y + h - 10
    d.rectangle([cx - 52, base_y - 16, cx + 52, base_y], fill=(240, 238, 230))
    d.rectangle([cx - 34, base_y - 30, cx + 34, base_y - 16],
                fill=(240, 238, 230))
    d.pieslice([cx - 22, base_y - 56, cx + 22, base_y - 12], 180, 360,
               fill=(240, 238, 230), outline=(150, 150, 150))
    d.rectangle([cx - 2, base_y - 66, cx + 2, base_y - 56], fill=(150, 150, 150))
    for k in range(5):
        px = cx - 44 + k * 22
        d.rectangle([px, base_y - 14, px + 6, base_y - 2], fill=(120, 120, 120))


def ill_flags(d, x, y, w, h):
    """Nepal's double-pennant and India's tricolour, crossed poles."""
    _sky(d, x, y, w, h, (226, 220, 205), (200, 190, 168))
    # Nepal: two stacked crimson pennants with blue edge
    nx, ny = x + w * 0.2, y + h * 0.2
    d.polygon([(nx, ny), (nx + 34, ny + 12), (nx, ny + 24)],
              fill=(220, 20, 60), outline=(0, 56, 147))
    d.polygon([(nx, ny + 24), (nx + 28, ny + 34), (nx, ny + 44)],
              fill=(220, 20, 60), outline=(0, 56, 147))
    d.line([(nx, ny - 4), (nx, y + h - 8)], fill=(90, 84, 72), width=2)
    # India: horizontal tricolour with navy chakra
    ix, iy = x + w * 0.55, y + h * 0.22
    fw, fh = 40, 30
    d.rectangle([ix, iy, ix + fw, iy + fh / 3], fill=(255, 153, 51))
    d.rectangle([ix, iy + fh / 3, ix + fw, iy + 2 * fh / 3],
                fill=(255, 255, 255))
    d.rectangle([ix, iy + 2 * fh / 3, ix + fw, iy + fh], fill=(19, 136, 8))
    d.ellipse([ix + fw / 2 - 4, iy + fh / 2 - 4, ix + fw / 2 + 4,
               iy + fh / 2 + 4], outline=(0, 0, 128), width=2)
    d.line([(ix, iy - 4), (ix, y + h - 8)], fill=(90, 84, 72), width=2)


def ill_rubble(d, x, y, w, h):
    """Ruined buildings and dust: a toxic wasteland."""
    _sky(d, x, y, w, h, (168, 158, 140), (200, 192, 176))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(140, 128, 108))
    # broken building silhouettes
    d.polygon([(x + 10, y + h - 12), (x + 10, y + h * 0.3),
               (x + 30, y + h * 0.18), (x + 34, y + h * 0.3),
               (x + 52, y + h * 0.3), (x + 52, y + h - 12)],
              fill=(110, 100, 88))
    d.polygon([(x + 62, y + h - 12), (x + 62, y + h * 0.45),
               (x + 82, y + h * 0.32), (x + 96, y + h * 0.45),
               (x + 96, y + h - 12)], fill=(96, 88, 76))
    d.polygon([(x + 104, y + h - 12), (x + 104, y + h * 0.55),
               (x + 124, y + h * 0.42), (x + 140, y + h * 0.55),
               (x + 140, y + h - 12)], fill=(120, 110, 96))
    # hazard sign
    cx, cy, r = x + w - 22, y + 16, 9
    d.polygon([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)],
              fill=(255, 210, 80), outline=(28, 26, 22))
    d.text((cx - 2, cy - 2), "!", font=font(SANS_B, 10), fill=(28, 26, 22))
    _smoke(d, x + w * 0.3, y + h * 0.25, 7)


def ill_chart(d, x, y, w, h):
    """A falling market line on a grid, red arrow down."""
    _sky(d, x, y, w, h, (240, 238, 230), (222, 216, 200))
    for k in range(4):
        gy = y + 6 + k * (h - 12) // 3
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(200, 192, 176), width=1)
    pts = [(x + 10, y + 10), (x + w * 0.3, y + h * 0.3),
           (x + w * 0.55, y + h * 0.45), (x + w * 0.75, y + h * 0.62),
           (x + w - 12, y + h - 12)]
    d.line(pts, fill=(164, 24, 34), width=3, joint="curve")
    ax, ay = x + w - 12, y + h - 12
    d.polygon([(ax, ay + 8), (ax - 7, ay - 2), (ax + 7, ay - 2)],
              fill=(164, 24, 34))
    d.text((x + 8, y + 4), "\u22123.3%", font=font(SANS_B, 11),
           fill=(164, 24, 34))


def ill_arena(d, x, y, w, h):
    """Concert arena at night, stage lights, crowd leaving."""
    _sky(d, x, y, w, h, (24, 24, 38), (60, 50, 80))
    # stage glow
    d.polygon([(x + w * 0.5, y + h * 0.7), (x + w * 0.2, y + 4),
               (x + w * 0.35, y + 4)], fill=(255, 210, 80))
    d.polygon([(x + w * 0.5, y + h * 0.7), (x + w * 0.65, y + 4),
               (x + w * 0.8, y + 4)], fill=(120, 180, 255))
    d.rectangle([x + w * 0.35, y + h * 0.62, x + w * 0.65, y + h * 0.78],
                fill=(40, 40, 52))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(30, 30, 40))
    for k in range(8):
        kx = x + 8 + k * (w - 16) // 8
        d.ellipse([kx, y + h * 0.8, kx + 7, y + h * 0.8 + 7],
                  fill=(200, 200, 210))
    d.text((x + 8, y + 4), "CO-OP LIVE", font=font(SANS_B, 9),
           fill=(255, 255, 255))


def ill_clinic(d, x, y, w, h):
    """A hospital building with a cross, dim windows."""
    _sky(d, x, y, w, h, (214, 222, 232), (190, 200, 212))
    d.rectangle([x + w * 0.2, y + h * 0.3, x + w * 0.8, y + h - 8],
                fill=(240, 238, 230), outline=(150, 150, 150))
    d.rectangle([x + w * 0.2, y + h * 0.3, x + w * 0.8, y + h * 0.42],
                fill=(180, 190, 200))
    # red cross on the roof sign
    cx, cy = x + w * 0.5, y + h * 0.18
    d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=(164, 24, 34))
    d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=(164, 24, 34))
    for r in range(2):
        for c in range(4):
            wx = x + w * 0.26 + c * (w * 0.12)
            wy = y + h * 0.5 + r * (h * 0.2)
            col = (255, 222, 140) if (r + c) % 3 else (90, 90, 90)
            d.rectangle([wx, wy, wx + 12, wy + 10], fill=col)


ILL = {
    "ship": ill_ship, "nato": ill_nato, "flats": ill_flats,
    "chip": ill_chip, "football": ill_football, "refinery": ill_refinery,
    "fire": ill_fire, "capitol": ill_capitol, "flags": ill_flags,
    "rubble": ill_rubble, "chart": ill_chart, "arena": ill_arena,
    "clinic": ill_clinic,
}


# ------------------------------------------------------------------ world map
# Coarse continent outlines (lon, lat), equirectangular projection.
# Rough hand-drawn shapes, good enough to place the 13 numbered pins.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16),
     (-105, 20), (-117, 33), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-35, 76), (-55, 76)],
    # South America
    [(-80, 9), (-72, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -38), (-65, -45), (-68, -52), (-72, -54),
     (-73, -40), (-70, -20), (-77, -12), (-80, -3)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68),
     (44, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 43), (-2, 37)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (38, 22), (43, 12),
     (48, 11), (51, 10), (44, 0), (40, -10), (35, -18), (32, -26),
     (28, -33), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5),
     (-13, 8), (-17, 15), (-16, 20), (-15, 27)],
    # Asia
    [(32, 36), (36, 36), (43, 41), (48, 44), (52, 46), (55, 51), (60, 55),
     (65, 60), (70, 68), (75, 72), (80, 73), (90, 75), (100, 77), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (158, 66), (162, 60),
     (158, 52), (150, 45), (142, 42), (140, 38), (135, 35), (130, 33),
     (127, 35), (122, 38), (120, 32), (115, 23), (110, 20), (105, 10),
     (100, 8), (98, 12), (95, 16), (90, 22), (86, 20), (80, 15), (77, 8),
     (75, 12), (72, 20), (66, 25), (60, 25), (57, 26), (52, 28), (50, 30),
     (48, 30), (44, 29), (40, 32), (36, 36)],
    # South-East Asia islands
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -2), (140, -8), (141, -4), (138, 1),
     (130, 3), (120, 4), (108, 2), (100, 6)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44),
     (141, 45), (139, 40), (136, 36), (132, 33)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 170) / 360.0 * (x1 - x0)
    py = y0 + (85 - lat) / 145.0 * (y1 - y0)
    return px, py


def draw_map(d, box, pins):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=SEA)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for s in pins:
        px, py = project(s["lon"], s["lat"], box)
        r = 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(s["n"])
        tw = d.textlength(num, font=font(SANS_B, 9))
        d.text((px - tw / 2, py - 6), num, font=font(SANS_B, 9),
               fill=(255, 255, 255))


# ------------------------------------------------------------------ sections

def draw_top(d):
    d.text((M, 8), "MAKE.FUN  \u2022  THE WORLD IN ONE PICTURE",
           font=F_SUB, fill=MUTED)
    right = "No. 327  \u2022  ONE DAY, ONE PAGE"
    d.text((W - M - d.textlength(right, font=F_SUB), 8), right,
           font=F_SUB, fill=MUTED)
    hrule(d, M, 26, W - M, width=1)


def draw_masthead(d):
    title = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 30), title, font=F_MAST, fill=INK)
    sub = ("THE WORLD IN ONE PAGE  \u2014  39 STORIES, 8 REGIONS  \u2022  "
           "EVERY STORY VERIFIED FROM THE WIRES")
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 74), sub, font=F_SUB, fill=MUTED)
    hrule(d, M, 90, W - M, width=2)


def draw_ticker(d, y):
    d.rectangle([M, y, W - M, y + 26], fill=RED)
    items = ["UKRAINE SINKS RUSSIAN CORVETTE OFF LIBYA",
             "NATO COUNCIL MEETS OVER POLAND MISSILES",
             "11 KILLED IN KYIV DRONE STRIKE"]
    text = "   \u2022   ".join(items)
    tw = d.textlength(text, font=F_TICK)
    d.text(((W - tw) / 2, y + 6), text, font=F_TICK, fill=(255, 255, 255))
    return y + 26


def draw_numbers(d, y):
    d.text((M, y), "BY THE NUMBERS", font=F_SEC, fill=RED)
    hrule(d, M, y + 15, W - M, width=1)
    col_w = CW / 6
    yy = y + 22
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * col_w + (6 if i else 0)
        if i:
            d.line([(M + i * col_w, yy), (M + i * col_w, yy + 44)],
                   fill=(200, 192, 176), width=1)
        d.text((x + 4, yy), num, font=F_NUM_BIG, fill=RED)
        block(d, x + 4, yy + 24, cap, F_NUM_CAP, col_w - 14, fill=MUTED,
              leading=11)
    return yy + 46


def draw_regions(d, y):
    counts = {}
    for s in LEADS + CARDS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for _n, region, _t in ALSO:
        counts[region] = counts.get(region, 0) + 1
    x = M
    for name, color in REGIONS:
        n = counts.get(name, 0)
        if not n:
            continue
        label = "%s %d" % (name, n)
        w = int(d.textlength(label, font=F_REG)) + 14
        d.rounded_rectangle([x, y, x + w, y + 20], radius=4, fill=color)
        d.text((x + 7, y + 4), label, font=F_REG, fill=(255, 255, 255))
        x += w + 7
    total = sum(counts.values())
    d.text((x + 4, y + 4), "%d stories" % total, font=F_REG, fill=MUTED)
    return y + 20


def draw_timeline(d, y):
    d.text((M, y), "THE DAY IN UTC", font=F_SEC, fill=RED)
    hrule(d, M, y + 15, W - M, width=1)
    col_w = CW / 6
    yy = y + 21
    d.line([(M, yy + 4), (W - M, yy + 4)], fill=(180, 170, 150), width=2)
    for i, (t, ev) in enumerate(TIMELINE):
        x = M + i * col_w
        d.ellipse([x + 2, yy, x + 10, yy + 8], fill=RED)
        d.text((x + 14, yy - 2), t, font=F_TL_T, fill=INK)
        block(d, x + 14, yy + 12, ev, F_TL_E, col_w - 18, fill=MUTED,
              leading=11)
    return yy + 36


def draw_leads(d, y):
    col_w = (CW - 2 * 12) / 3
    max_bottom = y
    for i, s in enumerate(LEADS):
        x = M + i * (col_w + 12)
        ILL[s["ill"]](d, x, y, col_w, 88)
        yy = y + 94
        tag_chip(d, x, yy, s["tag"], REGION_COLOR[s["region"]])
        yy += 20
        d.text((x, yy), "%d." % s["n"], font=F_LEAD_H, fill=RED)
        head_x = x + d.textlength("%d.  " % s["n"], font=F_LEAD_H)
        yy = block(d, head_x, yy, s["head"], F_LEAD_H,
                   col_w - (head_x - x), leading=20, max_lines=2)
        yy += 2
        yy = block(d, x, yy, s["body"], F_LEAD_B, col_w, leading=12,
                   max_lines=6)
        max_bottom = max(max_bottom, yy)
    return max_bottom


def draw_cards(d, y):
    col_w = (CW - 4 * 8) / 5
    row_h = 92
    for row in range(2):
        yy = y + row * (row_h + 6)
        for col in range(5):
            s = CARDS[row * 5 + col]
            x = M + col * (col_w + 8)
            d.rectangle([x, yy, x + col_w, yy + row_h], fill=PANEL,
                        outline=(210, 200, 182), width=1)
            ILL[s["ill"]](d, x + 1, yy + 1, col_w - 2, 26)
            ty = yy + 30
            d.text((x + 5, ty), "%d. %s" % (s["n"], s["tag"]), font=F_TAG,
                   fill=REGION_COLOR[s["region"]])
            ty += 13
            ty = block(d, x + 5, ty, s["head"], F_CARD_H, col_w - 10,
                       leading=12, max_lines=2)
            block(d, x + 5, ty + 1, s["body"], F_CARD_B, col_w - 10,
                  fill=MUTED, leading=11, max_lines=2)
    return y + 2 * row_h + 6


def draw_map_also(d, y):
    map_w = 400
    box_h = 200
    d.text((M, y), "WHERE IT HAPPENED \u2014 1\u201313 ON THE MAP",
           font=F_MAP_T, fill=INK)
    draw_map(d, (M, y + 18, M + map_w, y + 18 + 172), LEADS + CARDS)
    ax = M + map_w + 14
    aw = W - M - ax
    d.text((ax, y), "ALSO ON MONDAY", font=F_MAP_T, fill=INK)
    hrule(d, ax, y + 15, W - M, width=1)
    half = (len(ALSO) + 1) // 2
    col_w = (aw - 10) / 2
    for ci, chunk in enumerate((ALSO[:half], ALSO[half:])):
        cx = ax + ci * (col_w + 10)
        yy = y + 20
        for n, region, text in chunk:
            num = "%d." % n
            d.text((cx, yy), num, font=F_ALSO_N, fill=REGION_COLOR[region])
            nx = cx + d.textlength("39. ", font=F_ALSO_N)
            yy = block(d, nx, yy, text, F_ALSO, col_w - (nx - cx),
                       leading=11, max_lines=1)
            yy += 3
    return y + box_h


def draw_datecheck(d, y):
    box_w = 640
    d.rectangle([M, y, M + box_w, y + 64], fill=(255, 248, 220),
                outline=(200, 170, 90), width=1)
    d.text((M + 8, y + 6), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY",
           font=F_DC_B, fill=RED)
    block(d, M + 8, y + 22, DATE_CHECK, F_DC, box_w - 16, leading=11)
    hx = M + box_w + 12
    hw = W - M - hx
    d.rectangle([hx, y, hx + hw, y + 64], fill=PANEL,
                outline=(210, 200, 182), width=1)
    d.text((hx + 8, y + 6), "HOW SURE ARE WE?", font=F_DC_B, fill=INK)
    for i, (lab, txt) in enumerate(HOW_SURE):
        yy = y + 21 + i * 14
        d.text((hx + 8, yy), lab, font=F_DC_B, fill=RED)
        lx = hx + 8 + d.textlength("CONFIRMED  ", font=F_DC_B)
        d.text((lx, yy), txt, font=F_DC, fill=INK)
    return y + 64


def draw_footer(d, y):
    hrule(d, M, y, W - M, width=2)
    line = ("Every story here happened or was first reported on "
            "Monday 23 November 2026.")
    lw = d.textlength(line, font=F_FOOT_B)
    d.text(((W - lw) / 2, y + 4), line, font=F_FOOT_B, fill=INK)
    src = ("Sources: Reuters, BBC, AP, Al Jazeera, Guardian, CNN, Le Monde, "
           "Bloomberg, Xinhua, UN News  \u2022  Illustrations are original "
           "drawings made for this entry")
    sw = d.textlength(src, font=F_FOOT)
    d.text(((W - sw) / 2, y + 17), src, font=F_FOOT, fill=MUTED)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_top(d)
    draw_masthead(d)
    y = draw_ticker(d, 96)
    y = draw_numbers(d, y + 6)
    y = draw_regions(d, y + 4)
    y = draw_timeline(d, y + 6)
    y = draw_leads(d, y + 4)
    y = draw_cards(d, y + 6)
    y = draw_map_also(d, y + 8)
    y = draw_datecheck(d, y + 4)
    draw_footer(d, y + 4)
    return img


if __name__ == "__main__":
    out = os.path.join(HERE, "entry.png")
    img = build()
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")
