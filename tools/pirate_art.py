"""The Inventor redesigned as a steampunk sky pirate (the user, 2026-10-06: "a pirate theme and look...
still keep it steampunk"). Same class and skills; new look. The old art is kept in generated/_old/inventor_v1.

    python tools/pirate_art.py portrait   3 full-body portraits (standing straight) + an airship-deck background
    python tools/pirate_art.py sprite     8-direction in-game character
    python tools/pirate_art.py anims      walk / fire the pistol / throw a bomb
    python tools/pirate_art.py review     contact sheet: generated/pirate_review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

NAME = "inventor"
HEADS = "small head, realistic adult body proportions, long legs"
# From the user's reference sheet (2026-10-06): a gothic pirate queen, kept steampunk.
FIGURE = (
    "full body gothic steampunk pirate captain woman standing straight, black tricorn hat with gold trim, skulls and red "
    "feathers, long wavy ash-blonde hair with braids, dark lips, black leather corset with buckles over a white ruffled "
    "blouse, tattered black and crimson layered coat, a brass clockwork mechanical arm holding an ornate brass flintlock "
    "pistol, a cutlass, brass lanterns and gears hanging on chains from her belt, thigh-high laced black boots with skulls, "
    "head to boots visible"
)
SPRITE = (
    "gothic steampunk pirate captain woman, black tricorn hat with red feathers, long wavy ash-blonde hair, black leather "
    "corset over a white ruffled blouse, tattered black and crimson coat, brass mechanical arm holding a brass flintlock "
    "pistol, cutlass, thigh-high black boots"
)
ANIMS = [
    (NAME, "walking confidently forward, tattered coat swaying", 6),
    (NAME, "aiming the brass flintlock pistol forward and firing", 6),
    (NAME, "throwing a small brass bomb forward with the mechanical arm", 6),
]


def portrait():
    d = gen.d_of(NAME)
    for tag in "abc":
        out = d / f"pirate_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": f"{FIGURE}, plain flat grey background, bold clean outlines, cel shading",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "bust, close-up, cropped, bent legs, crouching, multiple people, chibi, big head, nudity, "
                                    "text, watermark, scenery, extra limbs, extra arms, deformed hands",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"pirate full {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "pirate.png"
    if not bg.exists():
        body = {
            "description": "the deck of a gothic steampunk pirate airship at dusk above the clouds, a ship's wheel, brass lanterns, "
                           "black and crimson sails with a skull banner, ropes and rigging, brass propellers and pipes venting "
                           f"steam, a dark castle in the distance, background scenery only, no people, {gen.STYLE}",
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
            gen.log_charge("portrait bg pirate", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


def sprite():
    if not (gen.GEN / NAME / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, NAME, f"{SPRITE}, {HEADS}", 48, "realistic_female", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("pirate anims done", flush=True)


def review():
    d = gen.GEN / NAME
    ps = [d / f"pirate_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "pirate.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "pirate_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "anims": anims, "review": review}[sys.argv[1]]()
