#!/usr/bin/env python3
"""Draw a newspaper front page summing up 19 November 2026 in one image.

Uses only Pillow and the local DejaVu fonts. Everything on the page is
drawn with simple shapes and gradients -- no external pictures, no network.
Run from the repo root; it writes entry.png next to this script.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BIG = font("DejaVuSerif-Bold.ttf", 72)
SERIF = font("DejaVuSerif-Bold.ttf", 30)
SANS_BIG = font("DejaVuSans-Bold.ttf", 34)
SANS = font("DejaVuSans-Bold.ttf", 22)
SANS_SM = font("DejaVuSans-Bold.ttf", 17)
SANS_TXT = font("DejaVuSans.ttf", 19)
SANS_TINY = font("DejaVuSans.ttf", 15)

INK = (18, 18, 18)
PAPER = (250, 246, 238)
RULE = (120, 110, 95)
ACCENT = (178, 34, 34)
NEON_PINK = (255, 45, 149)
NEON_CYAN = (0, 229, 255)
NEON_YELLOW = (255, 214, 64)
DUSK_TOP = (26, 16, 66)
DUSK_BOT = (84, 24, 96)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def skyline_panel(draw, x, y, w, h):
    """A neon dusk skyline for the GTA VI lead panel."""
    for i in range(h):
        t = i / max(1, h - 1)
        r = int(DUSK_TOP[0] + (DUSK_BOT[0] - DUSK_TOP[0]) * t)
        g = int(DUSK_TOP[1] + (DUSK_BOT[1] - DUSK_TOP[1]) * t)
        b = int(DUSK_TOP[2] + (DUSK_BOT[2] - DUSK_TOP[2]) * t)
        draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # sun
    cx, cy, rad = x + w // 2, y + h // 2 - 10, 58
    for rr in range(rad, 0, -1):
        t = rr / rad
        col = (255, int(120 + 90 * t), int(60 + 120 * t))
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col)
    # buildings
    import random

    rng = random.Random(19)
    bx = x + 8
    while bx < x + w - 30:
        bw = rng.randint(34, 72)
        bh = rng.randint(70, h - 48)
        top = y + h - bh
        draw.rectangle([bx, top, bx + bw, y + h], fill=(12, 8, 30))
        draw.rectangle([bx, top, bx + bw, top + 4], fill=NEON_PINK)
        for wy in range(top + 12, y + h - 10, 18):
            for wx in range(bx + 6, bx + bw - 6, 14):
                if rng.random() < 0.45:
                    draw.rectangle(
                        [wx, wy, wx + 6, wy + 8],
                        fill=rng.choice([NEON_CYAN, NEON_YELLOW, (255, 255, 255)]),
                    )
        bx += bw + 6
    # street glow
    draw.rectangle([x, y + h - 14, x + w, y + h], fill=NEON_PINK)
    draw.text((x + 14, y + h - 54), "VICE CITY", font=SANS_BIG, fill=(255, 255, 255))
    draw.text(
        (x + 14, y + 10),
        "AFTER A 13-YEAR WAIT",
        font=SANS_SM,
        fill=NEON_YELLOW,
    )


def mini_panel(draw, x, y, w, h, kind):
    """Small drawn graphic for a column story."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    if kind == "capitol":
        draw.rectangle([x, y + h - 16, x + w, y + h], fill=(70, 90, 120))
        draw.polygon(
            [(x + w / 2, y + 6), (x + 14, y + h - 16), (x + w - 14, y + h - 16)],
            fill=(200, 205, 215),
        )
        draw.ellipse(
            [x + w / 2 - 12, y + 18, x + w / 2 + 12, y + 42], fill=(245, 245, 245)
        )
        draw.rectangle([x + w / 2 - 3, y + 42, x + w / 2 + 3, y + h - 16], fill=(245, 245, 245))
    elif kind == "flags":
        cols = [(178, 34, 34), (255, 214, 64), (34, 120, 178)]
        for i, c in enumerate(cols):
            fx = x + 12 + i * (w - 24) // 3
            draw.rectangle([fx, y + 10, fx + (w - 24) // 3 - 6, y + h - 10], fill=c)
            draw.line([fx + 4, y + 10, fx + 4, y + h - 6], fill=(60, 60, 60), width=3)
    elif kind == "gulf":
        draw.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
        for i in range(5):
            yy = y + 14 + i * 14
            draw.line([(x + 8, yy), (x + w - 8, yy)], fill=(0, 180, 220), width=3)
        draw.polygon(
            [(x + w / 2, y + 8), (x + w / 2 - 26, y + 44), (x + w / 2 + 26, y + 44)],
            fill=(255, 180, 40),
        )
    elif kind == "euro":
        draw.rectangle([x, y, x + w, y + h], fill=(30, 60, 130))
        for i in range(12):
            import math

            ang = 2 * math.pi * i / 12
            sx = x + w / 2 + int(0.32 * w * math.cos(ang))
            sy = y + h / 2 + int(0.32 * h * math.sin(ang))
            draw.regular_polygon((sx, sy, 5), 5, fill=NEON_YELLOW)
        draw.text((x + w / 2 - 22, y + h / 2 - 18), "€", font=SERIF, fill=(255, 255, 255))
    elif kind == "space":
        draw.rectangle([x, y, x + w, y + h], fill=(5, 5, 20))
        import random

        rng = random.Random(7)
        for _ in range(26):
            sx = rng.randint(x + 4, x + w - 4)
            sy = rng.randint(y + 4, y + h - 4)
            draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        draw.ellipse([x + w / 2 - 20, y + h / 2 - 20, x + w / 2 + 20, y + h / 2 + 20],
                     fill=(210, 190, 140))
        draw.ellipse([x + w / 2 - 12, y + h / 2 - 26, x + w / 2 + 12, y + h / 2 - 8],
                     fill=(160, 140, 100))
    elif kind == "storm":
        draw.rectangle([x, y, x + w, y + h], fill=(90, 110, 140))
        cx, cy = x + w / 2, y + h / 2
        for r in (30, 23, 16, 9):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=4)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 36  # margin

    # --- masthead ---
    d.text((m, 18), "THE WORLD TODAY", font=SERIF_BIG, fill=INK)
    d.line([(m, 96), (W - m, 96)], fill=INK, width=3)
    d.text((m, 104), "THURSDAY 19 NOVEMBER 2026", font=SANS_BIG, fill=ACCENT)
    d.text(
        (W - m - d.textlength("ONE DAY, ONE IMAGE", font=SANS_SM), 112),
        "ONE DAY, ONE IMAGE",
        font=SANS_SM,
        fill=INK,
    )
    d.line([(m, 146), (W - m, 146)], fill=INK, width=2)

    # --- lead story: GTA VI ---
    ly = 162
    d.text((m, ly), "GRAND THEFT AUTO VI", font=font("DejaVuSerif-Bold.ttf", 54), fill=INK)
    d.text(
        (m, ly + 62),
        "BEGINS GLOBAL ROLLOUT AFTER A 13-YEAR WAIT",
        font=SANS_BIG,
        fill=ACCENT,
    )
    skyline_panel(d, m, ly + 108, W - 2 * m, 170)
    y = ly + 108 + 170 + 12
    y = para(
        d, m, y,
        "Gamers finally enter Vice City today as Rockstar's long-awaited "
        "sequel reaches stores and downloads worldwide, ending the longest "
        "wait in the series' history.",
        SANS_TXT, W - 2 * m, 26,
    )
    d.line([(m, y + 8), (W - m, y + 8)], fill=RULE, width=1)
    y += 22

    # --- six stories in two rows of three columns ---
    stories = [
        ("capitol", "JEFFRIES NOMINATED FOR SPEAKER",
         "Democrats nominate Hakeem Jeffries — set to be the first "
         "Black Speaker."),
        ("flags", "TRUMP, XI AND PUTIN MEET",
         "The three leaders hold trilateral talks in Shenzhen at the "
         "APEC summit."),
        ("gulf", "US AND IRAN EXCHANGE FIRE",
         "Strikes flare again as Iran widens attacks on Gulf states."),
        ("euro", "EU'S €45BN LOAN FOR UKRAINE",
         "Brussels proposes a €45 billion loan, repaid only after "
         "Russia pays reparations."),
        ("space", "VOYAGER 1: ONE LIGHT-DAY OUT",
         "NASA confirms the probe is one light-day from Earth — "
         "a milestone announced today."),
        ("storm", "CYCLONE AKVAN BEARS DOWN",
         "The storm heads for India's east coast, with landfall "
         "expected on 20 November."),
    ]
    col_w = (W - 2 * m - 2 * 20) // 3
    panel_h, head_h = 64, 44
    row_h = 18 + panel_h + 6 + head_h + 4 + 3 * 22 + 8
    for idx, (kind, head, body) in enumerate(stories):
        r, c = divmod(idx, 3)
        x = m + c * (col_w + 20)
        yy = y + r * row_h
        d.text((x, yy), "WORLD", font=SANS_TINY, fill=ACCENT)
        mini_panel(d, x, yy + 18, col_w, panel_h, kind)
        hy = yy + 18 + panel_h + 6
        hy = para(d, x, hy, head, SANS, col_w, 22)
        para(d, x, hy + 4, body, SANS_TXT, col_w, 22)

    # --- footer ---
    d.line([(m, H - 44), (W - m, H - 44)], fill=INK, width=2)
    footer = ("THE WORLD TODAY — 19 NOVEMBER 2026  •  GTA VI  •  JEFFRIES  •  "
              "SHENZHEN  •  GULF  •  €45BN  •  VOYAGER 1  •  AKVAN")
    while d.textlength(footer, font=SANS_TINY) > W - 2 * m:
        footer = footer.rsplit("  •  ", 1)[0]
    d.text((m, H - 36), footer, font=SANS_TINY, fill=INK)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()
