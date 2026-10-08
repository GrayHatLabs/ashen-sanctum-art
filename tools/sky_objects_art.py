"""Act 6's non-humanoid fliers, made like the clockwork crow (tools/crow_art.py): one bitforge image each
(the character generator keeps giving them legs), mirrored for the left-facing directions and written as
8 rotation files with no animations. The game bobs and flashes them in code.

    python tools/sky_objects_art.py
The previous character-generator takes are kept in generated/_old/act6_chars_take1 and take2.
"""
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

# name -> (description, bitforge canvas, width in game, view)
OBJECTS = {
    "ophanim": ("a floating holy wheel made of three interlocking golden rings tilted at different angles like a gyroscope, "
                "many open eyes set along the rings, a glowing white core at the centre, an abstract floating object, no body, no legs",
                64, 34, "side"),
    "boss_ophan": ("a colossal floating holy wheel of many interlocking golden rings turning at different angles like a gyroscope, "
                   "hundreds of open eyes along the rings, a blazing white core, rays of light, an abstract floating object, no body, no legs",
                   128, 92, "side"),
    "thunderbird": ("a giant storm eagle in flight seen from the side facing right, huge dark blue feathered wings raised, white "
                    "lightning crackling between the feathers, hooked yellow beak, glowing white eye, clearly a bird",
                    96, 58, "side"),
}


def make(name, desc, canvas, width, view, old_dir="act6_chars_take2"):
    d = gen.d_of(name)
    if d.exists() and not (d / "image.png").exists():
        # A character-generator take sits here: keep it.
        old = gen.GEN / "_old" / old_dir / name
        old.parent.mkdir(parents=True, exist_ok=True)
        if not old.exists():
            shutil.move(str(d), str(old))
    d.mkdir(parents=True, exist_ok=True)
    src = d / "image.png"
    if not src.exists():
        body = {
            "description": f"{desc}, single object, no background, {gen.STYLE}",
            "image_size": {"width": canvas, "height": canvas},
            "no_background": True,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "highly detailed",
            "view": view,
            "negative_description": "person, human, legs, arms, text, background, floor, ground, multiple objects",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        gen.log_charge(name, r.get("usage"))
        gen.save_b64(r["image"], src)
    im = Image.open(src).convert("RGBA")
    im = im.crop(im.getbbox())
    k = width / im.width
    im = im.resize((width, max(1, round(im.height * k))), Image.LANCZOS)
    im.putalpha(im.getchannel("A").point(lambda v: 255 if v > 110 else 0))
    right, left = im, ImageOps.mirror(im)
    for k in ["east", "south-east", "north-east", "south"]:
        right.save(d / f"rotation_urls_{k}.png")
    for k in ["west", "south-west", "north-west", "north"]:
        left.save(d / f"rotation_urls_{k}.png")
    (d / "character.json").write_text(json.dumps({"animations": []}))
    print("made", name, im.size, flush=True)


# Act 5's anglerlurk, the same way (the character generator stood it up on legs twice; 2026-10-07).
LURKER = ("anglerlurk", "a deep-sea anglerfish monster seen from the side facing right, a round dark blue-black fish body low on "
          "the sand, pulling itself along on two stubby fins, an enormous open jaw of long glassy needle teeth, a glowing cyan "
          "lure dangling on a stalk in front of its face, clearly a fish", 80, 46, "side")


# Act 4's Junk Golem (user's choice, 2026-10-08): the character generator made a sleek robot twice
# (kept in _old/junkgolem_take1 and generated/boss_junkgolem2).
GOLEM = ("boss_junkgolem", "a hulking golem built from a heap of rusty scrap metal seen from the side facing right: a dented old "
         "boiler for a chest glowing orange through cracks, bent pipes and chains for arms, two huge mismatched iron fists, "
         "cog wheels and broken gears stuck all over its shoulders and back, rivets and rust, crooked and lopsided, standing "
         "hunched on two stumpy legs made of piled scrap", 128, 92, "side")


if __name__ == "__main__":
    if sys.argv[1:] == ["junkgolem"]:
        make(*GOLEM, old_dir="junkgolem_take1")
        sys.exit()
    if sys.argv[1:] == ["anglerlurk"]:
        make(*LURKER, old_dir="act5_chars_take2")
        sys.exit()
    for name, (desc, canvas, width, view) in OBJECTS.items():
        if sys.argv[1:] and name not in sys.argv[1:]:
            continue
        make(name, desc, canvas, width, view)
