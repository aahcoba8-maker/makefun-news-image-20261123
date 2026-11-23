#!/usr/bin/env python3
"""THE WORLD IN ONE DAY -- front page for Monday 23 November 2026.

Builds a 1024x1024 newspaper page: masthead, the day's two lead
stories, an IN BRIEF ticker, a world map carrying one numbered pin
per story, a three-column legend of all 42 stories, and a footer
with sources and the closing markets.

Only the standard library is imported at module level.  When Pillow
is importable it does the drawing; otherwise a small built-in bitmap
renderer draws the same layout and writes the PNG itself.  Either
way the output is deterministic: same bytes on every run.
"""

import math
import os

PAGE = 1024
EDGE = 26                    # outer margin on every side
RIGHT = PAGE - EDGE          # last text column edge (998)
CONTENT = RIGHT - EDGE       # usable width (972)

PAPER = (243, 238, 226)
INK = (28, 26, 24)
RED = (178, 32, 28)
NAVY = (30, 52, 96)
GREY = (95, 89, 80)
OCEAN = (197, 210, 215)
LAND = (224, 212, 184)
FAINT = (203, 196, 182)
WHITE = (255, 255, 255)

# Each story: (number, region, latitude, longitude, headline, summary)
STORIES = [
    (1, "EUROPE", 36.88, 30.71,
     "COP31 summit ends without a deal",
     "EU and 130 parties reject a text omitting fossil fuels."),
    (2, "ASIA", 35.68, 139.69,
     "AI sell-off rattles world markets",
     "Nikkei -5.06%, S&P -3.7%; gold jumps, futures rebound."),
    (3, "EUROPE", 50.78, 30.30,
     "Russian strike on Dymer kills at least 10",
     "Missiles hit the town north of Kyiv, officials say."),
    (4, "ASIA", 22.55, 114.06,
     "Trump, Putin, Xi hold Shenzhen summit",
     "Leaders issue a 'Declaration toward Peace' at APEC."),
    (5, "MIDEAST", 26.56, 56.27,
     "Trump threatens to sink Iranian vessels",
     "Warning follows a US strike on an oil tanker."),
    (6, "AFRICA", 32.12, 20.07,
     "Russian frigate sinks in Benghazi",
     "The Merkury goes down in the Libyan port."),
    (7, "AFRICA", 15.50, 32.53,
     "Drone attacks kill five children in Khartoum",
     "Aid groups condemn the strikes on the capital."),
    (8, "AFRICA", 4.86, 31.57,
     "Paramilitary attack kills 24 in South Sudan",
     "Civilians targeted in the latest raid, officials say."),
    (9, "MIDEAST", 24.09, 38.06,
     "Houthis claim attack on Saudi refinery",
     "Claim raises fears for Red Sea energy routes."),
    (10, "N.AMERICA", 24.81, -107.39,
     "FBI fugitive 'El Chapo Isidro' captured",
     "Most-wanted cartel figure seized in Sinaloa."),
    (11, "AFRICA", -1.94, 30.06,
     "Five EU states accept Rwanda deportation hubs",
     "Deal moves asylum processing to Kigali."),
    (12, "EUROPE", 41.01, 28.98,
     "Thousands rally in Istanbul over media takeover",
     "Protesters defend the independent press."),
    (13, "S.AMERICA", -15.79, -47.88,
     "Bolsonaro in intensive care in Brasilia",
     "Former president under observation in hospital."),
    (14, "N.AMERICA", 38.90, -77.04,
     "Democrats win biggest House majority since 1992",
     "Result reshapes the Washington balance of power."),
    (15, "N.AMERICA", 37.77, -122.42,
     "Anthropic team claims Riemann proof",
     "Claim on the 160-year-old problem stirs mathematics."),
    (16, "ASIA", 39.90, 116.40,
     "AI hackers 'Cairn' hit East Asia universities",
     "Campuses across the region report breaches."),
    (17, "ASIA", 37.57, 126.98,
     "South Korea exports top $1 trillion",
     "Annual total passes the mark for the first time."),
    (18, "ASIA", 25.03, 121.57,
     "Taiwan stocks swing 1,578 points in a day",
     "TSMC rebounds over 2% after an early plunge."),
    (19, "OCEANIA", -17.74, 168.31,
     "Magnitude 6.5 quake strikes Vanuatu region",
     "Deep quake; no tsunami threat issued."),
    (20, "ASIA", 13.26, 123.69,
     "Mayon eruption raises fears of bigger blast",
     "Philippine volcano spews ash; alerts raised."),
    (21, "EUROPE", 39.47, -0.38,
     "Marquez wins eighth MotoGP world title",
     "Eighth crown for the Spanish rider."),
    (22, "N.AMERICA", 36.17, -115.14,
     "Verstappen wins Las Vegas Grand Prix",
     "Red Bull ace takes the night race in Nevada."),
    (23, "EUROPE", 51.51, -0.13,
     "UK confirmed to host 2035 Women's World Cup",
     "FIFA set to award the tournament to Britain."),
    (24, "N.AMERICA", 40.76, -73.91,
     "Mets sign Skubal for record $450 million",
     "Nine-year deal is baseball's richest for a pitcher."),
    (25, "AFRICA", 0.49, 29.47,
     "Fighting disrupts Ebola response in DR Congo",
     "Health teams blocked near the outbreak zone."),
    (26, "MIDEAST", 31.50, 34.47,
     "Experts: Gaza war left widespread contamination",
     "Toxins found across soil and water, study says."),
    (27, "EUROPE", 50.85, 4.35,
     "Belgian airports shut by anti-austerity strike",
     "Brussels flights grounded for the day."),
    (28, "ASIA", 19.08, 72.88,
     "Tata Steel in $1.67bn steel-pipe deal",
     "Buys into APL Apollo, India's top pipe maker."),
    (29, "ASIA", 28.61, 77.21,
     "India factory demand lifts November PMI",
     "Composite index rises to 56.3 in November."),
    (30, "ASIA", -6.21, 106.85,
     "MSCI talked down from Indonesia downgrade",
     "Index provider holds off after talks in Jakarta."),
    (31, "EUROPE", 50.11, 8.68,
     "Lagarde to step down as ECB chief in Feb 2027",
     "Succession race opens at the central bank."),
    (32, "N.AMERICA", 33.75, -84.39,
     "Delta delays top 1,000 after automation glitch",
     "Weekend disruption ripples across US hubs."),
    (33, "EUROPE", 48.86, 2.35,
     "French rivals both question Ukraine aid",
     "Top candidates harden lines before spring vote."),
    (34, "EUROPE", 52.21, 0.12,
     "NHS launches huge AI breast-cancer trial",
     "World's largest study tests earlier detection."),
    (35, "ASIA", -6.24, 107.00,
     "Deadly factory fire probed in Indonesia",
     "Authorities investigate the cause of the blaze."),
    (36, "EUROPE", 38.72, -9.14,
     "Thousands march in Lisbon on living costs",
     "Protesters demand action on rent and wages."),
    (37, "ASIA", 34.15, 77.58,
     "India, China hold 10-day border talks",
     "LAC tensions in Arunachal on the agenda."),
    (38, "ASIA", 27.71, 85.32,
     "Nepal PM Balen Shah begins India visit",
     "Energy and connectivity top the Delhi agenda."),
    (39, "N.AMERICA", 29.76, -95.37,
     "US energy exports hit record levels",
     "Oil market watches a growing surplus."),
    (40, "N.AMERICA", 26.68, -80.04,
     "Trump hosts gala for his plunging meme coin",
     "Top holders feted as the token slides."),
    (41, "EUROPE", 55.76, 37.62,
     "Kremlin: Ukraine trilateral talks soon",
     "Moscow signals a fresh round after Shenzhen."),
    (42, "N.AMERICA", 45.42, -75.70,
     "EU and Canada plan deeper AI collaboration",
     "Joint push on research and standards."),
]

