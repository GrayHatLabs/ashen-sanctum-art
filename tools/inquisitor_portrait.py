"""The Inquisitor's class-select portrait, take 3 (the user, 2026-10-06): the v2 figure, darkened gold
armor, the darkened gold halo of spikes with an arching band, and an iron chain down to the censer of holy fire.
A painted guide, then bitforge redraws over it at a few strengths.

    python tools/inquisitor_portrait.py guide    generated/inquisitor_hero/guide.png
    python tools/inquisitor_portrait.py redraw   generated/inquisitor_hero/p3_s{400,500,600}.png
    python tools/inquisitor_portrait.py review   generated/inquisitor_portrait_review.png
"""
import math
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import pixellab  # noqa: E402

D = gen.GEN / "inquisitor_hero"
BG = (136, 134, 138, 255)
IRON = (62, 49, 28, 255)
STEEL = (122, 100, 58, 255)
TIP = (200, 168, 100, 255)


def darkened_gold(p):
    lum = 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]
    return tuple(int((c * 0.65 + lum * 0.35) * 0.66) for c in p[:3]) + (255,)


def guide_sprite():
    """Take 4 (the user): her in-game sprite, standing straight, scaled up into a portrait guide."""
    from inquisitor_halo import fix_frame
    spr = fix_frame(Image.open(D / "rotation_urls_south.png"))
    spr = spr.crop(spr.getbbox())
    k = 182 / spr.height
    fig = spr.resize((int(spr.width * k), 182), Image.NEAREST)
    out = Image.new("RGBA", (140, 200), BG)
    ox = (140 - fig.width) // 2
    out.alpha_composite(fig, (ox, 10))
    op = out.load()

    def put(x, y, c, r=0):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = int(round(x)) + dx, int(round(y)) + dy
                if 0 <= X < 140 and 0 <= Y < 200:
                    op[X, Y] = c

    # Her right hand (viewer's left): find the lowest skin-ish pixel on that side.
    hand = None
    for y in range(199, 0, -1):
        for x in range(0, 70):
            p = op[x, y]
            if p[0] > 150 and p[1] > 100 and p[2] > 80 and p[0] > p[2] + 30:
                hand = (x, y)
                break
        if hand:
            break
    hand = hand or (ox + 4, 120)
    cen = (hand[0] - 6, hand[1] + 30)
    n = 16
    for s_ in range(n + 1):
        t = s_ / n
        put(hand[0] + (cen[0] - hand[0]) * t, hand[1] + (cen[1] - hand[1]) * t, (40, 38, 42, 255) if s_ % 2 else (120, 116, 110, 255), 0)
    cx, cy = cen
    for y in range(-7, 9):
        w = int(6 * math.sqrt(max(0.0, 1 - (y / 8) ** 2)))
        for x in range(-w, w + 1):
            c = (120, 92, 40, 255) if (x + y) % 4 else (70, 54, 26, 255)
            if abs(x) < w - 1 and y % 4 == 0 and abs(x) % 3 == 0:
                c = (255, 240, 190, 255)
            put(cx + x, cy + y, c)
    for a in range(8):
        ang = a / 8 * math.tau
        for t in range(7, 10):
            put(cx + math.cos(ang) * t, cy + math.sin(ang) * t * 1.1, (150, 120, 60, 255))
    out.save(D / "guide4.png")
    print("saved guide4", hand, flush=True)


def redraw4():
    desc = ("full body gothic inquisitor woman standing straight facing forward, legs straight, arms at her sides, black hood, "
            "pale face, a darkened gold halo of spikes with a band arching through them behind her head, black leather armor "
            "with darkened gold shoulder plates, long black coat with crimson lining, a spiked censer hanging on a chain from "
            "her hand glowing with holy fire, plain grey background, cel shading, bold outlines")
    for strength in (450, 550, 650):
        out = D / f"p4_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{desc}, anatomically correct, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "guide4.png"),
            "init_image_strength": strength,
            "negative_description": "bent legs, crouching, walking pose, crown, bright gold, mask, extra hands, extra arms, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"inquisitor portrait p4 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "guide4.png"] + [D / f"p4_s{s}.png" for s in (450, 550, 650)]
    gen.review(gen.GEN / "inquisitor_portrait_review.png", *[p for p in ps if p.exists()])


