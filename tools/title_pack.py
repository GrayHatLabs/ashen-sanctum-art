"""Turns the chosen OpenAI title art (tools/oai_title.py) into game art: the painted background cut for the wide
(640x360) and handheld (640x480) screens, and the ASHEN SANCTUM logo, all as pixel art.

    python tools/title_pack.py <bg_n> <logo_n>
writes generated/title/title_bg.png, title_bg_tall.png, title_logo.png (pack.py picks them up).
"""
import sys
from pathlib import Path

from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "generated" / "oai" / "title" / "raw"
OUT = ROOT / "generated" / "title"
COLORS = 64
LOGO_W = 330


def quant(im, colors=COLORS):
    a = im.getchannel("A").point(lambda v: 255 if v >= 128 else 0) if im.mode == "RGBA" else None
    rgb = im.convert("RGB").quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    if a is not None:
        out.putalpha(a)
    return out


def cover(im, w, h, focus_x=0.55):
    """Scale to cover w x h, then crop (keeping the cathedral, a little right of centre, in view)."""
    k = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = int((im.width - w) * focus_x)
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def outline(im, col=(16, 8, 6, 255)):
    px = im.load()
    out = im.copy()
    po = out.load()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3]:
                continue
            if any(0 <= x + dx < im.width and 0 <= y + dy < im.height and px[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                po[x, y] = col
    return out


def main():
    bn, ln = sys.argv[1:3]
    OUT.mkdir(parents=True, exist_ok=True)
    bg = Image.open(RAW / f"bg_{bn}.png").convert("RGB")
    bg = ImageEnhance.Contrast(ImageEnhance.Brightness(bg).enhance(1.12)).enhance(1.08)
    quant(cover(bg, 640, 360)).save(OUT / "title_bg.png")
    quant(cover(bg, 640, 480)).save(OUT / "title_bg_tall.png")
    logo = Image.open(RAW / f"logo_{ln}.png").convert("RGBA")
    logo = logo.crop(logo.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox())
    # Brighter, warmer gold so it reads over the dark painting.
    rgb = ImageEnhance.Contrast(ImageEnhance.Brightness(logo.convert("RGB")).enhance(1.7)).enhance(1.25)
    logo = Image.merge("RGBA", (*rgb.split(), logo.getchannel("A")))
    k = LOGO_W / logo.width
    logo = logo.resize((LOGO_W, round(logo.height * k)), Image.LANCZOS)
    outline(quant(logo, 48)).save(OUT / "title_logo.png")
    print("title art", Image.open(OUT / "title_logo.png").size)


if __name__ == "__main__":
    main()