BRIEF = ("IN BRIEF - COP31 deadlocks on fossil fuels | Shenzhen "
         "declaration signed | Vanuatu quake M6.5 | Marquez crowned "
         "again | Delta delays top 1,000 | Mayon erupts")
SOURCES = ("Sources: Reuters - BBC - AP - Al Jazeera - Bloomberg - "
           "The Guardian - USGS - every story first reported on "
           "23 November 2026.")
MARKETS = ("MARKETS - S&P 500 6,910 -3.70% | NIKKEI -5.06% | "
           "FTSE 100 10,346 -1.02% | BRENT $89.96 +0.01% | "
           "GOLD +2.72% | DOLLAR INDEX 103.77")

# Coarse continent outlines as (longitude, latitude) loops, drawn
# from memory of a standard world map; recognisable at panel scale.
LAND_SHAPES = [
    # North America
    [(-165, 60), (-150, 60), (-140, 66), (-130, 70), (-120, 72),
     (-110, 73), (-100, 78), (-92, 79), (-85, 72), (-82, 68),
     (-78, 62), (-70, 58), (-65, 60), (-60, 55), (-55, 52),
     (-60, 47), (-65, 44), (-70, 42), (-73, 40), (-74, 37),
     (-76, 34), (-79, 31), (-80, 27), (-81, 25), (-84, 28),
     (-86, 21), (-90, 20), (-94, 18), (-97, 16), (-101, 17),
     (-104, 20), (-106, 23), (-110, 24), (-113, 28), (-118, 33),
     (-122, 37), (-124, 42), (-124, 47), (-128, 52), (-135, 57),
     (-152, 59), (-162, 58)],
    # South America
    [(-78, 3), (-80, -3), (-79, -8), (-76, -14), (-70, -18),
     (-70, -24), (-70, -30), (-72, -37), (-73, -44), (-74, -50),
     (-69, -54), (-66, -55), (-66, -49), (-65, -42), (-63, -39),
     (-58, -34), (-52, -32), (-48, -27), (-41, -22), (-39, -17),
     (-35, -8), (-37, -5), (-44, -3), (-50, 0), (-54, 4),
     (-60, 7), (-66, 10), (-72, 12), (-77, 8), (-80, 9)],
    # Europe
    [(-10, 36), (-9, 44), (-2, 49), (1, 51), (6, 53), (8, 57),
     (5, 59), (8, 62), (14, 67), (24, 71), (35, 67), (44, 66),
     (48, 64), (40, 60), (36, 56), (38, 52), (40, 48), (36, 46),
     (33, 42), (30, 46), (27, 44), (28, 41), (23, 39), (19, 40),
     (16, 38), (12, 42), (8, 44), (3, 43), (-1, 44), (-2, 37)],
    # Africa
    [(-6, 35), (0, 36), (9, 37), (11, 34), (19, 32), (29, 31),
     (33, 27), (35, 24), (37, 22), (39, 20), (40, 16), (43, 12),
     (46, 11), (51, 12), (48, 6), (42, 0), (40, -6), (40, -12),
     (38, -18), (36, -22), (34, -26), (31, -29), (27, -33),
     (22, -35), (19, -34), (18, -31), (16, -28), (14, -22),
     (13, -17), (12, -13), (13, -8), (9, -3), (9, 1), (5, 4),
     (-1, 5), (-7, 4), (-12, 8), (-16, 12), (-17, 15), (-17, 20),
     (-16, 24), (-15, 28), (-10, 31)],
    # Asia (steppe line, Pacific coast, India, Arabia, Levant)
    [(36, 45), (44, 48), (56, 51), (68, 52), (82, 52), (96, 50),
     (110, 48), (122, 50), (132, 48), (140, 45), (141, 42),
     (139, 39), (140, 37), (137, 35), (133, 34), (130, 32),
     (127, 35), (126, 38), (123, 39), (121, 37), (122, 33),
     (121, 29), (119, 25), (114, 22), (109, 19), (109, 15),
     (108, 11), (106, 8), (104, 2), (101, 3), (99, 7), (98, 10),
     (96, 14), (94, 17), (92, 16), (91, 22), (89, 22), (87, 21),
     (84, 19), (81, 15), (79, 13), (77, 8), (76, 10), (74, 14),
     (73, 17), (72, 20), (70, 22), (67, 24), (62, 25), (58, 25),
     (54, 26), (51, 28), (49, 29), (50, 25), (55, 24), (58, 22),
     (57, 19), (55, 17), (52, 15), (49, 14), (45, 12), (43, 13),
     (42, 15), (40, 19), (38, 22), (36, 27), (35, 29), (36, 36),
     (33, 36), (30, 36), (28, 37), (27, 40), (30, 41), (33, 42)],
    # Australia
    [(113, -11), (114, -17), (114, -22), (115, -27), (115, -32),
     (117, -35), (122, -34), (127, -32), (131, -32), (134, -33),
     (136, -35), (138, -36), (140, -38), (144, -38), (147, -38),
     (149, -37), (151, -34), (153, -29), (153, -25), (151, -21),
     (147, -19), (144, -15), (142, -11), (141, -13), (139, -17),
     (136, -15), (136, -12), (133, -11), (130, -12), (126, -14),
     (122, -17), (118, -15), (114, -13)],
    # Britain, Japan, Indonesia, New Zealand (small shapes)
    [(-5, 50), (-3, 51), (-1, 52), (0, 54), (-1, 56), (-3, 58),
     (-5, 57), (-6, 55), (-5, 53), (-4, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 36),
     (140, 38), (141, 41), (141, 44), (143, 43), (142, 40),
     (140, 37), (138, 36), (135, 34), (132, 33), (130, 32)],
    [(95, 5), (99, 2), (103, -2), (106, -5), (109, -6), (112, -7),
     (115, -8), (119, -9), (123, -10), (127, -10), (124, -11),
     (118, -10), (112, -8), (107, -7), (103, -4), (98, 2), (95, 4)],
    [(172, -35), (174, -38), (175, -41), (173, -42), (170, -44),
     (168, -46), (167, -45), (169, -43), (171, -41), (172, -38)],
]


