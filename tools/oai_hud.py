"""The bottom HUD's art via OpenAI gpt-image-1: the life and mana globe housings and the carved panel between them.
The raw images go to generated/oai/hud/raw/<part>_<n>.png; tools/hud_pack.py turns the chosen ones into game art.

    python tools/oai_hud.py gen <part> [count]    part: left | right | panel
    python tools/oai_hud.py review                 contact sheet: generated/oai/hud/review.png
"""
import base64
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from oai_portraits import api_key  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "generated" / "oai" / "hud"
RAW = OUT / "raw"

STYLE = ("Dark gothic fantasy game UI art in the style of Diablo II's bottom control panel: weathered dark stone, blackened iron "
         "and tarnished dark gold filigree, ash and embers. Detailed hand-painted pixel art look, crisp edges, strong contrast, "
         "lit from the top left. Transparent background. No text, no letters, no numbers, no icons, no characters other than the statue.")

PARTS = {
    "left": ("1024x1024",
             "A single ornate circular globe housing for a life orb, front view: a thick round frame of carved dark stone with a "
             "tarnished gold rim and iron claws, cradled from the left side and below by a small weathered stone angel statue with "
             "folded wings and a bowed head. The inside of the round frame is a completely empty hole (transparent), a perfect circle "
             "taking up about half the image width, centred slightly right of the image centre. "),
    "right": ("1024x1024",
              "A single ornate circular globe housing for a mana orb, front view: a thick round frame of carved dark stone with a "
              "tarnished gold rim and iron claws, cradled from the right side and below by a small crouching stone gargoyle demon "
              "statue with horns and bat wings. The inside of the round frame is a completely empty hole (transparent), a perfect "
              "circle taking up about half the image width, centred slightly left of the image centre. "),
    "panel": ("1536x1024",
              "A long, low, horizontal control-panel bar seen straight on, filling the whole image width edge to edge and about a "
              "quarter of the image height, centred vertically: dark carved stone slabs bound with blackened iron straps and rivets, "
              "a tarnished gold trim line along the top edge with small skull and thorn ornaments, a few shallow recessed rectangular "
              "sockets. Flat and symmetrical, nothing above or below the bar. "),
}


def generate(prompt, size):
    body = json.dumps({"model": "gpt-image-1", "prompt": prompt, "size": size, "quality": "high", "background": "transparent",
                       "output_format": "png", "n": 1}).encode()
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body, method="POST",
                                 headers={"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            return base64.b64decode(data["data"][0]["b64_json"]), data.get("usage")
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(20 * (attempt + 1))
                continue
            sys.exit(f"HTTP {e.code}: {msg}")
    sys.exit("gave up")


def gen(part, count=2):
    RAW.mkdir(parents=True, exist_ok=True)
    size, desc = PARTS[part]
    for _ in range(count):
        n = len(list(RAW.glob(f"{part}_*.png")))
        png, usage = generate(desc + STYLE, size)
        (RAW / f"{part}_{n}.png").write_bytes(png)
        with (OUT / "usage.log").open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {part}_{n} {json.dumps(usage)}\n")
        print("saved", part, n, flush=True)


def review():
    ims = sorted(RAW.glob("*.png"))
    tiles = []
    for p in ims:
        im = Image.open(p).convert("RGBA")
        im.thumbnail((360, 360))
        bg = Image.new("RGBA", (370, 380), (60, 60, 64, 255))
        bg.alpha_composite(im, ((370 - im.width) // 2, 5))
        tiles.append((bg, p.stem))
    cols = 3
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 370, rows * 380), (30, 30, 34, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, (t, name) in enumerate(tiles):
        x, y = (i % cols) * 370, (i // cols) * 380
        sheet.alpha_composite(t, (x, y))
        d.text((x + 6, y + 364), name, fill=(255, 255, 255, 255))
    sheet.save(OUT / "review.png")
    print("review", OUT / "review.png")


if __name__ == "__main__":
    if sys.argv[1] == "gen":
        gen(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    else:
        review()
