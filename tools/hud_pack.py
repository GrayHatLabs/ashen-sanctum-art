"""Turns the chosen OpenAI HUD images (tools/oai_hud.py) into game-size pixel art, plus a mockup over a game frame.

    python tools/hud_pack.py <left_n> <right_n> <panel_n> [hole_px]
writes generated/hud/hud_orb_l.png, hud_orb_r.png, hud_panel.png (+ hud.json with the globe centres) and
generated/hud/mockup.png.
"""
import json
import math
import sys
from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "generated" / "oai" / "hud" / "raw"
OUT = ROOT / "generated" / "hud"
GAME = Path("D:/projects/AshenSanctum")
W, H, HUD_H = 640, 360, 52
COLORS = 48
DROP = 16
MODULE, SOCKET0 = 97, 132  # one strap + socket; the first socket clear of the angel  # the housings' pedestals run off the bottom of the screen


def hole(im):
    """The orb's hole: the biggest transparent region that doesn't touch the image edge -> (cx, cy, r)."""
    a = im.getchannel("A").load()
    w, h = im.size
    seen = bytearray(w * h)
    best = None
    for sy in range(0, h, 4):
        for sx in range(0, w, 4):
            if seen[sy * w + sx] or a[sx, sy] >= 128:
                continue
            q, pts, edge = deque([(sx, sy)]), [], False
            seen[sy * w + sx] = 1
            while q:
                x, y = q.popleft()
                pts.append((x, y))
                if x in (0, w - 1) or y in (0, h - 1):
                    edge = True
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and a[nx, ny] < 128:
                        seen[ny * w + nx] = 1
                        q.append((nx, ny))
            if not edge and (best is None or len(pts) > len(best)):
                best = pts
    cx = sum(p[0] for p in best) / len(best)
    cy = sum(p[1] for p in best) / len(best)
    return cx, cy, math.sqrt(len(best) / math.pi)


def pixelize(im, size):
    small = im.resize(size, Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    return out


def orb(n_name, hole_px):
    from PIL import ImageEnhance
    im = Image.open(RAW / f"{n_name}.png").convert("RGBA")
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.3)).enhance(1.15)
    box = im.getbbox()
    im = im.crop(box)
    cx, cy, r = hole(im)
    k = (hole_px / 2) / r
    out = pixelize(im, (round(im.width * k), round(im.height * k)))
    return out, (round(cx * k), round(cy * k))


def panel(n_name, body_h=HUD_H):
    """panel_1's pieces (in its alpha-cropped coordinates), rebuilt to the screen width: the right end (mirrored for the
    left, which the model cut off), the strap-and-socket module tiled between, and the skull-and-thorns crest on top."""
    from PIL import ImageEnhance, ImageOps
    im = Image.open(RAW / f"{n_name}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v >= 128 else 0).getbbox())
    im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.45)).enhance(1.25)
    top, bot = 118, im.height
    ky = body_h / (bot - top)
    kx = ky * 2.2  # stretched sideways: the straps and sockets read better wider
    def piece(x0, x1, y0=top, y1=bot, k=None):
        c = im.crop((x0, y0, x1, y1))
        return c.resize((max(1, round(c.width * (k or kx))), max(1, round(c.height * (k or ky)))), Image.LANCZOS)
    end = piece(1370, im.width)
    module = piece(248, 648)
    module = module.resize((MODULE, body_h), Image.LANCZOS)
    crest = piece(330, 1000, 0, 132, ky * 1.25)
    crest_h = crest.height - round(14 * ky * 1.25)
    big = Image.new("RGBA", (W, body_h + crest_h))
    # Straps at SOCKET0 - 8 + k * MODULE, so the game's sockets (render.rs HUD_SOCKETS) line up with the art.
    x = SOCKET0 - 8 - MODULE * 2
    while x < W:
        big.alpha_composite(module, (x, crest_h))
        x += MODULE
    big.alpha_composite(ImageOps.mirror(end), (0, crest_h))
    big.alpha_composite(end, (W - end.width, crest_h))
    big.alpha_composite(crest, (W // 2 - crest.width // 2, 0))
    a = big.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = big.convert("RGB").quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    return out


def globe(img, cx, cy, r, frac, dark, hi):
    px = img.load()
    level = cy + r - 2 * r * frac
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y > r * r:
                continue
            if cy + y >= level:
                s = max(0.0, 1 - math.hypot(x + r / 3, y + r / 3) / (r * 1.6))
                c = tuple(int(d * 0.5 + (h - d * 0.5) * s * 0.7) for d, h in zip(dark, hi))
            else:
                c = (12, 10, 10)
            px[cx + x, cy + y] = c + (255,)


def main():
    ln, rn, pn = sys.argv[1:4]
    hole_px = int(sys.argv[4]) if len(sys.argv) > 4 else 52
    OUT.mkdir(parents=True, exist_ok=True)
    L, lc = orb(f"left_{ln}", hole_px)
    R, rc = orb(f"right_{rn}", hole_px)
    P = panel(f"panel_{pn}")
    L.save(OUT / "hud_orb_l.png")
    R.save(OUT / "hud_orb_r.png")
    P.save(OUT / "hud_panel.png")
    json.dump({"l": [L.width, L.height, *lc], "r": [R.width, R.height, *rc], "panel_h": P.height}, open(OUT / "hud.json", "w"))
    # Mockup: the orbs' bottoms sit at the screen's bottom edge.
    frame = Image.open(GAME / "snapshots" / "act2_wilds.bmp").convert("RGBA").crop((0, 0, W, H - HUD_H)).resize((W, H - HUD_H))
    m = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    m.alpha_composite(frame, (0, 0))
    m.alpha_composite(P, (0, H - P.height))
    r = hole_px // 2
    lx, ly = 0, H - L.height + DROP
    rx, ry = W - R.width, H - R.height + DROP
    globe(m, lx + lc[0], ly + lc[1], r, 0.7, (176, 24, 24), (255, 96, 80))
    globe(m, rx + rc[0], ry + rc[1], r, 0.45, (24, 48, 176), (96, 144, 255))
    m.alpha_composite(L, (lx, ly))
    m.alpha_composite(R, (rx, ry))
    m.save(OUT / "mockup.png")
    m.resize((W * 2, H * 2), Image.NEAREST).save(OUT / "mockup_x2.png")
    print("L", L.size, lc, "R", R.size, rc, "panel", P.size)


if __name__ == "__main__":
    main()