# ------------------------------------------------------------------
# Text layout helpers.  `measure` is a pen's text-width function with
# signature measure(text, size, bold) -> pixels.
# ------------------------------------------------------------------

def wrap_words(measure, text, size, bold, width, limit=None):
    """Greedy word wrap; returns at most `limit` lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if cur and measure(trial, size, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines[:limit] if limit else lines


def fit_line(measure, text, size, bold, width):
    """One line, shortened with '...' until it fits `width`."""
    if measure(text, size, bold) <= width:
        return text
    while text and measure(text + "...", size, bold) > width:
        text = text.rsplit(" ", 1)[0] if " " in text else text[:-1]
    return text + "..."


def split_headline(measure, text, first_width, rest_width, size):
    """Wrap a headline whose first line is narrower than the rest."""
    lines, cur, width = [], "", first_width
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if cur and measure(trial, size, True) > width:
            lines.append(cur)
            cur = word
            width = rest_width
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines[:2]


# ------------------------------------------------------------------
# Pillow backend.
# ------------------------------------------------------------------

class PilPen:
    """Draws with Pillow's ImageDraw and DejaVu fonts."""

    FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

    def __init__(self):
        from PIL import Image, ImageDraw, ImageFont
        self._tt = ImageFont
        self.img = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.drw = ImageDraw.Draw(self.img)
        self._fonts = {}

    def _font(self, size, bold):
        key = (int(size), bool(bold))
        if key not in self._fonts:
            name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
            try:
                font = self._tt.truetype(self.FONT_DIR + name, int(size))
            except Exception:
                font = self._tt.load_default()
            self._fonts[key] = font
        return self._fonts[key]

    def textw(self, text, size, bold=False):
        return self.drw.textlength(text, font=self._font(size, bold))

    def write(self, x, y, text, size, color=INK, bold=False, align="l"):
        w = self.textw(text, size, bold)
        if align == "c":
            x -= w / 2
        elif align == "r":
            x -= w
        self.drw.text((x, y), text, font=self._font(size, bold),
                      fill=color)

    def box(self, x0, y0, x1, y1, color):
        self.drw.rectangle([x0, y0, x1, y1], fill=color)

    def poly(self, points, color):
        self.drw.polygon(points, fill=color)

    def disc(self, cx, cy, r, fill, ring=None, ring_w=2):
        self.drw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
                         outline=ring, width=ring_w)

    def save(self, path):
        self.img.save(path, "PNG")


