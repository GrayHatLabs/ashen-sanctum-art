"""Concept art for the Reaper class (sixth playable class: rune scythe, spirit lantern, the Ledger).

    python tools/reaper_art.py portrait   3 class-select portrait variants (figure on flat grey, keyed later) + background
    python tools/reaper_art.py sprite     8-direction in-game character
    python tools/reaper_art.py anims      walk / sweep / cast / spin
    python tools/reaper_art.py extras     a scholar spirit
    python tools/reaper_art.py review     contact sheet: generated/reaper_review.png

From the user's concept (docs/concepts/RUNE_LIBRARY_REAPER.md): black, charcoal, aged bronze, parchment brown,
muted amber and spectral blue rune magic; mysterious and elegant rather than grotesque.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
PALETTE = "black, charcoal, aged bronze, parchment brown, muted amber and spectral blue palette, elegant not grotesque"
LOOK = (
    "mysterious gothic rune library reaper woman, calm cold intelligent expression with a subtle knowing smile, extremely "
    "long silver-grey hair to the floor with thin braids of black thread, antique keys and bone beads, ghostly pale skin, "
    "glowing muted amber eyes, charcoal smoky eyeshadow, black-plum lips, thin black rune markings under one eye and down "
    "her neck, deep black hood and an enormous weathered black reaper cloak whose edges dissolve into black smoke, fitted "
    "black leather corset with aged bronze clasps, high-slit layered black mourning skirt, tall leather boots, belts of "
    "old keys, scroll tubes, hourglasses and chained books"
)
SCYTHE = "an enormous rune scythe with a black wood shaft and a curved nearly black blade engraved with glowing blue-white runes, a small iron lantern with a pale blue spirit flame hanging under the blade"
# v2 (the user): no hood, her long silver-grey hair instead, and glowing blue runes on her outfit.
# (v1, hooded, is in reference/reaper_sprite_v1.)
SPRITE = (
    "gothic reaper woman with very long flowing silver-grey hair, no hood, pale face, black gown and long black cloak "
    "decorated with bright glowing cyan blue rune symbols down the front, on the sleeves and along the hem, holding a huge "
    "black scythe with glowing blue runes"
)

ANIMS = [
    # (The first walk, "gliding forward ... scythe held upright", swung the scythe overhead in every direction.)
    ("reaper", "walking calmly forward with steady steps, holding the scythe still and upright at her side, no swinging", 6),
    ("reaper", "sweeping the great scythe in a wide horizontal arc", 6),
    ("reaper", "raising one hand to cast spectral blue rune magic, scythe in the other hand", 6),
    ("reaper", "spinning in a full circle with the scythe held out", 6),
]

EXTRAS = [
    ("scholar_spirit", f"a translucent pale blue ghost of an old scholar in long robes holding a book, {HEADS}", 48, "heroic", ""),
]
EXTRA_ANIMS = [
    ("scholar_spirit", "ghost scholar floating forward, robes drifting", 6),
    ("scholar_spirit", "ghost scholar raising the book and casting a spell", 6),
]


def portrait():
    for tag in "abc":
        out = gen.d_of("reaper") / f"portrait_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": (
                f"cartoon character design portrait of one {LOOK}, standing silently in a three-quarter pose holding {SCYTHE}, "
                "a chained black grimoire with a bronze lock floating beside her, a black raven with amber eyes on the scythe, "
                f"{PALETTE}, plain flat grey background, bold clean outlines, cel shading, anatomically correct, exactly two "
                "arms, exactly two legs, five fingers"
            ),
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "red, gore, skeleton face, text, watermark, multiple people, chibi, big head, nudity, "
                                    "exposed chest, extra limbs, extra arms, extra legs, duplicated limbs, deformed hands, scenery",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"reaper portrait {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved portrait", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "reaper.png"
    if not bg.exists():
        body = {
            "description": "an impossibly vast ancient forbidden gothic library, towering bookshelves vanishing into darkness, "
                           "iron bridges and spiral staircases, thousands of candles, floating chained books, and at the far end "
                           "a huge black stone door covered in locks, chains and glowing blue runes, background scenery only, "
                           f"no people, portrait orientation, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "people, person, character, figure, woman, text, watermark",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if r:
            gen.log_charge("portrait bg reaper", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


def sprite():
    if not (gen.GEN / "reaper" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "reaper", f"{SPRITE}, {HEADS}", 56, "realistic_female", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("reaper anims done", flush=True)


def extras():
    import world_art
    for name, desc, size, prop, tmpl in EXTRAS:
        if not (gen.GEN / name / "rotation_urls_south.png").exists():
            act2_art.safe(gen.character, name, desc, size, prop, tmpl)
    for name, action, frames in EXTRA_ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("reaper extras done", flush=True)


def review():
    d = gen.GEN / "reaper"
    ps = [d / f"portrait_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "reaper.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "reaper_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "anims": anims, "extras": extras, "review": review,
     "all": lambda: (portrait(), sprite(), anims(), extras())}[sys.argv[1]]()
