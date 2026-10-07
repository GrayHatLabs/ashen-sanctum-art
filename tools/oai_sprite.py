"""An experiment (the user, 2026-10-06): an in-game sprite designed by OpenAI's image model. One turnaround
sheet with the character in 8 directions is generated, then sliced and converted into small pixel-art
rotation images like PixelLab's (for review; animating them is a later step).

    python tools/oai_sprite.py gen <hero>      generated/oai/sprite_<hero>_raw_<n>.png + _dirs_<n>.png preview
    python tools/oai_sprite.py slice <hero>    re-slice the raw sheets (free)

Direction order on the sheet: south, south-east, east, north-east, north, north-west, west, south-west.
"""
import sys
import time
import json
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_portraits as op  # noqa: E402

OUT = op.OUT
DIRS = ["south", "south-east", "east", "north-east", "north", "north-west", "west", "south-west"]
SPRITE_H = 60

DESIGNS = {
    "inquisitor": "a tall, slender gothic inquisitor woman in a long flowing black hooded robe; pale face, ash-blonde hair under "
                  "the hood; behind her head a golden halo of long sharp spikes with a golden band arching through them; golden "
                  "chains wrapped across her body and waist; a spiked golden censer hanging on a chain from her right hand, "
                  "glowing with white-gold holy fire",
}

PROMPT = (
    "A character turnaround sprite sheet for an isometric dark fantasy action RPG in the style of Diablo 2, as detailed pixel "
    "art with crisp pixels, a limited muted palette and dark outlines. The SAME character drawn 8 times in one horizontal row, "
    "evenly spaced and the same size, each standing in a neutral idle pose, seen from a high isometric three-quarter camera, "
    "facing in this order from left to right: toward the viewer, toward the viewer and to the right, to the right (profile), "
    "away and to the right, away from the viewer (back), away and to the left, to the left (profile), toward the viewer and to "
    "the left. Identical outfit, colours and proportions in every view. Small realistic head, adult proportions. Transparent "
    "background, no text, no labels, no ground, no shadows.\n\nThe character: {design}"
)


def slice_sheet(raw: Image.Image):
    """Splits a row of figures into 8 by the empty columns between them."""
    im = raw.convert("RGBA")
    a = im.getchannel("A")
    w, h = im.size
    cols = [any(a.getpixel((x, y)) > 40 for y in range(0, h, 2)) for x in range(w)]
    spans, start = [], None
    for x, c in enumerate(cols + [False]):
        if c and start is None:
            start = x
        elif not c and start is not None:
            if x - start > 12:
                spans.append((start, x))
            start = None
    # Merge slivers (a censer or chain separated from its body) into the nearest figure.
    while len(spans) > 8:
        gaps = [spans[i + 1][0] - spans[i][1] for i in range(len(spans) - 1)]
        i = gaps.index(min(gaps))
        spans[i:i + 2] = [(spans[i][0], spans[i + 1][1])]
    figs = []
    for x0, x1 in spans:
        f = im.crop((x0, 0, x1, h))
        f = f.crop(f.getbbox())
        figs.append(f)
    return figs


def pixel_sprite(fig: Image.Image) -> Image.Image:
    k = SPRITE_H / fig.height
    small = fig.resize((max(1, round(fig.width * k)), SPRITE_H), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=32, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    # Canvas like PixelLab's rotations: 80x80, feet near the bottom middle.
    canvas = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    canvas.alpha_composite(out, ((80 - out.width) // 2, 76 - out.height))
    return canvas


def preview(hero, n, sprites):
    sheet = Image.new("RGBA", (84 * len(sprites), 84), (40, 36, 44, 255))
    for i, s in enumerate(sprites):
        sheet.alpha_composite(s, (i * 84 + 2, 2))
    sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(OUT / f"sprite_{hero}_dirs_{n}.png")


def do_slice(hero, n):
    raw = Image.open(OUT / f"sprite_{hero}_raw_{n}.png")
    figs = slice_sheet(raw)
    print(hero, n, "figures found:", len(figs))
    sprites = [pixel_sprite(f) for f in figs]
    d = OUT / f"sprite_{hero}_{n}"
    d.mkdir(parents=True, exist_ok=True)
    for name, s in zip(DIRS, sprites):
        s.save(d / f"rotation_urls_{name}.png")
    preview(hero, n, sprites)


def gen(hero, count=1):
    OUT.mkdir(parents=True, exist_ok=True)
    n0 = len(list(OUT.glob(f"sprite_{hero}_raw_*.png")))
    for n in range(n0, n0 + count):
        import base64
        body = json.dumps({"model": "gpt-image-1", "prompt": PROMPT.format(design=DESIGNS[hero]), "size": "1536x1024",
                           "quality": "high", "background": "transparent", "output_format": "png", "n": 1}).encode()
        import urllib.request
        req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                     headers={"Authorization": f"Bearer {op.api_key()}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read())
        (OUT / f"sprite_{hero}_raw_{n}.png").write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
        with (OUT / "usage.log").open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} sprite_{hero}_{n} {json.dumps(data.get('usage'))}\n")
        do_slice(hero, n)


if __name__ == "__main__":
    cmd, hero = sys.argv[1], sys.argv[2]
    if cmd == "gen":
        gen(hero, int(sys.argv[3]) if len(sys.argv) > 3 else 1)
    else:
        for p in sorted(OUT.glob(f"sprite_{hero}_raw_*.png")):
            do_slice(hero, int(p.stem.rsplit("_", 1)[1]))