# ------------------------------------------------------------------
# Bitmap fallback backend: a 5x7 font, one 7-row tuple per glyph,
# each row a 5-bit mask (bit 16 = leftmost pixel).
# ------------------------------------------------------------------

GLYPHS = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A),
    "X": (0x11, 0x0A, 0x04, 0x04, 0x04, 0x0A, 0x11),
    "Y": (0x11, 0x0A, 0x04, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F),
    "3": (0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "-": (0, 0, 0, 0x1F, 0, 0, 0),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "%": (0x19, 0x1A, 0x02, 0x04, 0x08, 0x0B, 0x13),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    "+": (0, 0, 0x04, 0x1F, 0x04, 0, 0),
    "/": (0x01, 0x02, 0x02, 0x04, 0x08, 0x08, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x06, 0x04, 0, 0x04),
    "|": (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    '"': (0x0A, 0x0A, 0, 0, 0, 0, 0),
    "·": (0, 0, 0, 0x0C, 0x0C, 0, 0),
}

_SWAP = {"—": "-", "–": "-", "−": "-", "’": "'", "‘": "'"}


def _clean(text):
    """Uppercase and reduce to characters the bitmap font knows."""
    out = []
    for ch in text.upper():
        ch = _SWAP.get(ch, ch)
        out.append(ch if ch in GLYPHS else " ")
    return "".join(out)


class RawPen:
    """Same drawing surface as PilPen, on a raw RGB pixel buffer."""

    def __init__(self):
        self.buf = bytearray(bytes(PAPER) * (PAGE * PAGE))

    def _put(self, x, y, color):
        if 0 <= x < PAGE and 0 <= y < PAGE:
            i = (y * PAGE + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def box(self, x0, y0, x1, y1, color):
        x0, x1 = max(0, int(x0)), min(PAGE, int(x1))
        if x1 <= x0:
            return
        row = bytes(color) * (x1 - x0)
        for y in range(max(0, int(y0)), min(PAGE, int(y1))):
            i = (y * PAGE + x0) * 3
            self.buf[i:i + len(row)] = row

    def poly(self, points, color):
        top = int(min(p[1] for p in points))
        bot = int(max(p[1] for p in points))
        n = len(points)
        for y in range(max(0, top), min(PAGE, bot + 1)):
            hits = []
            for i in range(n):
                ax, ay = points[i]
                bx, by = points[(i + 1) % n]
                if (ay <= y < by) or (by <= y < ay):
                    hits.append(ax + (y - ay) * (bx - ax) / (by - ay))
            hits.sort()
            for k in range(0, len(hits) - 1, 2):
                self.box(hits[k], y, hits[k + 1] + 1, y + 1, color)

    def disc(self, cx, cy, r, fill, ring=None, ring_w=2):
        inner = (r - ring_w) ** 2
        for y in range(int(cy - r), int(cy + r) + 1):
            for x in range(int(cx - r), int(cx + r) + 1):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                if d2 <= r * r:
                    self._put(x, y, ring if (ring and d2 > inner)
                              else fill)

    @staticmethod
    def _scale(size):
        return max(1, int(round(size / 7.0)))

    def textw(self, text, size, bold=False):
        text = _clean(text)
        return (len(text) * 6 - 1) * self._scale(size) if text else 0

    def write(self, x, y, text, size, color=INK, bold=False,
              align="l"):
        text = _clean(text)
        sc = self._scale(size)
        if align == "c":
            x -= self.textw(text, size, bold) / 2
        elif align == "r":
            x -= self.textw(text, size, bold)
        cx = int(x)
        for ch in text:
            rows = GLYPHS.get(ch, GLYPHS[" "])
            for gy, bits in enumerate(rows):
                for gx in range(5):
                    if bits & (16 >> gx):
                        for dy in range(sc):
                            for dx in range(sc):
                                px = cx + gx * sc + dx
                                py = int(y) + gy * sc + dy
                                self._put(px, py, color)
                                if bold:
                                    self._put(px + 1, py, color)
            cx += 6 * sc

    def save(self, path):
        import struct
        import zlib
        stride = PAGE * 3
        raw = b"".join(
            b"\x00" + bytes(self.buf[y * stride:(y + 1) * stride])
            for y in range(PAGE))

        def chunk(tag, data):
            return (struct.pack(">I", len(data)) + tag + data +
                    struct.pack(">I",
                                zlib.crc32(tag + data) & 0xFFFFFFFF))

        png = (b"\x89PNG\r\n\x1a\n" +
               chunk(b"IHDR", struct.pack(">IIBBBBB", PAGE, PAGE,
                                          8, 2, 0, 0, 0)) +
               chunk(b"IDAT", zlib.compress(raw, 9)) +
               chunk(b"IEND", b""))
        with open(path, "wb") as fh:
            fh.write(png)


# ------------------------------------------------------------------
# Page composition, shared by both backends.
# ------------------------------------------------------------------

MAP_TOP, MAP_BOT = 274, 458
LEG_TOP, LEG_ROWS, LEG_RH = 472, 14, 34
LEG_COLS = (26, 354, 682)
LEG_W = 300


def _project(lon, lat):
    """Longitude/latitude -> pixel inside the map panel."""
    x = EDGE + (lon + 180.0) / 360.0 * CONTENT
    y = MAP_TOP + (78.0 - lat) / 136.0 * (MAP_BOT - MAP_TOP)
    return x, y


def compose(pen):
    measure = pen.textw

    # Masthead.
    pen.write(EDGE, 92, "42 STORIES", 11, INK, True)
    pen.write(RIGHT, 92, "7 REGIONS + SPACE", 11, INK, True, "r")
    pen.write(PAGE / 2, 14, "THE WORLD IN ONE DAY", 55, INK, True, "c")
    pen.write(PAGE / 2, 84, "MONDAY, 23 NOVEMBER 2026", 25, INK,
              True, "c")
    pen.write(PAGE / 2, 120, "42 STORIES · 7 REGIONS + SPACE", 12,
              GREY, False, "c")
    pen.box(EDGE, 140, RIGHT, 143, RED)

    # The two leads, side by side.
    lead_w = 462
    for i, st in enumerate(STORIES[:2]):
        x = EDGE + i * (lead_w + 48)
        pen.write(x, 154, st[1], 11, RED, True)
        lines = wrap_words(measure, st[4], 23, True, lead_w, limit=2)
        for j, line in enumerate(lines):
            pen.write(x, 172 + j * 28, line, 23, INK, True)
        pen.write(x, 234, fit_line(measure, st[5], 13, False, lead_w),
                  13, GREY)

    # IN BRIEF ticker.
    pen.write(EDGE, 254, fit_line(measure, BRIEF, 12, False, CONTENT),
              12, INK)

    # World map panel with one pin per story.
    pen.box(EDGE, MAP_TOP, RIGHT, MAP_BOT, OCEAN)
    for shape in LAND_SHAPES:
        pen.poly([_project(lon, lat) for lon, lat in shape], LAND)
    placed = []
    for st in STORIES:
        hx0, hy0 = _project(st[3], st[2])
        spot = None
        for rad in (0, 13, 20, 27, 34, 42, 50):
            steps = 1 if rad == 0 else 12
            for k in range(steps):
                ang = 2 * math.pi * k / steps
                cx = hx0 + rad * math.cos(ang)
                cy = hy0 + rad * math.sin(ang)
                if not (EDGE + 11 <= cx <= RIGHT - 11 and
                        MAP_TOP + 11 <= cy <= MAP_BOT - 11):
                    continue
                if all((cx - a) ** 2 + (cy - b) ** 2 >= 19 ** 2
                       for a, b in placed):
                    spot = (cx, cy)
                    break
            if spot:
                break
        if spot is None:
            spot = (max(EDGE + 11, min(RIGHT - 11, hx0)),
                    max(MAP_TOP + 11, min(MAP_BOT - 11, hy0)))
        cx, cy = spot
        placed.append((cx, cy))
        pen.disc(cx, cy, 10, RED, WHITE, 2)
        pen.write(cx, cy - 5, str(st[0]), 10, WHITE, True, "c")

    # Legend: all 42 stories, three columns of fourteen.
    for col_x in LEG_COLS[1:]:
        pen.box(col_x - 9, LEG_TOP, col_x - 8, LEG_TOP + 462, FAINT)
    for idx, st in enumerate(STORIES):
        x = LEG_COLS[idx // LEG_ROWS]
        y = LEG_TOP + (idx % LEG_ROWS) * LEG_RH
        pen.write(x, y, str(st[0]), 12, RED, True)
        pen.write(x + 24, y + 2, st[1], 8, NAVY, True)
        hx = x + 24 + measure(st[1], 8, True) + 5
        lines = split_headline(measure, st[4], LEG_W - (hx - x),
                               LEG_W - 24, 11)
        if lines:
            pen.write(hx, y, lines[0], 11, INK, True)
        if len(lines) > 1:
            pen.write(x + 24, y + 13, lines[1], 11, INK, True)
        pen.write(x + 24, y + 25,
                  fit_line(measure, st[5], 8.5, False, LEG_W - 24),
                  8.5, GREY)

    # Footer.
    pen.box(EDGE, 950, RIGHT, 952, RED)
    pen.write(EDGE, 960, fit_line(measure, SOURCES, 9.5, False,
                                  CONTENT), 9.5, GREY)
    pen.write(EDGE, 979, fit_line(measure, MARKETS, 10.5, True,
                                  CONTENT), 10.5, INK, True)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__))
    out = os.path.join(out_dir, "entry.png")
    try:
        import PIL.Image  # noqa: F401
        pen = PilPen()
    except Exception:
        pen = RawPen()
    compose(pen)
    pen.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
