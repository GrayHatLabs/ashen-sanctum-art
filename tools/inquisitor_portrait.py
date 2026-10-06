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


def paint():
    """Take 5 (the user: "the portrait, not the sprite image"): repaint the approved design freely, as a
    detailed painted portrait like the other heroes', keeping her pose, halo and darkened gold."""
    desc = ("highly detailed painted portrait art of a gothic inquisitor woman standing straight, full body, black hood framing "
            "a pale severe face, a halo of long darkened gold spikes with a gold band arching through them behind her head, "
            "black leather corset armor with darkened gold shoulder plates and buckles, long black coat with crimson lining, "
            "tall black boots, a spiked censer on a chain in her hand glowing with white-gold holy fire, plain grey background")
    for strength in (180, 260, 340):
        out = D / f"p5_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{desc}, anatomically correct, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "detailed shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "p4_final.png"),
            "init_image_strength": strength,
            "negative_description": "bent legs, crouching, crown, bright yellow gold, mask, blocky, low detail, extra hands, extra arms, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"inquisitor portrait p5 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "p4_final.png"] + [D / f"p5_s{s}.png" for s in (180, 260, 340)]
    gen.review(gen.GEN / "inquisitor_portrait_review.png", *[p for p in ps if p.exists()])


def paint_guide(src_path, out_name, head, hand, chains, blades=False, k=0.86, ox=10, oy=26):
    """A figure keyed out and dropped lower, a golden spiked halo with an arching band behind its head,
    gold chains wrapped around the body, and a censer on a gold chain from one hand.
    head / hand / chains are in the source image's pixels."""
    src = Image.open(src_path).convert("RGBA")
    px = src.load()
    bg = px[0, 0]
    for y in range(src.height):
        for x in range(src.width):
            p = px[x, y]
            if all(abs(p[i] - bg[i]) < 14 for i in range(3)):
                px[x, y] = (0, 0, 0, 0)
            # 1C's two blades: light, unsaturated grey reaching out past her coat.
            elif blades and 82 <= y <= 112 and (x < 42 or x > 98) and min(p[:3]) > 120 and max(p[:3]) - min(p[:3]) < 30:
                px[x, y] = (0, 0, 0, 0)
    fig = src.resize((int(src.width * k), int(src.height * k)), Image.NEAREST)
    out = Image.new("RGBA", (140, 200), BG)
    op = out.load()
    GOLD, GOLD_HI, GOLD_DK = (196, 150, 58, 255), (240, 204, 110, 255), (120, 86, 30, 255)

    def put(x, y, c, r=0):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = int(round(x)) + dx, int(round(y)) + dy
                if 0 <= X < 140 and 0 <= Y < 200:
                    op[X, Y] = c

    f = lambda x, y: (ox + x * k, oy + y * k)
    hx, hy = f(*head)
    for i in range(11):
        a = math.pi + 0.15 + i / 10 * (math.pi - 0.3)
        length = 28 if i % 2 == 0 else 20
        for t in range(8, length + 1):
            put(hx + math.cos(a) * t, hy + math.sin(a) * t, GOLD_HI if t >= length - 2 else GOLD, 1 if t < length - 6 else 0)
    for j in range(160):
        a = math.pi + 0.05 + j / 159 * (math.pi - 0.1)
        put(hx + math.cos(a) * 16, hy + math.sin(a) * 16, GOLD_HI, 1)
        put(hx + math.cos(a) * 18, hy + math.sin(a) * 18, GOLD_DK)
    out.alpha_composite(fig, (ox, oy))

    def chain(x0, y0, x1, y1, sag=0.0):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) / 2) + 1
        for s_ in range(n + 1):
            t = s_ / n
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t + math.sin(t * math.pi) * sag
            put(x, y, GOLD_HI if s_ % 2 else GOLD_DK, 0 if s_ % 2 else 1)

    for (x0, y0, x1, y1, sag) in chains:
        chain(*f(x0, y0), *f(x1, y1), sag)
    hx2, hy2 = f(*hand)
    cen = (hx2 - 4, hy2 + 40)
    chain(hx2, hy2, cen[0], cen[1] - 8, 2)
    cx, cy = cen
    for y in range(-7, 9):
        w = int(6 * math.sqrt(max(0.0, 1 - (y / 8) ** 2)))
        for x in range(-w, w + 1):
            c = GOLD if (x + y) % 4 else GOLD_DK
            if abs(x) < w - 1 and y % 4 == 0 and abs(x) % 3 == 0:
                c = (255, 244, 200, 255)
            put(cx + x, cy + y, c)
    for a in range(8):
        ang = a / 8 * math.tau
        for t in range(7, 10):
            put(cx + math.cos(ang) * t, cy + math.sin(ang) * t * 1.1, GOLD_DK)
    out.save(D / out_name)
    print("saved", out_name, flush=True)


