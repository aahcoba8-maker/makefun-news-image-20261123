#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - one-page newspaper image for Monday 23 November 2026.

Deterministic renderer: 42 verified stories of the day on a world map with
numbered pins, a three-column legend, and a markets rail. Stdlib only at the
top level; PIL is imported lazily and a pure-stdlib raster backend renders
the identical layout when PIL is unavailable. Writes entry.png.
"""
import os

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (185, 28, 28)
NAVY = (31, 58, 95)
OCEAN = (220, 230, 238)
LAND = (232, 220, 195)
FAINT = (190, 184, 168)

# (number, region, latitude, longitude, headline, summary)
STORIES = [
    (1, 'EUROPE', 36.90, 30.71, 'COP31 climate summit ends without a deal',
     'EU and 130 parties reject text omitting fossil fuels.'),
    (2, 'ASIA', 35.68, 139.69, 'AI sell-off rattles world markets',
     'Nikkei -5.06%, S&P -3.7%; gold jumps, futures rebound.'),
    (3, 'EUROPE', 50.78, 30.32, 'Russian strike on Dymer kills at least 10',
     'Boy, 7, pulled alive from rubble north of Kyiv.'),
    (4, 'ASIA', 22.55, 114.06, 'Trump, Putin, Xi hold Shenzhen summit',
     "Leaders issue a 'Declaration toward Peace' at APEC."),
    (5, 'MIDEAST', 26.56, 56.27, 'Trump threatens to sink Iranian vessels',
     'Warning follows US strike on an oil tanker.'),
    (6, 'AFRICA', 32.12, 20.07, 'Russian frigate sinks in Benghazi',
     'Suspected Ukrainian naval drone hit the Merkury.'),
    (7, 'AFRICA', 15.50, 32.53, 'Drone attacks kill five children in Khartoum',
     'Strikes also hit Omdurman, aid groups say.'),
    (8, 'AFRICA', 4.86, 31.57, 'Paramilitary attack kills 24 in South Sudan',
     'Civilians targeted in latest raid, officials say.'),
    (9, 'MIDEAST', 14.80, 42.95, 'Houthis claim attack on Saudi refinery',
     'Saudi strike answers on Hodeida port.'),
    (10, 'N.AMERICA', 25.00, -107.50, "FBI fugitive 'El Chapo Isidro' captured",
     'Most-wanted cartel figure seized in Sinaloa.'),
    (11, 'AFRICA', -1.94, 30.06, 'Five EU states accept Rwanda deportation hubs',
     'Deal moves asylum processing to Kigali.'),
    (12, 'EUROPE', 41.01, 28.98, 'Thousands rally in Istanbul over media takeover',
     'Protesters defend the independent press.'),
    (13, 'S.AMERICA', -15.79, -47.88, 'Bolsonaro in intensive care in Brasilia',
     'Former president treated for intestinal blockage.'),
    (14, 'N.AMERICA', 38.90, -77.04, 'Democrats win biggest House majority since 1992',
     'North Carolina flip seals the margin.'),
    (15, 'N.AMERICA', 37.77, -122.42, 'Anthropic team claims Riemann proof',
     'Mathematician and Claude say 160-year problem solved.'),
    (16, 'ASIA', 25.03, 121.57, "AI hackers 'Cairn' hit East Asia universities",
     'Suspected China-linked group used an AI framework.'),
    (17, 'ASIA', 37.57, 126.98, 'South Korea exports top $1 trillion',
     'Annual total passes the mark for the first time.'),
    (18, 'ASIA', 25.03, 121.57, 'Taiwan stocks swing 1,578 points in a day',
     'TSMC rebounds over 2% after early plunge.'),
    (19, 'OCEANIA', -13.59, 172.27, 'Magnitude 6.5 quake strikes Vanuatu region',
     'Deep quake at 598 km; no tsunami threat issued.'),
    (20, 'ASIA', 13.26, 123.69, 'Mayon eruption raises fears of bigger blast',
     'Philippine volcano spews ash; alerts raised.'),
    (21, 'EUROPE', 37.15, -8.54, 'Marquez wins eighth MotoGP world title',
     "Portimao win equals Agostini's record haul."),
]
STORIES += [
    (22, 'N.AMERICA', 36.17, -115.14, 'Verstappen wins Las Vegas Grand Prix',
     'Red Bull ace takes the night race in Nevada.'),
    (23, 'EUROPE', 51.50, -0.12, "UK confirmed to host 2035 Women's World Cup",
     'FIFA set to award the tournament to Britain.'),
    (24, 'N.AMERICA', 40.76, -73.85, 'Mets sign Skubal for record $450 million',
     "Nine-year deal is baseball's richest for a pitcher."),
    (25, 'AFRICA', -1.68, 29.22, 'Fighting disrupts Ebola response in DR Congo',
     'Health teams blocked near the outbreak zone.'),
    (26, 'MIDEAST', 31.50, 34.47, 'Experts: Gaza war left widespread contamination',
     'Toxins found across soil and water, study says.'),
    (27, 'EUROPE', 50.85, 4.35, 'Belgian airports shut by anti-austerity strike',
     'Brussels flights grounded for the day.'),
    (28, 'ASIA', 19.08, 72.88, 'Tata Steel in $1.67bn steel-pipe deal',
     "Buys into APL Apollo, India's top pipe maker."),
    (29, 'ASIA', 28.61, 77.21, 'India factory demand lifts November PMI',
     'Composite index up to 56.3, highest since June.'),
    (30, 'ASIA', -6.21, 106.85, 'MSCI talked down from Indonesia downgrade',
     'Prabowo and Dalio joined the call, Bloomberg says.'),
    (31, 'EUROPE', 50.11, 8.68, 'Lagarde to step down as ECB chief in Feb 2027',
     'Succession race opens at the central bank.'),
    (32, 'N.AMERICA', 33.75, -84.39, 'Delta delays top 1,000 after automation glitch',
     'Weekend disruption ripples across US hubs.'),
    (33, 'EUROPE', 48.86, 2.35, 'French rivals both question Ukraine aid',
     'Top candidates harden lines before spring vote.'),
    (34, 'EUROPE', 51.50, -0.12, 'NHS launches huge AI breast-cancer trial',
     "World's largest study tests earlier detection."),
    (35, 'ASIA', -7.25, 112.75, 'Deadly factory fire probed in Indonesia',
     'Authorities investigate the cause of the blaze.'),
    (36, 'EUROPE', 38.72, -9.14, 'Thousands march in Lisbon on living costs',
     'Protesters demand action on rent and wages.'),
    (37, 'ASIA', 28.20, 94.70, 'India, China hold 10-day border talks',
     'LAC tensions in Arunachal on the agenda.'),
    (38, 'ASIA', 27.71, 85.32, 'Nepal PM Balen Shah begins India visit',
     'Energy and connectivity top the Delhi agenda.'),
    (39, 'N.AMERICA', 29.76, -95.37, 'US energy exports hit record levels',
     'Oil market watches a growing surplus.'),
    (40, 'N.AMERICA', 39.01, -77.41, 'Trump hosts gala for his plunging meme coin',
     'Token trades under $1, down from a $75 peak.'),
    (41, 'EUROPE', 55.76, 37.62, 'Kremlin: Ukraine trilateral talks soon',
     'Moscow signals a fresh round after Shenzhen.'),
    (42, 'N.AMERICA', 45.42, -75.70, 'EU and Canada plan deeper AI collaboration',
     'Joint push on research and standards.'),
]

IN_BRIEF = ('IN BRIEF - Shenzhen peace declaration | Kyiv strike kills 10 | '
            'Marquez takes 8th title | Vanuatu M6.5 quake | Riemann claim')
SOURCES = ('Sources: Reuters - BBC - AP - Al Jazeera - Bloomberg - The Guardian - '
           'USGS - every story first reported on 23 November 2026.')
MARKETS = ("MARKETS - S&P 500 6,910 -3.70% | NIKKEI -5.06% | FTSE 100 10,346 -1.02% | "
           'BRENT $89.96 +0.01% | GOLD +2.72% | DOLLAR INDEX 103.77')

# Simplified continent outlines as (lon, lat) polygons for the map band.
SHAPES = [
    [(-168, 70), (-130, 58), (-122, 45), (-105, 22), (-80, 8), (-78, 25),
     (-100, 30), (-125, 50)],
    [(-81, 12), (-50, -2), (-45, -15), (-68, -55), (-80, -10)],
    [(-10, 70), (35, 65), (45, 50), (25, 40), (-10, 45)],
    [(-17, 35), (35, 30), (42, 12), (20, -35), (5, -34), (-15, 5)],
    [(30, 70), (80, 72), (125, 65), (170, 50), (135, 20), (100, 5), (60, 25)],
    [(112, -11), (150, -18), (145, -39), (115, -25)],
]

# 5x7 bitmap font for the stdlib backend: each glyph is 7 rows of 5 bits
# (bit value 16 = leftmost pixel). Text is rendered uppercase.
FONT5 = {
    'A': (14, 17, 17, 31, 17, 17, 17), 'B': (30, 17, 17, 30, 17, 17, 30),
    'C': (14, 17, 16, 16, 16, 17, 14), 'D': (30, 17, 17, 17, 17, 17, 30),
    'E': (31, 16, 16, 30, 16, 16, 31), 'F': (31, 16, 16, 30, 16, 16, 16),
    'G': (14, 17, 16, 23, 17, 17, 15), 'H': (17, 17, 17, 31, 17, 17, 17),
    'I': (14, 4, 4, 4, 4, 4, 14), 'J': (7, 2, 2, 2, 2, 18, 12),
    'K': (17, 18, 20, 24, 20, 18, 17), 'L': (16, 16, 16, 16, 16, 16, 31),
    'M': (17, 27, 21, 21, 17, 17, 17), 'N': (17, 17, 25, 21, 19, 17, 17),
    'O': (14, 17, 17, 17, 17, 17, 14), 'P': (30, 17, 17, 30, 16, 16, 16),
    'Q': (14, 17, 17, 17, 21, 18, 13), 'R': (30, 17, 17, 30, 20, 18, 17),
    'S': (15, 16, 16, 14, 1, 17, 14), 'T': (31, 4, 4, 4, 4, 4, 4),
    'U': (17, 17, 17, 17, 17, 17, 14), 'V': (17, 17, 17, 17, 17, 10, 4),
    'W': (17, 17, 17, 21, 21, 21, 10), 'X': (17, 10, 4, 4, 4, 10, 17),
    'Y': (17, 10, 4, 4, 4, 4, 4), 'Z': (31, 1, 2, 4, 8, 16, 31),
    '0': (14, 17, 19, 21, 25, 17, 14), '1': (4, 12, 4, 4, 4, 4, 14),
    '2': (14, 17, 1, 2, 4, 8, 31), '3': (31, 2, 4, 2, 1, 17, 14),
    '4': (2, 6, 10, 18, 31, 2, 2), '5': (31, 16, 30, 1, 1, 17, 14),
    '6': (6, 8, 16, 30, 17, 17, 14), '7': (31, 1, 2, 4, 8, 8, 8),
    '8': (14, 17, 17, 14, 17, 17, 14), '9': (14, 17, 17, 15, 1, 2, 12),
    ' ': (0, 0, 0, 0, 0, 0, 0), '.': (0, 0, 0, 0, 0, 12, 12),
    ',': (0, 0, 0, 0, 12, 4, 8), "'": (4, 4, 8, 0, 0, 0, 0),
    '-': (0, 0, 0, 31, 0, 0, 0), '%': (24, 25, 2, 4, 8, 19, 3),
    '$': (4, 15, 20, 14, 5, 30, 4), '+': (0, 4, 4, 31, 4, 4, 0),
    '/': (1, 1, 2, 4, 8, 16, 16), ':': (0, 12, 12, 0, 12, 12, 0),
    ';': (0, 12, 12, 0, 12, 4, 8), '!': (4, 4, 4, 4, 4, 0, 4),
    '?': (14, 17, 1, 2, 4, 0, 4), '(': (2, 4, 8, 8, 8, 4, 2),
    ')': (8, 4, 2, 2, 2, 4, 8), '&': (12, 18, 20, 8, 21, 18, 13),
    '*': (0, 4, 21, 14, 21, 4, 0), '#': (10, 10, 31, 10, 31, 10, 10),
    '|': (4, 4, 4, 4, 4, 4, 4), '_': (0, 0, 0, 0, 0, 0, 31),
    '"': (10, 10, 10, 0, 0, 0, 0), '=': (0, 0, 31, 0, 31, 0, 0),
    '<': (2, 4, 8, 16, 8, 4, 2), '>': (8, 4, 2, 1, 2, 4, 8),
}


# Rendering contract: draw_page() holds every layout decision (masthead,
# leads, map pins, legend, footer). The two backends further down only
# supply drawing primitives - PIL when available, pure stdlib otherwise -
# so both render the same page. Layout changes belong in draw_page().
def draw_page(text, rect, circle, polygon, line, wrap, measure, textfit):
    """Shared page layout. Backends supply the drawing primitives."""
    def centered(y, s, size, b=False, color=INK):
        text((W - measure(s, size, b)) / 2, y, s, size, color, b)

    centered(22, 'THE WORLD IN ONE DAY', 48, True)
    centered(82, 'MONDAY, 23 NOVEMBER 2026', 24, True)
    centered(118, '42 STORIES - 6 CONTINENTS', 12)
    text(28, 30, '42 STORIES', 10, INK, True)
    text(878, 30, '6 CONTINENTS', 10, INK, True)
    rect((28, 134, 996, 136), RED)

    # Two lead stories.
    for idx, st in enumerate(STORIES[:2]):
        n, reg, lat, lon, head, summ = st
        x = 28 + idx * 486
        text(x, 146, reg, 10, RED, True)
        for j, s in enumerate(wrap(head, 470, 20, True)[:2]):
            text(x, 164 + j * 24, s, 20, INK, True)
        for j, s in enumerate(wrap(summ, 470, 12)[:2]):
            text(x, 214 + j * 15, s, 12)
    textfit(28, 248, IN_BRIEF, 968, 10, 8)

    # World map band with numbered pins.
    rect((28, 268, 996, 436), OCEAN)

    def xy(lon, lat):
        return (28 + (lon + 180) * 968 / 360, 268 + (75 - lat) * 168 / 135)

    for shp in SHAPES:
        polygon([xy(lon, lat) for lon, lat in shp], LAND)
    placed = []
    for n, reg, lat, lon, head, summ in STORIES:
        x, y = xy(lon, lat)
        for step in range(3):
            if all((x - a) ** 2 + (y - b) ** 2 >= 14 ** 2 for a, b in placed):
                break
            if step % 2 == 0:
                y += 16
            else:
                x += 16
        x = max(39, min(985, x))
        y = max(279, min(425, y))
        placed.append((x, y))
        circle(x, y, 11, RED, (255, 255, 255), 2)
        textfit(x - 7, y - 5, str(n), 14, 9, 8, True, (255, 255, 255))

    # Legend: stories 3-42 in three columns of 14 / 13 / 13.
    starts = [3, 17, 30]
    ends = [16, 29, 42]
    for c, (start, end) in enumerate(zip(starts, ends)):
        x = 28 + c * 328
        for i in range(start, end + 1):
            n, reg, lat, lon, head, summ = STORIES[i - 1]
            y = 452 + (i - start) * 36
            text(x, y, str(n), 12, RED, True)
            text(x + 24, y + 1, reg, 7, NAVY, True)
            hx = x + 24 + measure(reg, 7, True) + 4
            avail = x + 312 - hx
            for j, s in enumerate(wrap(head, avail, 11, True)[:2]):
                textfit(hx, y + j * 13, s, avail, 11, 8, True)
            textfit(x + 24, y + 25, summ, 288, 8, 7)
        if c < 2:
            rect((28 + (c + 1) * 328 - 8, 452, 29 + (c + 1) * 328 - 8, 956), FAINT)

    rect((28, 960, 996, 961), RED)
    textfit(28, 966, SOURCES, 968, 8, 7)
    textfit(28, 988, MARKETS, 968, 8, 7, True)


def out_path():
    d = os.environ.get('MAKEFUN_OUTPUT_DIR') or '/output'
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        d = '.'
    return os.path.join(d, 'entry.png')


def pil_page(path):
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    fontdir = '/usr/share/fonts/truetype/dejavu/'
    try:
        regular = lambda size: ImageFont.truetype(fontdir + 'DejaVuSans.ttf', size)
        bold = lambda size: ImageFont.truetype(fontdir + 'DejaVuSans-Bold.ttf', size)
        regular(12)
        bold(12)
    except OSError:
        regular = lambda size: ImageFont.load_default()
        bold = regular

    def text(x, y, s, size=12, color=INK, b=False):
        draw.text((int(x), int(y)), s, font=(bold if b else regular)(size), fill=color)

    def rect(box, color):
        draw.rectangle(tuple(map(int, box)), fill=color)

    def circle(x, y, r, color, outline=None, width=1):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color, outline=outline, width=width)

    def polygon(points, color):
        draw.polygon(points, fill=color)

    def line(points, color, width=1):
        draw.line(points, fill=color, width=width)

    def measure(s, size, b=False):
        f = (bold if b else regular)(size)
        return draw.textbbox((0, 0), s, font=f)[2]

    def wrap(s, maxw, size, b=False):
        words = s.split()
        out = []
        cur = ''
        for word in words:
            test = (cur + ' ' + word).strip()
            if cur and measure(test, size, b) > maxw:
                out.append(cur)
                cur = word
            else:
                cur = test
        if cur:
            out.append(cur)
        return out

    def textfit(x, y, s, maxw, size, minsize=8, b=False, color=INK):
        while size > minsize and measure(s, size, b) > maxw:
            size -= 1
        text(x, y, s, size, color, b)
        return size

    draw_page(text, rect, circle, polygon, line, wrap, measure, textfit)
    image.save(path, format='PNG', optimize=False, compress_level=9)


def fallback_page(path):
    """Pure stdlib raster backend; 5x7 bitmap glyphs, uppercase."""
    pixels = bytearray(bytes(PAPER) * W * H)

    def put(x, y, color):
        x = int(x)
        y = int(y)
        if 0 <= x < W and 0 <= y < H:
            k = (y * W + x) * 3
            pixels[k:k + 3] = bytes(color)

    def rect(box, color):
        x0, y0, x1, y1 = map(int, box)
        for y in range(max(0, y0), min(H, y1 + 1)):
            a = (y * W + max(0, x0)) * 3
            b = (y * W + min(W, x1 + 1)) * 3
            if a < b:
                pixels[a:b] = bytes(color) * ((b - a) // 3)

    def circle(x, y, r, color, outline=None, width=1):
        x = int(x)
        y = int(y)
        r = int(r)
        for yy in range(y - r, y + r + 1):
            for xx in range(x - r, x + r + 1):
                d = (xx - x) ** 2 + (yy - y) ** 2
                if d <= r * r:
                    put(xx, yy, outline if (outline and d >= (r - width) ** 2) else color)

    def polygon(points, color):
        pts = [(int(x), int(y)) for x, y in points]
        if not pts:
            return
        lo = max(0, min(y for x, y in pts))
        hi = min(H - 1, max(y for x, y in pts))
        for y in range(lo, hi + 1):
            xs = []
            for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
                if y1 == y2:
                    continue
                if min(y1, y2) <= y < max(y1, y2):
                    xs.append(int(x1 + (y - y1) * (x2 - x1) / (y2 - y1)))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(max(0, a), min(W, b + 1)):
                    put(x, y, color)

    def line(points, color, width=1):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            dx = abs(int(x1) - int(x0))
            dy = abs(int(y1) - int(y0))
            sx = 1 if x0 < x1 else -1
            sy = 1 if y0 < y1 else -1
            err = dx - dy
            x = int(x0)
            y = int(y0)
            while True:
                rect((x - width // 2, y - width // 2, x + width // 2, y + width // 2), color)
                if x == int(x1) and y == int(y1):
                    break
                e = 2 * err
                if e > -dy:
                    err -= dy
                    x += sx
                if e < dx:
                    err += dx
                    y += sy

    def text(x, y, s, size=12, color=INK, b=False):
        scale = max(1, int(size / 8))
        xx = int(x)
        yy = int(y)
        for ch in s.upper():
            glyph = FONT5.get(ch, FONT5[' '])
            for gy, row in enumerate(glyph):
                for gx in range(5):
                    if row & (16 >> gx):
                        rect((xx + gx * scale, yy + gy * scale,
                              xx + (gx + 1) * scale - 1, yy + (gy + 1) * scale - 1), color)
            xx += 6 * scale

    def measure(s, size, b=False):
        return len(s) * 6 * max(1, int(size / 8))

    def wrap(s, maxw, size, b=False):
        words = s.split()
        out = []
        cur = ''
        for word in words:
            test = (cur + ' ' + word).strip()
            if cur and measure(test, size, b) > maxw:
                out.append(cur)
                cur = word
            else:
                cur = test
        if cur:
            out.append(cur)
        return out

    def textfit(x, y, s, maxw, size, minsize=8, b=False, color=INK):
        while size > minsize and measure(s, size, b) > maxw:
            size -= 1
        text(x, y, s, size, color, b)
        return size

    draw_page(text, rect, circle, polygon, line, wrap, measure, textfit)
    import struct
    import zlib
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw.extend(pixels[y * stride:(y + 1) * stride])

    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data +
                struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))

    png = (b'\x89PNG\r\n\x1a\n' +
           chunk(b'IHDR', struct.pack('>2I5B', W, H, 8, 2, 0, 0, 0)) +
           chunk(b'IDAT', zlib.compress(bytes(raw), 9)) +
           chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)


def main():
    path = out_path()
    try:
        import PIL  # noqa: F401
    except ImportError:
        fallback_page(path)
    else:
        pil_page(path)


if __name__ == '__main__':
    main()
