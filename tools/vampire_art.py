"""Concept art for the Vampire class (second playable class).

    python tools/vampire_art.py portrait   large class-select portrait (bitforge, with background)
    python tools/vampire_art.py sprite     8-direction in-game character (1 generation)
    python tools/vampire_art.py review     contact sheet: generated/vampire_review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402

LOOK = (
    "glamorous goth vampire woman in 1980s goth style, huge teased voluminous black hair falling past her waist "
    "with a purple streak, pale porcelain skin, glowing red eyes, purple smoky eyeshadow, dark red lips, "
    "off-shoulder floor-length plum velvet gown with a high leg slit and a fishnet stocking, studded black belt, "
    "black choker with a red gem, bat earrings, black vampire cape with a tall blood-red lined collar"
)
HEADS = "small head, realistic adult body proportions, long legs"


def portrait():
    body = {
        "description": (
            "cartoon illustration of a glamorous goth vampire woman standing in front of a moonlit gothic castle, "
            "hand on hip, sly smirk, huge teased black hair with a purple streak, pale skin, glowing red eyes, "
            "fully clothed in an off-shoulder floor-length plum purple velvet gown with a modest closed bodice, a leg slit and a fishnet stocking, studded belt, "
            "black cape with a tall blood-red collar, full moon in a deep purple and crimson night sky, rich purple and crimson palette, bold outlines, cel shading"
        ),
        "image_size": {"width": 140, "height": 200},
        "no_background": False,
        "outline": "single color black outline",
        "shading": "flat shading",
        "detail": "highly detailed",
        "view": "side",
        "negative_description": "text, watermark, multiple characters, chibi, big head, plain grey background, catsuit, bodysuit, nudity, exposed chest, blue grey palette",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge("vampire portrait", r.get("usage"))
    gen.save_b64(r["image"], gen.d_of("vampire") / "portrait.png")
    print("saved portrait", flush=True)


SPRITE = (
    "elegant goth vampire noblewoman wearing a long floor-length plum velvet gown that covers her legs, "
    "a black cape with a tall red-lined collar, very long voluminous black hair with a purple streak, pale skin, "
    "red eyes, black choker"
)


def sprite():
    gen.character("vampire", f"{SPRITE}, {HEADS}", 48, "realistic_female", "")


def review():
    d = gen.GEN / "vampire"
    ps = [d / "portrait.png"] + [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "vampire_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "review": review}[sys.argv[1]]()
