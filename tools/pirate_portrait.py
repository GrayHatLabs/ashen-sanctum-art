"""The Sky Pirate's class-select portrait (the user picked: keep the sprite, fix the portrait). Base: pirate_b
(blonde, ruffled sleeves). Guide: her staff erased, her right forearm turned to brass clockwork, an ornate brass
flintlock in that hand; then bitforge redraws over it. Also a new airship-deck background.

    python tools/pirate_portrait.py guide    generated/inventor/pguide.png
    python tools/pirate_portrait.py redraw   generated/inventor/pp_s{420,500,580}.png (+ review)
    python tools/pirate_portrait.py bg       generated/portrait_bg/pirate.png (the old one kept as pirate_v1.png)
"""
import math
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import pixellab  # noqa: E402

D = gen.GEN / "inventor"
BRASS, BRASS_HI, BRASS_DK = (176, 132, 52, 255), (232, 192, 104, 255), (104, 72, 26, 255)


def guide():
    im = Image.open(D / "pirate_b.png").convert("RGBA")
    px = im.load()
    bg = px[0, 0]

    def skin(p):
        return p[0] > 170 and p[1] > 120 and p[2] > 90 and p[0] > p[2] + 25

    # The staff (and the raised hand that held it): everything left of her sleeve, except the white
    # ruffled cuff and her lower hand; faint edge pixels too.
    def ruffle(p):
        return min(p[:3]) > 175

    for y in range(im.height):
        for x in range(20, 46):
            p = px[x, y]
            if all(abs(p[i] - bg[i]) < 30 for i in range(3)):
                px[x, y] = bg
                continue
            keep = ruffle(p) and 70 <= y <= 110 or (skin(p) and 86 <= y <= 104) or (x >= 44 and 36 <= y <= 110)
            if not keep:
                px[x, y] = bg

    def put(x, y, c, r=0):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = int(round(x)) + dx, int(round(y)) + dy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    px[X, Y] = c

    # A brass clockwork forearm from the elbow down to her hand, a gear at the elbow.
    (ex, ey), (hx, hy) = (46, 80), (40, 96)
    n = 18
    for s in range(n + 1):
        t = s / n
        x, y = ex + (hx - ex) * t, ey + (hy - ey) * t
        put(x, y, BRASS, 2)
        put(x - 1, y - 1, BRASS_HI)
        if s % 4 == 0:
            put(x + 2, y, BRASS_DK)
    for a in range(10):
        ang = a / 10 * math.tau
        put(ex + math.cos(ang) * 4, ey + math.sin(ang) * 4, BRASS_DK if a % 2 else BRASS_HI)
    put(ex, ey, BRASS_HI, 1)
    # The flintlock: grip in her hand, a long barrel pointing down and out.
    for s in range(22):
        put(hx - 4 - s * 0.8, hy + 6 + s * 0.55, (70, 60, 56, 255) if s % 5 else BRASS_DK, 1)
    for s in range(8):
        put(hx - 1 + s * 0.3, hy + 2 + s, (110, 60, 30, 255), 1)  # wooden grip
    put(hx - 3, hy + 5, BRASS_HI, 1)  # brass lock plate
    put(hx - 4 - 21 * 0.8, hy + 6 + 21 * 0.55, BRASS_HI, 1)  # muzzle ring
    im.save(D / "pguide.png")
    print("saved pguide", flush=True)


DESC = ("full body gothic steampunk pirate captain woman standing straight, black tricorn hat with red feathers, long wavy "
        "ash-blonde hair, black corset over a white ruffled blouse, long black and crimson coat with gold trim, a brass "
        "clockwork mechanical forearm with a gear at the elbow holding an ornate brass flintlock pistol, thigh-high black "
        "boots, plain grey background, cel shading, bold clean outlines")


