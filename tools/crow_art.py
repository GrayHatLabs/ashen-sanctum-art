"""The clockwork crow (Act 4). Not humanoid, so it's a bitforge image (like the Ordinals): one
flying crow facing right, mirrored for the left-facing directions, written as 8 rotation files.

    python tools/crow_art.py
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

NAME = "clock_crow"
DESC = ("a black crow bird in flight seen from the side facing right, both wings raised, made of dark iron plates with small "
        "brass gears, a glowing orange eye and a pointed brass beak, clearly a bird")


def main():
    d = gen.d_of(NAME)
    src = d / "image.png"
    if not src.exists():
        body = {
            "description": f"{DESC}, single creature, no background, {gen.STYLE}",
            "image_size": {"width": 40, "height": 40},
            "no_background": True,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "medium detail",
            "view": "side",
            "negative_description": "person, human, text, background, multiple birds, floor",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        gen.log_charge("clock crow", r.get("usage"))
        gen.save_b64(r["image"], src)
    im = Image.open(src).convert("RGBA")
    # A crow is small: about two thirds of a tile across in game.
    im = im.crop(im.getbbox())
    k = 22 / im.width
    im = im.resize((22, max(1, round(im.height * k))), Image.LANCZOS)
    a = im.getchannel("A").point(lambda v: 255 if v > 110 else 0)
    im.putalpha(a)
    right, left = im, ImageOps.mirror(im)
    for k in ["east", "south-east", "north-east", "south"]:
        right.save(d / f"rotation_urls_{k}.png")
    for k in ["west", "south-west", "north-west", "north"]:
        left.save(d / f"rotation_urls_{k}.png")
    (d / "character.json").write_text(json.dumps({"animations": []}))
    print("crow done", flush=True)


if __name__ == "__main__":
    main()
