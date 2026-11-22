"""The World -- Saturday 21 November 2026.

A one-page newspaper front page summing up the world's news of
Saturday 21 November 2026, drawn from scratch with the Python
standard library only.  The program builds a 1024x1024 RGB image
in memory (a hand-written 5x7 bitmap font, rectangles, lines,
circles and filled polygons) and writes it as a PNG to
$MAKEFUN_OUTPUT_DIR/entry.png.  No network, no randomness, no
clock: two runs write byte-identical files.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (44, 82, 130)
TAN = (214, 196, 160)
GOLD = (240, 200, 40)
WHITE = (255, 255, 255)
SEA = (52, 96, 138)

# ---------------------------------------------------------------- font
# A 5x7 bitmap font, written by hand.  Each glyph is 7 rows of 5 cells,
# "#" is ink, "." is blank.  Uppercase letters, digits and punctuation
# only: the whole page is set in capitals, as a newspaper front page.

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", "..#..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", "..#..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."],
    "'": ["..#..", "..#..", ".#...", ".....", ".....", ".....", "....."],
    '"': [".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", "#.#.#", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    "*": [".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."],
}

_BLANK = ["....."] * 7

_REPLACEMENTS = {
    "\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2026": "...", "\u00e9": "E",
    "\u00ed": "I", "\u00f6": "O", "\u00fc": "U", "\u00b7": ".",
}


def normalise(text):
    out = []
    for ch in text:
        if ch in _REPLACEMENTS:
            out.append(_REPLACEMENTS[ch])
        else:
            out.append(ch)
    return "".join(out).upper()


def text_width(text, scale):
    text = normalise(text)
    return max(0, len(text) * 6 * scale - scale)


def wrap(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width."""
    text = normalise(text)
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for word in words:
            trial = word if not current else current + " " + word
            if text_width(trial, scale) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


# ---------------------------------------------------------------- canvas