def guide():
    src = Image.open(D / "full_c.png").convert("RGBA")
    # Key out the flat grey, shrink, and drop her lower for headroom.
    px = src.load()
    bg = px[0, 0]
    for y in range(src.height):
        for x in range(src.width):
            if all(abs(px[x, y][i] - bg[i]) < 14 for i in range(3)):
                px[x, y] = (0, 0, 0, 0)
    k = 0.84
    fig = src.resize((int(src.width * k), int(src.height * k)), Image.NEAREST)
    fp = fig.load()
    for y in range(fig.height):
        for x in range(fig.width):
            p = fp[x, y]
            if p[3] and p[0] > p[2] + 40 and p[1] > p[2] + 15 and p[0] > 90:
                fp[x, y] = darkened_gold(p)
    out = Image.new("RGBA", (140, 200), BG)
    ox, oy = 12, 30
    # The halo first, behind her: spikes and an iron arch.
    hx, hy = ox + 70 * k, oy + 12 * k
    op = out.load()

    def put(x, y, c, r=0):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = int(round(x)) + dx, int(round(y)) + dy
                if 0 <= X < 140 and 0 <= Y < 200:
                    op[X, Y] = c

    for i in range(11):
        a = math.pi + 0.15 + i / 10 * (math.pi - 0.3)
        length = 30 if i % 2 == 0 else 22
        for t in range(8, length + 1):
            put(hx + math.cos(a) * t, hy + math.sin(a) * t, TIP if t >= length - 2 else STEEL, 1 if t < length - 6 else 0)
    for j in range(160):
        a = math.pi + 0.05 + j / 159 * (math.pi - 0.1)
        put(hx + math.cos(a) * 17, hy + math.sin(a) * 17, (168, 138, 78, 255), 1)
        put(hx + math.cos(a) * 19, hy + math.sin(a) * 19, (96, 78, 44, 255))
    out.alpha_composite(fig, (ox, oy))
    # The chain from her right hand (viewer's right) down to the censer.
    hand = (ox + 104 * k, oy + 66 * k)
    cen = (hand[0] + 8, hand[1] + 48)
    n = 22
    for s in range(n + 1):
        t = s / n
        x = hand[0] + (cen[0] - hand[0]) * t + math.sin(t * math.pi) * 3
        y = hand[1] + (cen[1] - hand[1]) * t
        put(x, y, (40, 38, 42, 255) if s % 2 else (120, 116, 110, 255), 1 if s % 2 else 0)
    # The censer: a spiked darkened-gold lantern, holy fire through its openings.
    cx, cy = cen
    for y in range(-9, 11):
        w = int(7 * math.sqrt(max(0.0, 1 - (y / 10) ** 2)))
        for x in range(-w, w + 1):
            c = (120, 92, 40, 255) if (x + y) % 4 else (70, 54, 26, 255)
            if abs(x) < w - 1 and y % 4 == 0 and abs(x) % 3 == 0:
                c = (255, 240, 190, 255)
            put(cx + x, cy + y, c)
    for a in range(8):
        ang = a / 8 * math.tau
        for t in range(8, 12):
            put(cx + math.cos(ang) * t, cy + math.sin(ang) * t * 1.1, (150, 120, 60, 255))
    put(cx, cy - 12, (120, 92, 40, 255), 1)
    out.save(D / "guide.png")
    print("saved guide", flush=True)


DESC = (
    "full body gothic inquisitor woman in a black hood, a darkened gold halo of long spikes with a gold band arching through them "
    "behind her head, black leather armor with darkened gold plates, black coat, holding a spiked censer hanging on an "
    "iron chain glowing with white-gold holy fire, plain grey background, cel shading, bold outlines"
)


def redraw():
    for strength in (400, 500, 600):
        out = D / f"p3_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{DESC}, anatomically correct, exactly two arms, exactly two hands, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "guide.png"),
            "init_image_strength": strength,
            "negative_description": "crown, bright gold, extra hands, extra arms, duplicated limbs, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"inquisitor portrait p3 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)


def review():
    ps = [D / "guide.png"] + [D / f"p3_s{s}.png" for s in (400, 500, 600)]
    gen.review(gen.GEN / "inquisitor_portrait_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"guide": guide, "redraw": redraw, "review": review, "guide4": guide_sprite, "redraw4": redraw4}[sys.argv[1]]()