def redraw():
    for strength in (420, 500, 580):
        out = D / f"pp_s{strength}.png"
        if out.exists():
            continue
        body = {
            "description": f"{DESC}, anatomically correct, two hands, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "init_image": pixellab.b64img(D / "pguide.png"),
            "init_image_strength": strength,
            "negative_description": "staff, spear, red hair, bent legs, crouching, extra hands, extra arms, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"pirate portrait {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "pguide.png"] + [D / f"pp_s{s}.png" for s in (420, 500, 580)]
    gen.review(gen.GEN / "pirate_portrait_review.png", *[p for p in ps if p.exists()])


def bg():
    d = gen.d_of("portrait_bg")
    old = d / "pirate.png"
    if old.exists() and not (d / "pirate_v1.png").exists():
        old.rename(d / "pirate_v1.png")
    body = {
        "description": "standing on the wooden deck of a gothic pirate airship at dusk, a big ship's wheel in front, brass "
                       "lanterns glowing, black and crimson sails with a skull banner, ropes and rigging, a huge balloon "
                       f"overhead, clouds and a dark castle far below, background scenery only, no people, {gen.STYLE}",
        "image_size": {"width": 140, "height": 200},
        "no_background": False,
        "outline": "single color black outline",
        "shading": "medium shading",
        "detail": "highly detailed",
        "view": "side",
        "negative_description": "people, person, character, figure, woman, cage, text, watermark",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge("portrait bg pirate v2", r.get("usage"))
    gen.save_b64(r["image"], d / "pirate.png")
    print("saved background", flush=True)


def guide2():
    """Take 2: keep her raised hand that gripped the staff; the staff becomes a flintlock held upright,
    and that hand a brass clockwork gauntlet."""
    im = Image.open(D / "pirate_b.png").convert("RGBA")
    px = im.load()
    bg = px[0, 0]

    def skin(p):
        return p[0] > 170 and p[1] > 120 and p[2] > 90 and p[0] > p[2] + 25

    # Erase the staff except within her grip (rows 56-70); keep the sleeve and lower cuff.
    hand_rows = range(55, 71)
    for y in range(im.height):
        for x in range(20, 46):
            p = px[x, y]
            if all(abs(p[i] - bg[i]) < 30 for i in range(3)):
                px[x, y] = bg
                continue
            keep = (y in hand_rows and x >= 34) or (min(p[:3]) > 175 and 70 <= y <= 110) or (x >= 44 and 36 <= y <= 110) or (skin(p) and 86 <= y <= 104)
            if not keep:
                px[x, y] = bg

    def put(x, y, c, r=0):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                X, Y = int(round(x)) + dx, int(round(y)) + dy
                if 0 <= X < im.width and 0 <= Y < im.height:
                    px[X, Y] = c

    # The gauntlet: her gripping hand turned to brass, rivets and a knuckle gear.
    for y in hand_rows:
        for x in range(33, 46):
            if skin(px[x, y]):
                px[x, y] = BRASS if (x + y) % 3 else BRASS_HI
    put(40, 66, BRASS_DK)
    put(37, 60, BRASS_DK)
    # The flintlock, held upright: barrel up from the grip, wooden stock below the hand.
    hx, hy = 39, 58
    for s in range(20):
        put(hx - s * 0.12, hy - s, (66, 58, 54, 255) if s % 6 else BRASS_DK, 1)
    put(hx - 2.4, hy - 20, BRASS_HI, 1)
    put(hx + 1, hy + 2, BRASS_HI, 1)
    for s in range(7):
        put(hx + 1 + s * 0.4, hy + 6 + s, (112, 62, 30, 255), 1)
    im.save(D / "pguide2.png")
    print("saved pguide2", flush=True)


def redraw2():
    desc = DESC.replace("a brass clockwork mechanical forearm with a gear at the elbow holding an ornate brass flintlock pistol",
                        "one raised brass clockwork mechanical hand holding an ornate brass flintlock pistol pointed upward")
    for strength in (480, 560, 640):
        out = D / f"pp2_s{strength}.png"
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
            "init_image": pixellab.b64img(D / "pguide2.png"),
            "init_image_strength": strength,
            "negative_description": "staff, spear, red hair, bent legs, crouching, extra hands, extra arms, floating objects, text, watermark, nudity, chibi, big head",
        }
        r = gen.call("POST", "/create-image-bitforge", body)
        gen.log_charge(f"pirate portrait take2 {strength}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", strength, flush=True)
    ps = [D / "pguide2.png"] + [D / f"pp2_s{s}.png" for s in (480, 560, 640)]
    gen.review(gen.GEN / "pirate_portrait_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"guide": guide, "redraw": redraw, "bg": bg, "guide2": guide2, "redraw2": redraw2}[sys.argv[1]]()
