"""Concept art for the Inventor class (third playable class, steampunk).

    python tools/inventor_art.py portrait   class-select portrait (bitforge, 140x200, with background)
    python tools/inventor_art.py sprite     8-direction in-game character (1 generation)
    python tools/inventor_art.py anims      walk / shoot / gadget animations
    python tools/inventor_art.py review     contact sheet: generated/inventor_review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
SPRITE = (
    "steampunk woman inventor wearing a long floor-length black and oxblood Victorian bustle dress that covers her legs, "
    "with a brown leather corset over it, long dark auburn curly hair, a small tilted black top hat with brass goggles, "
    "one mechanical brass clockwork arm holding an ornate brass ray pistol, no trousers"
)

ANIMS = [
    ("inventor", "walking confidently forward, skirt swaying", 6),
    ("inventor", "aiming the brass ray pistol forward and firing", 6),
    ("inventor", "throwing a small brass bomb forward with the mechanical arm", 6),
]


def portrait():
    body = {
        "description": (
            "cartoon illustration of a glamorous steampunk goth woman inventor, hand on hip, clever smirk, "
            "long dark auburn hair in loose curls, pale skin, amber eyes, small tilted black top hat with brass goggles "
            "with teal lenses, black lace choker with a brass gear pendant, fully clothed in a brown leather overbust "
            "corset with brass buckles over a black ruffled blouse, long black and oxblood bustle skirt, black lace-up "
            "boots, one mechanical clockwork brass arm holding an ornate brass ray pistol, pocket watch chain, "
            "foggy Victorian city background with airships, copper pipes and steam, warm brass and teal palette, "
            "bold outlines, cel shading"
        ),
        "image_size": {"width": 140, "height": 200},
        "no_background": False,
        "outline": "single color black outline",
        "shading": "flat shading",
        "detail": "highly detailed",
        "view": "side",
        "negative_description": "text, watermark, multiple characters, chibi, big head, nudity, exposed chest, plain grey background",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge("inventor portrait", r.get("usage"))
    gen.save_b64(r["image"], gen.d_of("inventor") / "portrait.png")
    print("saved portrait", flush=True)


def portrait_v2(tag):
    """A cleaner redo: simple clear pose, one character, the arm and pistol readable."""
    body = {
        "description": (
            "cartoon character design portrait of one glamorous steampunk woman inventor standing in a confident three-quarter pose, "
            "left hand on her hip, right arm is a brass clockwork mechanical arm with visible gears raised holding an ornate brass "
            "ray pistol pointed upward, clever smirk, long dark auburn hair in loose curls, small tilted black top hat with brass "
            "goggles with teal lenses, black lace choker with a brass gear, brown leather corset with brass buckles over a black "
            "ruffled blouse, long black and oxblood bustle skirt, black lace-up boots, foggy Victorian city with airships and "
            "copper pipes behind her, warm brass and teal palette, bold clean outlines, cel shading, "
            "anatomically correct, exactly two arms, exactly two legs, five fingers"
        ),
        "image_size": {"width": 140, "height": 200},
        "no_background": False,
        "outline": "single color black outline",
        "shading": "flat shading",
        "detail": "highly detailed",
        "view": "side",
        "negative_description": "text, watermark, multiple characters, chibi, big head, nudity, exposed chest, extra limbs, "
                                "extra legs, extra arms, duplicated limbs, deformed hands, plain grey background",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge(f"inventor portrait v2 {tag}", r.get("usage"))
    gen.save_b64(r["image"], gen.d_of("inventor") / f"portrait_v2_{tag}.png")
    print("saved portrait v2", tag, flush=True)


def sprite():
    gen.character("inventor", f"{SPRITE}, {HEADS}", 48, "realistic_female", "")


def anims():
    import act2_art
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("inventor anims done", flush=True)


def review():
    d = gen.GEN / "inventor"
    ps = [d / "portrait.png"] + [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "inventor_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "portrait2": lambda: [portrait_v2(t) for t in "abc"], "sprite": sprite, "anims": anims, "review": review}[sys.argv[1]]()