def guide6():
    """Take 6 (the user): 1C's stance with the halo, gold chains and censer."""
    v1 = gen.GEN / "_old" / "inquisitor_hero_v1"
    chains = [(50, 40, 90, 82, 2), (88, 40, 52, 78, 3), (48, 86, 92, 86, 4), (50, 94, 90, 94, 5)] + [(40, 70 + r * 5, 50, 72 + r * 5, 1) for r in range(3)]
    paint_guide(v1 / "full_c.png", "guide6.png", (70, 14), (46, 92), chains, blades=True)


def guide7():
    """Take 7 (the user: "use 5B as the base"): 5B's tall slender robed figure, with the golden spiked
    halo, gold chains wrapped around her body and the censer on its chain."""
    chains = [(58, 46, 86, 74, 2), (86, 46, 58, 72, 3), (55, 80, 88, 80, 4), (56, 88, 87, 88, 5)] + [(32, 80 + r * 4, 44, 82 + r * 4, 1) for r in range(3)]
    paint_guide(D / "p5_s260.png", "guide7.png", (72, 16), (37, 92), chains)


def redraw7():
    desc = ("full body gothic inquisitor woman standing tall and slender in a long flowing black hooded robe, long ash-blonde "
            "hair, a golden halo of long spikes with a gold band arching through them behind her head, gold chains wrapped "
            "around her body, black leather corset, a spiked gold censer hanging on a chain from her hand glowing with holy "
            "fire, plain grey background, highly detailed, cel shading, bold clean outlines")
    for strength in (380, 460, 540):
        out = D / f"p7_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{desc}, anatomically correct, two hands, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "guide7.png"),
            "init_image_strength": strength,
            "negative_description": "sword, blade, crown, mask, bent legs, crouching, extra hands, extra arms, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"inquisitor portrait p7 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "guide7.png"] + [D / f"p7_s{s}.png" for s in (380, 460, 540)]
    gen.review(gen.GEN / "inquisitor_portrait_review.png", *[p for p in ps if p.exists()])


def redraw6():
    desc = ("full body gothic inquisitor woman standing tall and slender, long ash-blonde hair, black hood, a golden halo of long "
            "spikes with a gold band arching through them behind her head, gold chains wrapped around her body, black leather "
            "corset armor with steel plates, long split black coat, tall black boots, a spiked gold censer hanging on a chain "
            "from her hand glowing with holy fire, plain grey background, highly detailed, cel shading, bold clean outlines")
    for strength in (380, 460, 540):
        out = D / f"p6_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{desc}, anatomically correct, two hands, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "guide6.png"),
            "init_image_strength": strength,
            "negative_description": "sword, blade, crown, mask, bent legs, crouching, extra hands, extra arms, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"inquisitor portrait p6 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "guide6.png"] + [D / f"p6_s{s}.png" for s in (380, 460, 540)]
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
    {"guide": guide, "redraw": redraw, "review": review, "guide4": guide_sprite, "redraw4": redraw4, "paint": paint, "guide6": guide6, "redraw6": redraw6, "guide7": guide7, "redraw7": redraw7}[sys.argv[1]]()