class Canvas:
    def __init__(self, w, h, colour):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 3)
        r, g, b = colour
        for i in range(0, len(self.buf), 3):
            self.buf[i] = r
            self.buf[i + 1] = g
            self.buf[i + 2] = b

    def px(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = colour[0]
            self.buf[i + 1] = colour[1]
            self.buf[i + 2] = colour[2]

    def fill_rect(self, x, y, w, h, colour):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.buf[i] = colour[0]
                self.buf[i + 1] = colour[1]
                self.buf[i + 2] = colour[2]

    def rect(self, x, y, w, h, colour, thick=1):
        self.fill_rect(x, y, w, thick, colour)
        self.fill_rect(x, y + h - thick, w, thick, colour)
        self.fill_rect(x, y, thick, h, colour)
        self.fill_rect(x + w - thick, y, thick, h, colour)

    def hline(self, x, y, w, colour, thick=1):
        self.fill_rect(x, y, w, thick, colour)

    def vline(self, x, y, h, colour, thick=1):
        self.fill_rect(x, y, thick, h, colour)

    def line(self, x0, y0, x1, y1, colour):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, colour)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, colour):
        x = 0
        y = r
        d = 3 - 2 * r
        while x <= y:
            for sx, sy in ((x, y), (y, x), (-x, y), (-y, x),
                           (x, -y), (y, -x), (-x, -y), (-y, -x)):
                self.px(cx + sx, cy + sy, colour)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def fill_circle(self, cx, cy, r, colour):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, colour)

    def fill_polygon(self, points, colour):
        """Even-odd scanline fill for a simple polygon."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                    xs.append(x)
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                x0 = int(xs[i] + 0.5)
                x1 = int(xs[i + 1] + 0.5)
                if x1 >= x0:
                    self.fill_rect(x0, y, x1 - x0 + 1, 1, colour)

    def star(self, cx, cy, r, colour):
        import math
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rad = r if i % 2 == 0 else r * 0.38
            pts.append((int(cx + rad * math.cos(ang) + 0.5),
                        int(cy + rad * math.sin(ang) + 0.5)))
        self.fill_polygon(pts, colour)

    def text(self, x, y, s, scale, colour):
        s = normalise(s)
        cx = x
        for ch in s:
            glyph = FONT.get(ch, _BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "#":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, colour)
            cx += 6 * scale

    def text_centred(self, cx, y, s, scale, colour):
        self.text(cx - text_width(s, scale) // 2, y, s, scale, colour)


# ---------------------------------------------------------------- drawing

def draw_us_flag(cv, x, y, w, h):
    for i in range(13):
        y0 = y + round(i * h / 13)
        y1 = y + round((i + 1) * h / 13)
        if i % 2 == 0:
            cv.fill_rect(x, y0, w, y1 - y0, RED)
    canton_w = int(w * 0.4)
    canton_h = int(h * 7 / 13)
    cv.fill_rect(x, y, canton_w, canton_h, BLUE)
    for r in range(4):
        for c in range(5):
            dx = x + 4 + c * 7
            dy = y + 4 + r * 7
            cv.fill_rect(dx, dy, 2, 2, WHITE)


def draw_china_flag(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, RED)
    cv.star(x + int(w * 0.30), y + int(h * 0.48), 13, GOLD)
    for sx, sy in ((0.62, 0.16), (0.78, 0.30), (0.78, 0.55), (0.60, 0.72)):
        cv.star(x + int(w * sx), y + int(h * sy), 4, GOLD)


def draw_russia_flag(cv, x, y, w, h):
    third = h // 3
    cv.fill_rect(x, y, w, third, WHITE)
    cv.fill_rect(x, y + third, w, third, BLUE)
    cv.fill_rect(x, y + 2 * third, w, h - 2 * third, RED)


def draw_icon_sun(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    cv.circle(cx, cy, 11, INK)
    for i in range(8):
        import math
        a = i * math.pi / 4
        x0 = int(cx + 14 * math.cos(a))
        y0 = int(cy + 14 * math.sin(a))
        x1 = int(cx + 20 * math.cos(a))
        y1 = int(cy + 20 * math.sin(a))
        cv.line(x0, y0, x1, y1, INK)


def draw_icon_bars(cv, x, y, s):
    cv.fill_rect(x + 4, y + 8, 9, 28, INK)
    cv.fill_rect(x + 17, y + 18, 9, 18, INK)
    cv.fill_rect(x + 30, y + 28, 9, 8, INK)
    cv.line(x + 2, y + 6, x + 40, y + 34, RED)
    cv.line(x + 40, y + 34, x + 34, y + 34, RED)
    cv.line(x + 40, y + 34, x + 40, y + 28, RED)


def draw_icon_target(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    cv.circle(cx, cy, 19, INK)
    cv.circle(cx, cy, 11, INK)
    cv.fill_circle(cx, cy, 4, RED)


def draw_icon_burst(cv, x, y, s):
    import math
    cx, cy = x + s // 2, y + s // 2
    for i in range(8):
        a = i * math.pi / 4
        r = 20 if i % 2 == 0 else 13
        cv.line(cx, cy, int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), INK)
    cv.fill_circle(cx, cy, 4, RED)


def draw_icon_mountains(cv, x, y, s):
    cv.fill_polygon([(x + 2, y + 38), (x + 18, y + 10), (x + 30, y + 38)], INK)
    cv.fill_polygon([(x + 16, y + 38), (x + 32, y + 16), (x + 42, y + 38)], INK)
    cv.fill_polygon([(x + 15, y + 16), (x + 18, y + 10), (x + 21, y + 16)], PAPER)


def draw_icon_cross(cv, x, y, s):
    cv.rect(x + 4, y + 4, 36, 36, INK, 2)
    cv.fill_rect(x + 19, y + 12, 6, 20, RED)
    cv.fill_rect(x + 12, y + 19, 20, 6, RED)


def draw_icon_atom(cv, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    cv.circle(cx, cy, 16, INK)
    cv.fill_circle(cx, cy, 4, RED)
    cv.fill_circle(cx + 16, cy - 4, 3, INK)
    cv.fill_circle(cx - 12, cy + 12, 3, INK)


def draw_strait_map(cv, x, y, w, h):
    cv.rect(x, y, w, h, INK, 2)
    cv.text_centred(x + w // 2, y + 8, "STRAIT OF HORMUZ", 2, INK)
    my = y + 30
    mh = h - 58
    cv.fill_rect(x + 6, my, w - 12, mh, SEA)
    cv.fill_polygon([(x + 6, my), (x + 130, my), (x + 90, my + mh),
                     (x + 6, my + mh)], TAN)
    cv.fill_polygon([(x + w - 6, my), (x + w - 150, my),
                     (x + w - 110, my + mh), (x + w - 6, my + mh)], TAN)
    for tx, ty in ((x + 150, my + 18), (x + 210, my + 40)):
        cv.fill_rect(tx, ty, 26, 7, INK)
        cv.fill_rect(tx + 6, ty - 6, 8, 6, INK)
        cv.line(tx + 30, ty - 8, tx + 38, ty + 2, RED)
        cv.line(tx + 38, ty - 8, tx + 30, ty + 2, RED)
    cv.text_centred(x + w // 2, y + h - 18, "STRIKES AT WARTIME HIGH", 2, RED)


# ---------------------------------------------------------------- layout

def story_block(cv, x, y, w, kicker, headline_lines, deck, icon):
    cv.text(x, y, kicker, 2, RED)
    hy = y + 20
    for line in headline_lines:
        cv.text(x, hy, line, 3, INK)
        hy += 24
    dy = hy + 4
    for line in wrap(deck, w - 8, 2):
        cv.text(x, dy, line, 2, INK)
        dy += 16
    icon(cv, x + w - 46, y + 2, 44)


def build():
    cv = Canvas(W, H, PAPER)
    cv.rect(12, 12, W - 24, H - 24, INK, 3)
    cv.rect(20, 20, W - 40, H - 40, INK, 1)

    # Masthead.
    cv.text_centred(W // 2, 34, "THE WORLD", 15, INK)
    cv.hline(30, 152, W - 60, INK, 4)
    cv.hline(30, 160, W - 60, INK, 1)
    cv.text_centred(W // 2, 170, "SATURDAY, 21 NOVEMBER 2026", 2, INK)
    cv.hline(30, 194, W - 60, INK, 1)

    # Lead story: the Gulf.
    cv.text(30, 210, "MIDDLE EAST - THE GULF - OIL", 2, RED)
    cv.text(30, 234, "IRAN STRIKES BAHRAIN,", 5, INK)
    cv.text(30, 274, "HORMUZ TANKER ATTACKS SURGE", 5, INK)
    deck = ("TWO MORE TANKERS HIT NEAR THE STRAIT, AND OIL SHIPMENTS "
            "THROUGH IT ARE DOWN 15 PERCENT. SAUDI DEFENCES DOWN THREE "
            "HOUTHI MISSILES OVER RIYADH AS TEHRAN'S STANDOFF WITH THE "
            "U.S. DEEPENS.")
    dy = 314
    for line in wrap(deck, 600, 2):
        cv.text(30, dy, line, 2, INK)
        dy += 17
    draw_strait_map(cv, 664, 314, 320, 104)
    cv.hline(30, 434, W - 60, INK, 3)

    # APEC band.
    cv.text(30, 450, "APEC SUMMIT - SHENZHEN, CHINA", 2, RED)
    cv.text(30, 474, "TRUMP, XI AND PUTIN", 3, INK)
    cv.text(30, 498, "AT APEC IN SHENZHEN", 3, INK)
    deck2 = ("THREE NUCLEAR POWERS HOLD HISTORIC TALKS AND AGREE "
             "DIALOGUE ON NUCLEAR RISK")
    dy = 526
    for line in wrap(deck2, 620, 2):
        cv.text(30, dy, line, 2, INK)
        dy += 16
    draw_us_flag(cv, 680, 454, 96, 56)
    draw_china_flag(cv, 784, 454, 96, 56)
    draw_russia_flag(cv, 888, 454, 96, 56)
    cv.text_centred(728, 516, "USA", 2, INK)
    cv.text_centred(832, 516, "CHINA", 2, INK)
    cv.text_centred(936, 516, "RUSSIA", 2, INK)
    cv.hline(30, 560, W - 60, INK, 3)

    # Story grid: two columns, three rows.
    col_w = 477
    rows = [
        ("CLIMATE - COP31",
         ["CLIMATE TALKS DEADLOCK"],
         "COP31 IN OVERTIME IN ANTALYA AS FOSSIL-FUEL WORDING STALLS A DEAL",
         draw_icon_sun),
        ("MARKETS",
         ["U.S. STOCKS FALL INTO", "CORRECTION"],
         "S&P 500 DOWN 3.7%; CHINESE AI SHARES SHED $1.7 TRILLION",
         draw_icon_bars),
        ("MEXICO",
         ["MEXICO CAPTURES CARTEL", "BOSS 'EL CHAPO ISIDRO'"],
         "FAUSTO ISIDRO MEZA FLORES SEIZED IN SINALOA RAID; 11 KILLED",
         draw_icon_target),
        ("UKRAINE WAR",
         ["RUSSIA HITS ZELENSKY'S", "HOMETOWN"],
         "KRYVYI RIH MISSILE KILLS TWO; UKRAINE HITS RUSSIA-BOUND SHIP AT SEA",
         draw_icon_burst),
        ("EARTHQUAKE",
         ["MAGNITUDE 6.7 QUAKE", "SHAKES PERU"],
         "ANDES TREMOR NEAR JUNIN FELT IN LIMA; NO CASUALTIES REPORTED",
         draw_icon_mountains),
        ("BRAZIL",
         ["BOLSONARO IN INTENSIVE", "CARE"],
         "FORMER BRAZIL PRESIDENT HOSPITALISED WITH BOWEL OBSTRUCTION",
         draw_icon_cross),
    ]
    for i, (kicker, head, deck3, icon) in enumerate(rows):
        bx = 30 + (i % 2) * (col_w + 10)
        by = 572 + (i // 2) * 106
        story_block(cv, bx, by, col_w, kicker, head, deck3, icon)
    cv.hline(30, 892, W - 60, INK, 3)

    # Science strip.
    cv.text(30, 906, "SCIENCE", 2, RED)
    cv.text(30, 930, "AI HELPS PROVE RIEMANN HYPOTHESIS", 3, INK)
    cv.text(30, 958, "ANTHROPIC RESEARCHER CLAIMS BREAKTHROUGH ON MATH'S GREATEST UNSOLVED PROBLEM", 2, INK)
    draw_icon_atom(cv, 938, 908, 44)
    cv.hline(30, 980, W - 60, INK, 1)
    cv.text_centred(W // 2, 988, "THE WORLD - A SUMMARY OF THE DAY'S WORLD NEWS", 2, INK)

    return cv


def encode_png(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.buf[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(build())
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
