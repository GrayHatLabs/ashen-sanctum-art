"""The kraken's arm in the Bone Reef (Act 5, 2026-10-08): one OpenAI image, shrunk to pixel art and installed as the
prop generated/kraken_arm/image.png. PixelLab drew a whole octopus twice (kept in _old/kraken_arm_take1, take2).

    python tools/kraken_oai.py gen       new image -> generated/oai/kraken_arm_raw_<n>.png
    python tools/kraken_oai.py use <n>   pixelate image n into generated/kraken_arm/image.png
"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

PROMPT = (
    "A single game sprite for an isometric dark fantasy action RPG in the style of Diablo 2, detailed pixel art with crisp "
    "pixels, a limited muted palette and dark outlines. One giant kraken tentacle bursting up out of a small mound of broken "
    "coral and sand: a single long thick tentacle, no head, no eyes, no body, rising tall and curling over at the top like a "
    "hook, dark murky blue-green and purple-grey skin, rows of round pale suckers on its inner side, barnacles and strands "
    "of seaweed on it, wet highlights. Seen from a high isometric three-quarter camera. Transparent background, no text, "
    "no shadow beyond the mound."
)
W, H = 64, 104


def gen_one():
    os_.OUT.mkdir(parents=True, exist_ok=True)
    n = len(list(os_.OUT.glob("kraken_arm_raw_*.png")))
    body = json.dumps({"model": "gpt-image-1", "prompt": PROMPT, "size": "1024x1536", "quality": "high",
                       "background": "transparent", "output_format": "png", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {os_.op.api_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    (os_.OUT / f"kraken_arm_raw_{n}.png").write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    with (os_.OUT / "usage.log").open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} kraken_arm_{n} {json.dumps(data.get('usage'))}\n")
    print("made", n)


def use(n):
    im = Image.open(os_.OUT / f"kraken_arm_raw_{n}.png").convert("RGBA")
    im = im.crop(im.getbbox())
    k = min(W / im.width, H / im.height)
    small = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    d = gen.d_of("kraken_arm")
    d.mkdir(parents=True, exist_ok=True)
    out.save(d / "image.png")
    print("installed", n, out.size)


if __name__ == "__main__":
    gen_one() if sys.argv[1] == "gen" else use(int(sys.argv[2]))
