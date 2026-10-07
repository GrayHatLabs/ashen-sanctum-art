"""Title screen and handheld art via OpenAI gpt-image-1: the painted title background and the ASHEN SANCTUM logo.
Raw images go to generated/oai/title/raw/<part>_<n>.png; the chosen ones are pixelized for the game and the
PortMaster cover (tools/title_pack.py).

    python tools/oai_title.py gen <bg|logo> [count]
    python tools/oai_title.py review
"""
import json
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oai_hud import generate  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "generated" / "oai" / "title" / "raw"

PARTS = {
    "bg": ("1536x1024", False,
           "A dark gothic fantasy landscape painting for a video game title screen, in the style of Diablo II: a vast ruined "
           "black cathedral, the Ashen Sanctum, on a cliff above a valley of ash and embers, its broken spires reaching into a "
           "burning red and violet sky, ash falling like snow, a faint golden light in its great doorway, a winding road "
           "leading up to it, silhouettes of dead trees. Detailed hand-painted pixel art look, rich but dark, strong contrast. "
           "Leave the upper third of the sky fairly clear for a title logo. No text, no letters, no people."),
    "logo": ("1536x1024", True,
             "A video game title logo that reads exactly \"ASHEN SANCTUM\" in two words on one line, heavy gothic blackletter-inspired "
             "capital letters forged from tarnished dark gold and blackened iron, glowing embers in the cracks, a few curls "
             "of smoke and falling ash, a small thorned crown ornament above the middle. Crisp, readable, centred, "
             "Diablo II style. Transparent background, nothing else in the image."),
}


def gen(part, count=2):
    OUT.mkdir(parents=True, exist_ok=True)
    size, transparent, prompt = PARTS[part]
    for _ in range(count):
        n = len(list(OUT.glob(f"{part}_*.png")))
        png, usage = generate(prompt, size) if transparent else generate_opaque(prompt, size)
        (OUT / f"{part}_{n}.png").write_bytes(png)
        with (OUT.parent / "usage.log").open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {part}_{n} {json.dumps(usage)}\n")
        print("saved", part, n, flush=True)


def generate_opaque(prompt, size):
    import base64
    import urllib.request
    from oai_portraits import api_key
    body = json.dumps({"model": "gpt-image-1", "prompt": prompt, "size": size, "quality": "high", "output_format": "png", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.loads(r.read())
    return base64.b64decode(data["data"][0]["b64_json"]), data.get("usage")


def review():
    ims = sorted(OUT.glob("*.png"))
    tiles = []
    for p in ims:
        im = Image.open(p).convert("RGBA")
        im.thumbnail((480, 320))
        bg = Image.new("RGBA", (490, 340), (70, 70, 76, 255))
        bg.alpha_composite(im, ((490 - im.width) // 2, 5))
        tiles.append((bg, p.stem))
    cols = 2
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 490, rows * 340), (30, 30, 34, 255))
    d = ImageDraw.Draw(sheet)
    for i, (t, name) in enumerate(tiles):
        x, y = (i % cols) * 490, (i // cols) * 340
        sheet.alpha_composite(t, (x, y))
        d.text((x + 6, y + 326), name, fill=(255, 255, 255, 255))
    sheet.save(OUT.parent / "review.png")
    print("review", OUT.parent / "review.png")


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    else:
        review()
