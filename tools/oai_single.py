"""Non-humanoid monsters as one OpenAI image each (side view, facing right), shrunk to pixel art and mirrored
for the left-facing directions, written as 8 rotation files with no animations (the game bobs them), like
tools/sky_objects_art.py does with bitforge.

    python tools/oai_single.py gen <name>       new image -> generated/oai/<name>_raw_<n>.png
    python tools/oai_single.py use <name> <n>   install image n as generated/<name> (old take kept in _old)
"""
import base64
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

STYLE = (
    "A single creature sprite for an isometric dark fantasy action RPG in the style of Diablo 2, detailed pixel art "
    "with crisp pixels, a limited muted, gritty palette and dark outlines. Seen from the side and a little above, "
    "facing to the right. Transparent background, no text, no ground, no shadow, one creature only.\n\n"
)
# name -> (description, width in game pixels)
MONSTERS = {
    "boss_dicesaint": ("The Dice-Saint, a tall gaunt robed saint of chance: tattered violet and gold vestments embroidered with "
                       "dice pips, a halo made of six floating ivory dice, a face hidden behind a smooth white porcelain mask "
                       "with a single painted eye, long fingers holding a pair of huge bone dice, more dice on chains hanging "
                       "from the belt. Holy and sinister at once. A humanoid figure, standing.", 52),
    "vault_coffer": ("A heavy ornate treasure coffer from a gambler's vault: dark wood bound in tarnished brass, its lid "
                     "carved with dice pips, a big brass lock shaped like a die, a faint violet glow leaking from the seam "
                     "of the lid. Closed. Just the chest.", 30),
    "boss_ylgrath": ("Ylgrath the Unshaped, a towering being of raw chaos given a will: a storm of every element at once, "
                     "a churning column of violet and gold smoke with fire, ice shards, lightning and seawater swirling "
                     "through it, dozens of mismatched eyes and half-formed mouths opening and closing in the storm, "
                     "broken pieces of other monsters (a crown, a dragon's horn, gears, a tentacle, a halo) caught and "
                     "turning inside it. Huge, terrifying, not a person.", 120),
    "chaos_toad": ("A huge muscular toad-like brute standing on its hind legs, as tall as a man, warty grey-white "
                   "skin with no colour of its own (it will be tinted), a wide frog mouth full of jagged teeth, "
                   "long clawed arms, small cunning eyes, crude bone bracelets. A monster, not a cartoon frog.", 46),
    "chaos_blob": ("A heap of raw living chaos matter: a lumpy glistening blob of swirling violet and dirty gold "
                   "slime with half-formed eyes, teeth and fingers surfacing and sinking in it, dripping.", 36),
}


def gen_one(name):
    desc, _ = MONSTERS[name]
    os_.OUT.mkdir(parents=True, exist_ok=True)
    n = len(list(os_.OUT.glob(f"{name}_raw_*.png")))
    body = json.dumps({"model": "gpt-image-1", "prompt": STYLE + desc, "size": "1024x1024", "quality": "high",
                       "background": "transparent", "output_format": "png", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {os_.op.api_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    (os_.OUT / f"{name}_raw_{n}.png").write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    with (os_.OUT / "usage.log").open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {name}_{n} {json.dumps(data.get('usage'))}\n")
    print("made", name, n, flush=True)


def use(name, n):
    _, width = MONSTERS[name]
    im = Image.open(os_.OUT / f"{name}_raw_{n}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 80 else 0).getbbox())
    k = width / im.width
    small = im.resize((width, max(1, round(im.height * k))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    d = gen.d_of(name)
    if d.exists():
        old = gen.GEN / "_old" / f"{name}_take_before_{n}"
        old.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(d), str(old))
    d.mkdir(parents=True, exist_ok=True)
    right, left = out, ImageOps.mirror(out)
    for k in ["east", "south-east", "north-east", "south"]:
        right.save(d / f"rotation_urls_{k}.png")
    for k in ["west", "south-west", "north-west", "north"]:
        left.save(d / f"rotation_urls_{k}.png")
    (d / "character.json").write_text(json.dumps({"animations": []}))
    print("installed", name, n, out.size)


if __name__ == "__main__":
    gen_one(sys.argv[2]) if sys.argv[1] == "gen" else use(sys.argv[2], int(sys.argv[3]))
