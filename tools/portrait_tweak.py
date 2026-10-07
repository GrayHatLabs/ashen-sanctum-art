"""Small code recolours of the final OpenAI portraits that keep everything else, the face above all, exactly as is
(the user, 2026-10-06: the Druid's orb should glow green; the Reaper's hair should be silver, not blonde).
The previous versions are kept as generated/oai/final/<hero>_v2.png.

    python tools/portrait_tweak.py
"""
import shutil
from pathlib import Path

from PIL import Image

FINAL = Path(__file__).resolve().parent.parent / "generated" / "oai" / "final"


def backup(hero):
    src, dst = FINAL / f"{hero}.png", FINAL / f"{hero}_v2.png"
    if not dst.exists():
        shutil.copy(src, dst)
    return Image.open(dst).convert("RGBA")


def lum(r, g, b):
    return 0.3 * r + 0.59 * g + 0.11 * b


def druid():
    im = backup("druid")
    px = im.load()
    cx, cy, rad = 171, 34, 8
    for y in range(cy - rad, cy + rad + 1):
        for x in range(cx - rad, cx + rad + 1):
            r, g, b, a = px[x, y]
            if not a or (x - cx) ** 2 + (y - cy) ** 2 > rad * rad:
                continue
            v = lum(r, g, b)
            # The orb is the light tan inside the twigs; the dark wood stays.
            if v > 45 and r > b * 1.05:
                k = min(1.0, max(0.0, (v - 45) / 140))
                px[x, y] = (int(40 + 90 * k), int(120 + 135 * k), int(40 + 70 * k), a)
    im.save(FINAL / "druid.png")


def reaper():
    im = backup("reaper")
    px = im.load()
    for y in range(30, 130):
        for x in range(60, 145):
            r, g, b, a = px[x, y]
            if not a:
                continue
            v = lum(r, g, b)
            # Blonde: light, yellow (green close to red, blue well under). Skin is pinker (green further below red).
            # Her face and neck stay exactly as they are.
            if ((x - 108) / 9.5) ** 2 + ((y - 65) / 16) ** 2 < 1 or (103 <= x <= 113 and 80 <= y <= 92):
                continue
            if v > 50 and g > r * 0.8 and b < r * 0.9 and r > 70:
                s = v * 1.02
                px[x, y] = (min(255, int(s * 0.93)), min(255, int(s * 0.97)), min(255, int(s * 1.06)), a)
    im.save(FINAL / "reaper.png")


if __name__ == "__main__":
    druid()
    reaper()
    print("ok")
