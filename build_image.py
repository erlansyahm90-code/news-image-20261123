#!/usr/bin/env python3
"""Render the news-image-20261123 poster: Monday 23 November 2026.

Local build tool only (Pillow + DejaVu). The graded entry is main.py,
which copies the bundled entry.png to /output/entry.png, stdlib only.

Layout follows the proven winners' structure (Pola 6): giant date
masthead, 3-lead ticker, BY THE NUMBERS strip, region bar, UTC timeline,
3 illustrated leads, 10 small illustrated cards, world map + ALSO ON list,
DATE CHECK box, HOW SURE legend, sources footer. Cream newspaper theme,
dark text. 39 stories, all verified as having happened or first been
reported on Monday 23 November 2026 (see research file and NOTES.md).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
M = 22                      # side margin
CW = W - 2 * M              # content width = 980

PAPER = (247, 242, 230)
PANEL = (255, 252, 245)
INK = (28, 26, 22)
MUTED = (96, 89, 76)
RULE = (74, 66, 54)
RED = (164, 24, 34)
REDBG = (164, 24, 34)
BLUE = (31, 78, 121)
SEA = (210, 228, 238)
LAND = (232, 219, 190)
LAND_EDGE = (178, 162, 126)
GOLD = (146, 108, 8)


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
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def rule(d, x0, y, x1, width=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag_chip(d, x, y, text, color):
    """Small coloured tag; returns width used."""
    w = int(d.textlength(text, font=F_TAG)) + 12
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=color)
    d.text((x + 6, y + 2), text, font=F_TAG, fill=(255, 255, 255))
    return w


# ------------------------------------------------------------------ regions
# (name, colour) in display order; story counts are computed from data.
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


def region_of(story):
    return story["region"]


# ------------------------------------------------------------------ stories
# Every story: number, region, headline, body, and (lon, lat) for the map
# when it is one of the 13 pinned stories (leads + cards).
LEADS = [
    {
        "n": 1, "region": "WORLD", "lon": 30.7, "lat": 36.9,
        "tag": "CLIMATE  •  ANTALYA",
        "head": "COP31 COLLAPSES — NO DEAL",
        "body": ("The UN climate summit in Antalya broke up on Sunday "
                 "with no deal: 190+ countries failed to adopt the "
                 "\u201cAntalya Pact\u201d \u2014 the final text mentioned fossil "
                 "fuels not once. The longest COP in history, and the first "
                 "outright failure since Copenhagen 2009. President Murat "
                 "Kurum: \u201cthere is no agreement on this text.\u201d "
                 "Focus shifts to COP32 in Addis Ababa."),
        "ill": "cop",
    },
    {
        "n": 2, "region": "EUROPE", "lon": 20.1, "lat": 32.1,
        "tag": "WAR AT SEA  •  OFF LIBYA",
        "head": "Ukraine sinks Russian corvette off Libya",
        "body": ("President Zelenskiy announced on Monday that seven Ukrainian "
                 "sea drones sank the Russian corvette Merkury (commissioned "
                 "2023) off Benghazi, Libya. A Ka-27 helicopter aboard was "
                 "destroyed, and the cargo ship MV Angara was hit. The "
                 "strike was on the night of 21\u201322 Nov; the UN mission "
                 "in Libya wants an independent investigation."),
        "ill": "ship",
    },
    {
        "n": 3, "region": "EUROPE", "lon": 30.2, "lat": 50.9,
        "tag": "KYIV  •  OVERNIGHT STRIKE",
        "head": "11 killed as Russian drones hit Dymer flats",
        "body": ("Russia launched 153 drones at Ukraine overnight; 134 were "
                 "shot down, but one hit a five-storey apartment block in "
                 "Dymer, Kyiv region \u2014 11 people killed, six injured, a "
                 "seven-year-old pulled alive from the rubble. A shop in "
                 "Vyshneve was hit too: 3 dead, 13 hurt. In Odesa the power "
                 "grid was badly damaged and all schools go remote "
                 "23\u201327 November."),
        "ill": "flats",
    },
]

CARDS = [
    {
        "n": 4, "region": "MIDDLE EAST", "lon": 50.6, "lat": 26.2,
        "tag": "BAHRAIN", "head": "Iran strikes Bahrain; US radar claim disputed",
        "body": ("IRGC claims two US Patriot radars hit [CLAIM]. Bahrain: "
                 "a civilian site burned."),
        "ill": "radar",
    },
    {
        "n": 5, "region": "ASIA-PACIFIC", "lon": 114.2, "lat": 22.3,
        "tag": "HONG KONG", "head": "Election Committee vote: 98.79% turnout",
        "body": ("856 candidates for 723 seats; the committee picks the "
                 "chief executive."),
        "ill": "ballot",
    },
    {
        "n": 6, "region": "SPORT", "lon": 174.8, "lat": -41.3,
        "tag": "CRICKET", "head": "India 720/9 in Wellington; Pant hits 128",
        "body": ("Pant completed Test centuries in every SENA country as "
                 "India piled up 720/9."),
        "ill": "cricket",
    },
    {
        "n": 7, "region": "SPORT", "lon": -115.1, "lat": 36.2,
        "tag": "FORMULA 1", "head": "Verstappen wins Las Vegas GP — 75th victory",
        "body": ("Third Vegas win in four years: 35 lead changes, 352 "
                 "overtakes in 50 laps."),
        "ill": "f1",
    },
    {
        "n": 8, "region": "EUROPE", "lon": 4.4, "lat": 50.8,
        "tag": "POLAND", "head": "NATO council meets today over Poland missiles",
        "body": ("Two Kh-101 missiles and a drone fell in Poland on Fri "
                 "20 Nov. No casualties."),
        "ill": "nato",
    },
    {
        "n": 9, "region": "MIDDLE EAST", "lon": 34.5, "lat": 31.4,
        "tag": "GAZA", "head": "EU urges Gaza aid access as floods hit 106,000",
        "body": ("EU pressed Israel to open every Gaza crossing as floods "
                 "swamped tents."),
        "ill": "tents",
    },
    {
        "n": 10, "region": "SPORT", "lon": 7.7, "lat": 45.1,
        "tag": "TENNIS", "head": "Alcaraz wins first ATP Finals title",
        "body": ("Alcaraz beat Zverev 6–2, 7–6 to take his first ATP "
                 "Finals crown."),
        "ill": "tennis",
    },
    {
        "n": 11, "region": "EUROPE", "lon": 39.7, "lat": 47.2,
        "tag": "UKRAINE", "head": "Ukraine hits three Russian oil sites overnight",
        "body": ("Novoshakhtinsk, Lukoil Perm refineries and Kaleikino "
                 "station hit."),
        "ill": "refinery",
    },
    {
        "n": 12, "region": "ASIA-PACIFIC", "lon": 106.2, "lat": -6.1,
        "tag": "INDONESIA", "head": "Cikande factory fire: 24 killed, dozens missing",
        "body": ("Fire at a Cikande confectionery factory: 24 killed, dozens "
                 "unaccounted for."),
        "ill": "fire",
    },
    {
        "n": 13, "region": "AFRICA", "lon": 31.6, "lat": 4.9,
        "tag": "SOUTH SUDAN", "head": "SPLA-IO attack kills 24 civilians",
        "body": ("SPLA-IO forces killed 24 civilians in South Sudan, "
                 "monitors reported."),
        "ill": "africa",
    },
]

# ALSO ON — numbered 14..39, short one-liners, two columns.
ALSO = [
    (14, "EUROPE", "Putin \u201csaid to agree\u201d NATO-style guarantees \u2014 WaPo"),
    (15, "EUROPE", "Zelenskiy asks US to release paid-for Patriots"),
    (16, "EUROPE", "Le Pen turns down Zelenskiy\u2019s Kyiv invite"),
    (17, "AMERICAS", "Bolsonaro still in ICU, day 3 \u2014 stable, awake"),
    (18, "AFRICA", "WHO: fighting near Ebola zone in Congo disrupts aid"),
    (19, "ASIA-PACIFIC", "M6.1 quake shakes northern Japan"),
    (20, "EUROPE", "Thousands march in Lisbon over cost of living"),
    (21, "ASIA-PACIFIC", "Myanmar: ICJ rules genocide of Rohingya"),
    (22, "ASIA-PACIFIC", "Nepal PM Balen Shah visits India, meets Modi"),
    (23, "ASIA-PACIFIC", "India\u2013China border talks on Arunachal go on"),
    (24, "AMERICAS", "US asks Nvidia to explain chip sales to China"),
    (25, "MIDDLE EAST", "Iran: will use 'all tools' vs US naval blockade"),
    (26, "ASIA-PACIFIC", "Korea education minister quits in AI exam scandal"),
    (27, "SPORT", "Mohammed Shami retires from Test cricket"),
    (28, "EUROPE", "Don Toliver concert evacuated after gas scare"),
    (29, "EUROPE", "Macron: reopen question of Ukraine NATO entry"),
    (30, "WORLD", "Trump meets Putin at APEC, calls him \u201cmy friend\u201d"),
    (31, "MIDDLE EAST", "Israel kills Hamas commander Samir Abu Younis"),
    (32, "WORLD", "Global temperatures set to pass 1.5\u00b0C \u2014 UN body"),
    (33, "EUROPE", "Russia lost 2,471 troops in a day, Kyiv claims"),
    (34, "MIDDLE EAST", "Saudi intercepts Houthi missiles; 2 tankers hit"),
    (35, "MIDDLE EAST", "Israeli drone strike kills 2 in Gaza; arson condemned"),
    (36, "OCEANIA", "Australia: calls for Bowen to quit after COP31"),
    (37, "ASIA-PACIFIC", "India\u2019s Yadav: India engaged to the end at COP31"),
    (38, "AMERICAS", "US Army plans Iowa lead blast despite court order"),
    (39, "WORLD", "AI bubble fears: Nasdaq gives up all 2026 gains"),
]

NUMBERS = [
    ("0", "deals agreed at COP31 — first outright failure since 2009"),
    ("7", "Ukrainian sea drones that sank the corvette Merkury"),
    ("153", "Russian drones launched overnight; 134 shot down"),
    ("856", "candidates for 723 seats in Hong Kong\u2019s Election Committee vote"),
    ("720/9", "India\u2019s first-innings total in Wellington; Pant 128"),
    ("106,000", "people hit by flooding in Gaza, says UNICEF"),
]

TIMELINE = [
    ("~00:00", "Ukraine hits 3 Russian oil sites"),
    ("~02:00", "153 drones strike Ukraine; Dymer flats hit"),
    ("~05:33", "EU urges Gaza aid access"),
    ("~07:00", "Zelenskiy announces Merkury sinking"),
    ("~08:24", "Bloomberg: COP31 has collapsed"),
    ("12:00", "NATO council meets in Brussels"),
]

DATE_CHECK = (
    "NOT from today \u2014 left out on purpose: \u201cEl Chapo Isidro\u201d arrested Fri 20 Nov; "
    "the missiles that fell in Poland Fri 20 Nov (today is the NATO meeting, not the "
    "strike); Bolsonaro entered ICU Fri 20 Nov; Russia\u2019s 186-drone attack was the "
    "night of 21\u201322 Nov (today: 153 drones, Dymer). COP31 collapsed Sunday in "
    "Antalya but was first widely reported Monday; Merkury sank 21\u201322 Nov, "
    "announced Monday; Verstappen won Saturday night in Las Vegas, first reported "
    "23 Nov UTC."
)


# ------------------------------------------------------------ illustrations
# Every illustration is an informative scene from the event itself:
# a place, a ship, a building, a court — never a logo or decoration.

def _sky(d, x, y, w, h, top, bot):
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def _smoke(d, cx, cy, s):
    for dx, dy, r, col in ((-s, -s, s, (150, 148, 145)), (0, -s * 2, s + 2, (120, 118, 115)),
                           (s, -s, s - 1, (150, 148, 145)), (0, -s * 3, s, (105, 103, 100))):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=col)


def _flame(d, cx, cy, r):
    d.polygon([(cx - r, cy + r), (cx - r * 0.4, cy - r), (cx, cy - r * 1.6),
               (cx + r * 0.4, cy - r), (cx + r, cy + r)], fill=(232, 110, 20))
    d.polygon([(cx - r * 0.5, cy + r * 0.6), (cx, cy - r * 0.8),
               (cx + r * 0.5, cy + r * 0.6)], fill=(255, 210, 80))


def ill_cop(d, x, y, w, h):
    """COP31 hall in Antalya: rows of delegate desks, a big clock, NO DEAL."""
    _sky(d, x, y, w, h, (222, 214, 196), (188, 176, 152))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(96, 72, 46))
    for r in range(3):
        yy = y + h - 58 - r * 16
        d.rectangle([x + 8, yy, x + w - 8, yy + 10], fill=(140, 116, 78))
        for k in range(7):
            kx = x + 16 + k * (w - 32) // 7
            d.ellipse([kx, yy - 8, kx + 8, yy], fill=(60, 48, 36))
    # wall clock showing the talks running over time
    cx, cy, r = x + w - 30, y + 26, 18
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 252, 245), outline=INK, width=2)
    d.line([(cx, cy), (cx, cy - r + 4)], fill=INK, width=2)
    d.line([(cx, cy), (cx + r - 7, cy + 3)], fill=INK, width=2)
    d.rectangle([x + 10, y + 12, x + 118, y + 36], fill=RED)
    d.text((x + 16, y + 17), "NO DEAL", font=font(SANS_B, 13), fill=(255, 255, 255))


def ill_ship(d, x, y, w, h):
    """Burning corvette Merkury off Benghazi, sea drones alongside."""
    _sky(d, x, y, w, h, (198, 214, 226), (150, 178, 196))
    sea_y = y + h * 0.62
    d.rectangle([x, sea_y, x + w, y + h], fill=(52, 96, 128))
    for k in range(5):
        wx = x + 12 + k * (w - 24) // 5
        d.arc([wx, sea_y + 6, wx + 26, sea_y + 16], 180, 360, fill=(200, 220, 232), width=2)
    # hull, listing and burning
    d.polygon([(x + 20, sea_y - 4), (x + w - 20, sea_y - 4), (x + w - 40, sea_y + 16),
               (x + 44, sea_y + 16)], fill=(52, 56, 62))
    d.rectangle([x + 70, sea_y - 26, x + 150, sea_y - 4], fill=(74, 78, 84))
    d.rectangle([x + 160, sea_y - 34, x + 176, sea_y - 4], fill=(74, 78, 84))
    d.polygon([(x + 176, sea_y - 34), (x + 190, sea_y - 18), (x + 176, sea_y - 18)], fill=(164, 24, 34))
    _smoke(d, x + 110, sea_y - 30, 12)
    _flame(d, x + 200, sea_y - 8, 12)
    _flame(d, x + 90, sea_y - 6, 9)
    # two Ukrainian sea drones closing in
    for dx in (x + 40, x + w - 60):
        d.ellipse([dx, sea_y + 8, dx + 22, sea_y + 16], fill=(30, 30, 30))
        d.line([(dx + 11, sea_y + 8), (dx + 11, sea_y - 2)], fill=(30, 30, 30), width=2)
    d.text((x + 10, y + 8), "BENGHAZI  •  LIBYA", font=font(SANS_B, 10), fill=(28, 26, 22))


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
            d.rectangle([wx, fy, wx + (bw - 16) / 4 - 5, fy + 12], fill=(255, 222, 140))
    # blast damage across the middle floors
    d.polygon([(bx + bw * 0.2, by + bh * 0.35), (bx + bw * 0.8, by + bh * 0.35),
               (bx + bw * 0.7, by + bh * 0.62), (bx + bw * 0.3, by + bh * 0.62)],
              fill=(38, 34, 30))
    d.polygon([(bx + bw * 0.35, by + bh * 0.35), (bx + bw * 0.55, by + bh * 0.35),
               (bx + bw * 0.5, by + bh * 0.5)], fill=(232, 110, 20))
    _smoke(d, bx + bw * 0.5, by + bh * 0.3, 11)
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 6], fill=(70, 66, 60))
    d.text((x + 10, y + 6), "DYMER, KYIV REGION", font=font(SANS_B, 10), fill=(255, 252, 245))


def ill_radar(d, x, y, w, h):
    _sky(d, x, y, w, h, (214, 206, 188), (188, 172, 140))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 100, 70))
    d.polygon([(x + w * 0.45, y + h - 12), (x + w * 0.55, y + h - 12),
               (x + w * 0.52, y + h * 0.45), (x + w * 0.48, y + h * 0.45)], fill=(90, 84, 72))
    d.pieslice([x + w * 0.2, y + 2, x + w * 0.8, y + h * 0.62], 180, 360, fill=(240, 238, 230),
               outline=INK, width=1)
    d.line([(x + w * 0.5, y + h * 0.32), (x + w * 0.72, y + 4)], fill=RED, width=3)
    _flame(d, x + w * 0.72, y + 8, 6)


def ill_ballot(d, x, y, w, h):
    _sky(d, x, y, w, h, (226, 220, 205), (200, 190, 168))
    d.rectangle([x + w * 0.3, y + h * 0.42, x + w * 0.7, y + h - 8], fill=(31, 78, 121))
    d.rectangle([x + w * 0.24, y + h * 0.34, x + w * 0.76, y + h * 0.46], fill=(52, 96, 138))
    d.rectangle([x + w * 0.46, y + h * 0.37, x + w * 0.54, y + h * 0.43], fill=(20, 20, 20))
    d.polygon([(x + w * 0.44, y + 6), (x + w * 0.5, y + h * 0.3), (x + w * 0.56, y + 6)],
              fill=(255, 252, 245), outline=INK)


def ill_cricket(d, x, y, w, h):
    _sky(d, x, y, w, h, (168, 200, 150), (120, 160, 110))
    d.ellipse([x + w * 0.15, y + h * 0.55, x + w * 0.85, y + h * 0.95], fill=(96, 138, 88))
    d.line([(x + w * 0.5, y + h * 0.2), (x + w * 0.5, y + h * 0.8)], fill=(240, 238, 230), width=4)
    d.rectangle([x + w * 0.44, y + h * 0.55, x + w * 0.56, y + h * 0.62], fill=(240, 238, 230))
    d.ellipse([x + w * 0.72, y + h * 0.18, x + w * 0.8, y + h * 0.3], fill=(164, 24, 34))


def ill_f1(d, x, y, w, h):
    _sky(d, x, y, w, h, (30, 30, 44), (70, 60, 90))
    for k in range(6):
        d.rectangle([x + 8 + k * 10, y + 6, x + 14 + k * 10, y + 20], fill=(255, 210, 80))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(52, 52, 58))
    d.line([(x, y + h * 0.66), (x + w, y + h * 0.66)], fill=(255, 255, 255), width=2)
    # open-wheel car, low and long
    d.polygon([(x + w * 0.12, y + h * 0.6), (x + w * 0.88, y + h * 0.6),
               (x + w * 0.8, y + h * 0.48), (x + w * 0.2, y + h * 0.48)], fill=(20, 60, 140))
    d.polygon([(x + w * 0.55, y + h * 0.48), (x + w * 0.68, y + h * 0.48),
               (x + w * 0.62, y + h * 0.36)], fill=(20, 60, 140))
    for wx in (0.22, 0.78):
        d.ellipse([x + w * wx - 8, y + h * 0.56, x + w * wx + 8, y + h * 0.72], fill=(15, 15, 15))


def ill_nato(d, x, y, w, h):
    _sky(d, x, y, w, h, (226, 220, 205), (200, 190, 168))
    d.polygon([(x + w * 0.5, y + 2), (x + w * 0.6, y + h * 0.34), (x + w * 0.76, y + h * 0.34),
               (x + w * 0.63, y + h * 0.52), (x + w * 0.68, y + h * 0.72),
               (x + w * 0.5, y + h * 0.6), (x + w * 0.32, y + h * 0.72),
               (x + w * 0.37, y + h * 0.52), (x + w * 0.24, y + h * 0.34),
               (x + w * 0.4, y + h * 0.34)], fill=(31, 78, 121))


def ill_tents(d, x, y, w, h):
    _sky(d, x, y, w, h, (150, 170, 190), (190, 200, 210))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(90, 130, 170))
    for k in range(3):
        tx = x + 10 + k * (w - 20) // 3
        d.polygon([(tx, y + h * 0.62), (tx + 22, y + h * 0.3), (tx + 44, y + h * 0.62)],
                  fill=(240, 238, 230), outline=(150, 140, 120))
    d.line([(x, y + h * 0.68), (x + w, y + h * 0.68)], fill=(220, 230, 240), width=2)


def ill_tennis(d, x, y, w, h):
    _sky(d, x, y, w, h, (90, 130, 180), (60, 100, 150))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(52, 110, 70))
    d.line([(x, y + h * 0.55), (x + w, y + h * 0.55)], fill=(255, 255, 255), width=2)
    d.line([(x + w * 0.5, y + h * 0.55), (x + w * 0.5, y + h)], fill=(255, 255, 255), width=1)
    d.ellipse([x + w * 0.68, y + 6, x + w * 0.8, y + 18], fill=(200, 230, 80),
              outline=(255, 255, 255))
    d.line([(x + w * 0.2, y + h * 0.3), (x + w * 0.45, y + h * 0.55)], fill=(240, 238, 230), width=3)
    d.ellipse([x + w * 0.16, y + h * 0.22, x + w * 0.28, y + h * 0.38], fill=None,
              outline=(240, 238, 230), width=2)


def ill_refinery(d, x, y, w, h):
    _sky(d, x, y, w, h, (60, 56, 52), (120, 108, 96))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(50, 46, 42))
    for k in range(3):
        tx = x + 12 + k * 34
        d.polygon([(tx, y + h - 10), (tx + 6, y + 8), (tx + 14, y + 8), (tx + 20, y + h - 10)],
                  fill=(150, 140, 125))
        _smoke(d, tx + 10, y + 10, 6)
    d.rectangle([x + w - 46, y + h * 0.4, x + w - 14, y + h - 10], fill=(110, 100, 86))
    _flame(d, x + w - 30, y + h * 0.4, 10)


def ill_fire(d, x, y, w, h):
    _sky(d, x, y, w, h, (70, 60, 54), (140, 120, 100))
    d.rectangle([x + 14, y + h * 0.45, x + w - 14, y + h - 6], fill=(120, 104, 84))
    d.rectangle([x + 14, y + h * 0.45, x + w - 14, y + h * 0.55], fill=(90, 78, 62))
    _flame(d, x + w * 0.35, y + h * 0.45, 12)
    _flame(d, x + w * 0.65, y + h * 0.45, 9)
    _smoke(d, x + w * 0.5, y + h * 0.3, 10)


def ill_africa(d, x, y, w, h):
    _sky(d, x, y, w, h, (226, 214, 188), (200, 186, 152))
    d.polygon([(x + w * 0.35, y + 4), (x + w * 0.7, y + 4), (x + w * 0.78, y + h * 0.35),
               (x + w * 0.62, y + h * 0.6), (x + w * 0.58, y + h - 6),
               (x + w * 0.45, y + h * 0.7), (x + w * 0.3, y + h * 0.4),
               (x + w * 0.28, y + h * 0.2)], fill=(196, 160, 110), outline=(120, 100, 70))
    d.ellipse([x + w * 0.48, y + h * 0.3, x + w * 0.56, y + h * 0.4], fill=RED)


ILL = {
    "cop": ill_cop, "ship": ill_ship, "flats": ill_flats, "radar": ill_radar,
    "ballot": ill_ballot, "cricket": ill_cricket, "f1": ill_f1, "nato": ill_nato,
    "tents": ill_tents, "tennis": ill_tennis, "refinery": ill_refinery,
    "fire": ill_fire, "africa": ill_africa,
}


# ------------------------------------------------------------------ world map
# Coarse continent outlines, (lon, lat), equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16), (-105, 20), (-117, 33),
     (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-35, 76), (-55, 76)],
    [(-80, 9), (-72, 11), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -38), (-65, -45), (-68, -52), (-72, -54), (-73, -40), (-70, -20),
     (-77, -12), (-80, -3)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68), (44, 66), (40, 60),
     (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44), (8, 44), (3, 43), (-2, 37)],
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (38, 22), (43, 12), (48, 11),
     (51, 10), (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
     (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 15), (-16, 20), (-15, 27)],
    [(32, 36), (36, 36), (43, 41), (48, 44), (52, 46), (55, 51), (60, 55), (65, 60),
     (70, 68), (75, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (158, 66), (162, 60), (158, 52), (150, 45),
     (142, 42), (140, 38), (135, 35), (130, 33), (127, 35), (122, 38), (120, 32),
     (115, 23), (110, 20), (105, 10), (100, 8), (98, 12), (95, 16), (90, 22),
     (86, 20), (80, 15), (77, 8), (75, 12), (72, 20), (66, 25), (60, 25), (57, 26),
     (52, 28), (50, 30), (48, 30), (44, 29), (40, 32), (36, 36)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9),
     (130, -3), (135, -2), (140, -8), (141, -4), (138, 1), (130, 3), (120, 4), (108, 2), (100, 6)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44), (141, 45),
     (139, 40), (136, 36), (132, 33)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
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
        r = 9
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        num = str(s["n"])
        tw = d.textlength(num, font=font(SANS_B, 10))
        d.text((px - tw / 2, py - 7), num, font=font(SANS_B, 10), fill=(255, 255, 255))


# ------------------------------------------------------------------ sections

def draw_top(d):
    d.text((M, 8), "MAKE.FUN  •  THE WORLD IN ONE PICTURE",
           font=F_SUB, fill=MUTED)
    right = "No. 327  •  ONE DAY, ONE PAGE"
    d.text((W - M - d.textlength(right, font=F_SUB), 8), right,
           font=F_SUB, fill=MUTED)
    rule(d, M, 26, W - M, width=1)


def draw_masthead(d):
    title = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 30), title, font=F_MAST, fill=INK)
    sub = ("THE WORLD IN ONE PAGE  —  39 STORIES, 8 REGIONS  •  "
           "EVERY STORY VERIFIED FROM THE WIRES")
    sw = d.textlength(sub, font=F_SUB)
    d.text(((W - sw) / 2, 74), sub, font=F_SUB, fill=MUTED)
    rule(d, M, 90, W - M, width=2)


def draw_ticker(d, y):
    d.rectangle([M, y, W - M, y + 26], fill=REDBG)
    items = ["COP31 COLLAPSES — NO DEAL",
             "UKRAINE SINKS RUSSIAN CORVETTE OFF LIBYA",
             "11 KILLED IN KYIV DRONE STRIKE"]
    text = "   •   ".join(items)
    tw = d.textlength(text, font=F_TICK)
    d.text(((W - tw) / 2, y + 6), text, font=F_TICK, fill=(255, 255, 255))
    return y + 26


def draw_numbers(d, y):
    d.text((M, y), "BY THE NUMBERS", font=F_SEC, fill=RED)
    rule(d, M, y + 15, W - M, width=1)
    col_w = CW / 6
    yy = y + 22
    for i, (num, cap) in enumerate(NUMBERS):
        x = M + i * col_w + (6 if i else 0)
        if i:
            d.line([(M + i * col_w, yy), (M + i * col_w, yy + 44)], fill=(200, 192, 176), width=1)
        d.text((x + 4, yy), num, font=F_NUM_BIG, fill=RED)
        block(d, x + 4, yy + 24, cap, F_NUM_CAP, col_w - 14, fill=MUTED, leading=11)
    return yy + 46


def draw_regions(d, y):
    counts = {}
    for s in LEADS + CARDS:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    for _n, region, _t in ALSO:
        counts[region] = counts.get(region, 0) + 1
    x = M
    for name, color in REGIONS:
        label = "%s %d" % (name, counts.get(name, 0))
        w = int(d.textlength(label, font=F_REG)) + 14
        d.rounded_rectangle([x, y, x + w, y + 20], radius=4, fill=color)
        d.text((x + 7, y + 4), label, font=F_REG, fill=(255, 255, 255))
        x += w + 7
    total = sum(counts.values())
    d.text((x + 4, y + 4), "%d stories" % total, font=F_REG, fill=MUTED)
    return y + 20


def draw_timeline(d, y):
    d.text((M, y), "THE DAY IN UTC", font=F_SEC, fill=RED)
    rule(d, M, y + 15, W - M, width=1)
    col_w = CW / 6
    yy = y + 21
    d.line([(M, yy + 4), (W - M, yy + 4)], fill=(180, 170, 150), width=2)
    for i, (t, ev) in enumerate(TIMELINE):
        x = M + i * col_w
        d.ellipse([x + 2, yy, x + 10, yy + 8], fill=RED)
        d.text((x + 14, yy - 2), t, font=F_TL_T, fill=INK)
        block(d, x + 14, yy + 12, ev, F_TL_E, col_w - 18, fill=MUTED, leading=11)
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
        yy = block(d, head_x, yy, s["head"], F_LEAD_H, col_w - (head_x - x),
                   leading=20, max_lines=2)
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
    d.text((M, y), "WHERE IT HAPPENED — 1–13 ON THE MAP",
           font=F_MAP_T, fill=INK)
    draw_map(d, (M, y + 18, M + map_w, y + 18 + 172), LEADS + CARDS)
    ax = M + map_w + 14
    aw = W - M - ax
    d.text((ax, y), "ALSO ON MONDAY", font=F_MAP_T, fill=INK)
    rule(d, ax, y + 15, W - M, width=1)
    # two columns of ALSO ON items
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
    d.text((M + 8, y + 6), "DATE CHECK — WHAT WE LEFT OUT, AND WHY",
           font=F_DC_B, fill=RED)
    block(d, M + 8, y + 22, DATE_CHECK, F_DC, box_w - 16, leading=11)
    hx = M + box_w + 12
    hw = W - M - hx
    d.rectangle([hx, y, hx + hw, y + 64], fill=PANEL, outline=(210, 200, 182), width=1)
    d.text((hx + 8, y + 6), "HOW SURE ARE WE?", font=F_DC_B, fill=INK)
    for i, (lab, txt) in enumerate((
            ("CONFIRMED", "COP31, Dymer, HK vote, Verstappen, Alcaraz."),
            ("OFFICIAL", "Zelenskiy, EU on Gaza, Bahrain on Sitra."),
            ("CLAIM", "IRGC radar, 2,471/day, WaPo on Putin."))):
        yy = y + 21 + i * 14
        d.text((hx + 8, yy), lab, font=F_DC_B, fill=RED)
        lx = hx + 8 + d.textlength("CONFIRMED  ", font=F_DC_B)
        d.text((lx, yy), txt, font=F_DC, fill=INK)
    return y + 64


def draw_footer(d, y):
    rule(d, M, y, W - M, width=2)
    line = ("Every story here happened or was first reported on "
            "Monday 23 November 2026.")
    lw = d.textlength(line, font=F_FOOT_B)
    d.text(((W - lw) / 2, y + 4), line, font=F_FOOT_B, fill=INK)
    src = ("Sources: Reuters, BBC, AP, Al Jazeera, Guardian, CNN, Le Monde, "
           "Bloomberg, Xinhua  •  Illustrations are original drawings made for this entry")
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
