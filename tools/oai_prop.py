"""Map objects drawn by OpenAI and shrunk to pixel art (like tools/kraken_oai.py), for props PixelLab drew badly.
Any PixelLab version already installed is kept in generated/_old/<name>_pixellab.

    python tools/oai_prop.py gen <name>       new image -> generated/oai/<name>_raw_<n>.png
    python tools/oai_prop.py use <name> <n>   pixelate image n into generated/<name>/image.png
"""
import base64
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

STYLE = (
    "A single game sprite for an isometric dark fantasy action RPG in the style of Diablo 2, detailed pixel art with "
    "crisp pixels, a limited muted, slightly gritty palette, weathered and worn, dark outlines. Seen from a high "
    "isometric three-quarter camera. Transparent background, no text, one object only, no ground beyond its base.\n\n"
)
# name -> (description, max width, max height, OpenAI canvas)
PROPS = {
    "ent_vault": ("The way into the Probability Vault: a squat round stone vault door set into a mound of floating rock, the "
                  "huge circular door carved like a roulette wheel with numbered segments, two giant stone dice flanking it, "
                  "violet light leaking around the door's rim.", 96, 92, "1024x1024"),
    "shrine_chaos": ("The Chaos Roulette shrine, well lit: a waist-high pillar of pale grey weathered stone topped by a "
                     "big wheel of fortune with six vivid, brightly painted segments (bright red, bright blue, bright green, "
                     "bright gold, white and violet), each with a black rune, a crooked iron pointer above it, a few violet "
                     "sparks around it. Clear, high-contrast colours.", 40, 58, "1024x1024"),
    "stillpoint": ("The Stillpoint: a small perfect sphere of pale silver-blue light held motionless inside a delicate brass "
                   "clockwork cage of concentric rings, resting on a short fluted bronze pedestal with gear engravings; the "
                   "air around it is utterly calm, faint frozen dust motes hang in place around the sphere.", 40, 56, "1024x1024"),
    "ent_eye": ("The way into the Eye of the Churn: a huge round vortex opening in the ground ringed by broken stone and "
                "floating debris, swirling violet and gold light spiralling down into darkness at its centre, shards of "
                "rock hanging in the air around it.", 104, 96, "1024x1024"),
    "ent_cathedral": ("The entrance to a half-built gothic cathedral that is building and unbuilding itself: dark grey stone "
                      "walls and a pointed arch doorway, but the upper half is floating loose blocks, broken scaffolding "
                      "and bricks hanging in the air, faint violet light in the dark doorway, rubble at its base.", 104, 112, "1024x1024"),
    "ent_warren": ("A big muddy burrow mouth in a mound of wet dark earth and violet slime, ringed with huge toad bones, "
                   "crude totems and bubbling pools, a dark tunnel going down, dripping roots.", 104, 96, "1024x1024"),
    "ent_mirrors": ("The ruined gate of a monastery hall: two cracked stone pillars and a broken arch, tall shards of mirror "
                    "glass standing in the rubble reflecting violet light, a dark doorway between them.", 104, 112, "1024x1024"),
    "shrine_sky": ("A small ancient sky shrine: a weathered, cracked white marble pedestal with a pair of carved stone angel "
                   "wings folded on its sides, a small floating sun-disc of tarnished gold glowing softly above it, a few "
                   "fallen feathers and moss at its base.", 40, 56, "1024x1536"),
    "ent_observatory": ("The entrance to a ruined observatory: a crumbling round tower of weathered grey-white stone on a "
                        "broken rock, its domed roof cracked and half fallen in, an old tarnished brass telescope jutting "
                        "from the gap, faint golden constellation lines glowing on the stone, a dark arched doorway at "
                        "the bottom, moss and rubble.", 104, 112, "1024x1024"),
}


def gen_one(name):
    desc, _, _, size = PROPS[name]
    os_.OUT.mkdir(parents=True, exist_ok=True)
    n = len(list(os_.OUT.glob(f"{name}_raw_*.png")))
    body = json.dumps({"model": "gpt-image-1", "prompt": STYLE + desc, "size": size, "quality": "high",
                       "background": "transparent", "output_format": "png", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {os_.op.api_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    (os_.OUT / f"{name}_raw_{n}.png").write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    with (os_.OUT / "usage.log").open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {name}_{n} {json.dumps(data.get('usage'))}\n")
    print("made", name, n)


def use(name, n):
    _, W, H, _ = PROPS[name]
    im = Image.open(os_.OUT / f"{name}_raw_{n}.png").convert("RGBA")
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 60 else 0).getbbox())
    k = min(W / im.width, H / im.height)
    small = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    d = gen.d_of(name)
    old = gen.GEN / "_old" / f"{name}_pixellab"
    if (d / "image.png").exists() and not old.exists():
        old.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(d, old)
    d.mkdir(parents=True, exist_ok=True)
    out.save(d / "image.png")
    print("installed", name, n, out.size)


if __name__ == "__main__":
    gen_one(sys.argv[2]) if sys.argv[1] == "gen" else use(sys.argv[2], int(sys.argv[3]))
