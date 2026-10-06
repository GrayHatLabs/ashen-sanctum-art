"""The Inquisitor's halo, drawn onto her sprite frames (the user's design, 2026-10-06): spikes radiating
behind her head with a metal band arching through them, all in darkened gold like her armor. PixelLab drew a gold sun halo; this
strips it, dulls her gold armor to tarnished gold (the user's call), and paints the halo instead, the same
on every frame and direction. pack.py calls fix_frame() on every inquisitor_hero frame.

    python tools/inquisitor_halo.py      preview: generated/inquisitor_halo_preview.png
"""
import math
from pathlib import Path

from PIL import Image

GEN = Path(__file__).resolve().parent.parent / "generated"
# Darkened gold, like her armor (the user, 2026-10-06).
IRON = (62, 49, 28, 255)
STEEL = (122, 100, 58, 255)
TIP = (200, 168, 100, 255)
BAND = (96, 78, 44, 255)
BAND_HI = (168, 138, 78, 255)


def _gold(p):
    return p[3] > 0 and p[0] > 140 and p[1] > 100 and p[2] < 120 and p[0] > p[2] + 60


def _goldish(p):
    return p[3] > 0 and p[0] > p[2] + 40 and p[1] > p[2] + 15 and p[0] > 90


def fix_frame(im, head_rows=26):
    """Returns a new, taller frame (10 px more headroom on top) with the iron halo."""
    im = im.convert("RGBA")
    out = Image.new("RGBA", (im.width, im.height + 10), (0, 0, 0, 0))
    out.alpha_composite(im, (0, 10))
    px = out.load()
    top = head_rows + 10
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if y < top and _gold(p):
                px[x, y] = (0, 0, 0, 0)
            elif _goldish(p):
                # Her armor stays gold, but tarnished: less saturated, darkened (the user, 2026-10-06).
                lum = 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]
                px[x, y] = tuple(int((c * 0.65 + lum * 0.35) * 0.66) for c in p[:3]) + (p[3],)
    # Her head: the top of what's left.
    head = None
    for y in range(out.height):
        xs = [x for x in range(out.width) if px[x, y][3] > 0]
        if xs:
            head = (sum(xs) / len(xs), y)
            break
    if head is None:
        return out
    cx, cy = head[0], head[1] + 6

    def put(x, y, c, over=False):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < out.width and 0 <= y < out.height and (over or px[x, y][3] == 0):
            px[x, y] = c

    n = 9
    for k in range(n):
        a = math.pi + 0.12 + k / (n - 1) * (math.pi - 0.24)
        length = 15 if k % 2 == 0 else 11
        for t in range(5, length + 1):
            put(cx + math.cos(a) * t, cy + math.sin(a) * t, TIP if t >= length - 1 else STEEL)
            if t < length - 3:
                put(cx + math.cos(a) * t + math.sin(a), cy + math.sin(a) * t - math.cos(a), IRON)
    for j in range(90):
        a = math.pi + 0.05 + j / 89 * (math.pi - 0.1)
        put(cx + math.cos(a) * 9, cy + math.sin(a) * 9, BAND_HI, True)
        put(cx + math.cos(a) * 10, cy + math.sin(a) * 10, BAND, True)
    return out


if __name__ == "__main__":
    outs = []
    for d in ["south", "south-east", "east", "north-east", "north"]:
        p = GEN / "inquisitor_hero" / f"rotation_urls_{d}.png"
        outs.append(fix_frame(Image.open(p)).crop((12, 0, 68, 70)))
    sheet = Image.new("RGBA", (sum(o.width + 8 for o in outs), 70), (30, 28, 34, 255))
    x = 0
    for o in outs:
        sheet.alpha_composite(o, (x, 0))
        x += o.width + 8
    sheet = sheet.resize((sheet.width * 5, sheet.height * 5), Image.NEAREST)
    sheet.save(GEN / "inquisitor_halo_preview.png")
    print("saved", GEN / "inquisitor_halo_preview.png")
