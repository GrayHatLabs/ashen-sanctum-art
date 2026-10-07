"""Class-select portraits from OpenAI's image model, turned into pixel art (the user, 2026-10-06: "keep it
pixel-level, in the correct format, just more detail. Redo all the portraits; keep all the old ones").

The old portraits are kept in reference/portraits_v1/. New ones land in generated/oai/:
    raw/<hero>_<n>.png      the model's 1024x1536 image (transparent background)
    <hero>_<n>.png          pixel art: PORTRAIT_W x PORTRAIT_H on flat grey, limited palette, 1 px dark outline

    python tools/oai_portraits.py gen <hero> [count]     generate (costs money on the user's OpenAI account)
    python tools/oai_portraits.py pixel <hero>           re-run the pixel conversion on the raw images (free)
    python tools/oai_portraits.py review <hero>          contact sheet generated/oai/<hero>_review.png

The API key is read from OPENAI_API_KEY (or the Windows user environment) and never printed.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

GEN = Path(__file__).resolve().parent.parent / "generated"
OUT = GEN / "oai"
RAW = OUT / "raw"
# 1.5x the old 140x200: more detail on the big carousel card, same shape.
PORTRAIT_W, PORTRAIT_H = 210, 300
BG = (136, 134, 138, 255)
OUTLINE = (22, 18, 24, 255)
COLORS = 64

STYLE = (
    "Full-body character portrait for a dark gothic fantasy action RPG in the style of Diablo 2, drawn as detailed pixel art: "
    "crisp pixels, limited muted palette, bold dark outlines, cel shading. Exactly one character, standing straight and "
    "facing three-quarters toward the viewer, the whole figure visible from the top of the head (and headwear) down to the "
    "feet. Natural anatomy: exactly two arms and two hands with five fingers each, two legs. Small realistic head, adult "
    "proportions, long legs, never chibi. Fully clothed. Transparent background, no ground, no shadow, no text, no frame."
)

HEROES = {
    "sorceress": "A fire sorceress in a long crimson hooded robe with gold trim, pale face, dark hair under the hood, holding a "
                 "gnarled wooden staff topped with a burning ember in one hand and a small flame floating above her other open palm.",
    "vampire": "A glamorous gothic vampire countess in a plum velvet gown with a high lace collar, long straight black hair, very "
               "pale skin, red eyes, dark lips, one hand resting on her hip, the other holding up the hem of her gown.",
    "inventor": "A gothic steampunk sky-pirate captain woman: black tricorn hat with gold trim, small skulls and red feathers; long "
                "wavy ash-blonde hair with braids and little chains; dark lipstick; a black leather corset with buckles over a white "
                "ruffled blouse; a long tattered black and crimson coat with gold trim; her right forearm is brass clockwork with "
                "visible gears and rivets, and that mechanical hand holds an ornate brass flintlock pistol raised beside her shoulder; "
                "her other hand rests on a cutlass hilt at her hip; brass lanterns and gears hang on chains from her belt; thigh-high "
                "laced black boots with skull buckles. Colour: add a little earthy red (rust and oxblood) to warm the browns: "
                "the coat's lining and tattered hem, a sash at her waist, the hat feathers and the trim.",
    "valkyrie": "A dark nordic frost valkyrie warrior queen: very long ash-black hair fading to icy silver-blue at the ends with "
                "braids, a silver crown, glowing glacier-blue eyes, a blackened-steel breastplate with glowing blue runes, a black fur "
                "mantle on one shoulder, a layered black and midnight-blue battle skirt, dark steel knee-high boots, holding upright an "
                "enormous dark iron and silver rune spear whose blade is a glowing shard of glacier ice. No wings. Absolutely no red: "
                "blackened steel, charcoal, silver, glacier blue and midnight blue only.",
    "berserker": "A tall muscular gothic barbarian berserker queen, battle-scarred, a dangerous half-smile, very long wild ash-brown "
                 "braided hair, an iron spike crown, a black leather and iron corset, a big wolf-fur mantle, bare muscular arms, a "
                 "leather and fur skirt, knee-high fur boots, carrying a gigantic two-handed executioner's battle axe over one "
                 "shoulder. Palette: blackened iron, dark leather, wolf-fur grey, earthy brown, muted bronze, a little dried crimson.",
    "reaper": "A gothic reaper woman with very long flowing silver-grey hair (no hood), pale face, a black gown and long black cloak "
              "decorated with bright glowing cyan rune symbols down the front, on the sleeves and along the hem, holding a huge black "
              "scythe with glowing blue runes on its blade.",
    "druid": "A gothic plague druid woman with a crown of black thorn branches like antlers, very long tangled chestnut hair with ivy, "
             "pale freckled skin, yellow-green eyes, a black raven-feather mantle, a dark bark-and-leather corset, a long torn green "
             "and brown skirt turning into roots at the hem, holding a twisted thorn staff topped with a glowing green orb.",
    "inquisitor": "A tall, slender gothic inquisitor woman in a long flowing black hooded robe; a pale, severe face framed by the hood "
                  "and ash-blonde hair; behind her head a golden halo of long sharp spikes with a golden band arching through them; "
                  "golden chains wrapped across her body and around her waist; a black leather corset under the robe; in one hand a "
                  "spiked golden censer hanging on a chain, glowing with white-gold holy fire.",
}


def api_key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k and sys.platform == "win32":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as h:
                k = winreg.QueryValueEx(h, "OPENAI_API_KEY")[0]
        except OSError:
            k = None
    if not k:
        sys.exit("OPENAI_API_KEY is not set")
    return k


def generate(prompt):
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1536",
        "quality": "high",
        "background": "transparent",
        "output_format": "png",
        "n": 1,
    }).encode()
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


def edit(image_path, prompt):
    """Edits an existing image (gpt-image-1 /images/edits, multipart) and returns PNG bytes."""
    boundary = "----ashen" + str(int(time.time() * 1000))
    parts = []

    crlf = "\r\n"

    def field(name, value):
        parts.append(f'--{boundary}{crlf}Content-Disposition: form-data; name="{name}"{crlf}{crlf}{value}{crlf}'.encode())

    field("model", "gpt-image-1")
    field("prompt", prompt)
    field("size", "1024x1536")
    field("quality", "high")
    field("background", "transparent")
    data = Path(image_path).read_bytes()
    head = f'--{boundary}{crlf}Content-Disposition: form-data; name="image[]"; filename="in.png"{crlf}Content-Type: image/png{crlf}{crlf}'
    parts.append(head.encode() + data + crlf.encode())
    parts.append(f"--{boundary}--{crlf}".encode())
    req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=b"".join(parts), method="POST",
                                 headers={"Authorization": f"Bearer {api_key()}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            out = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")
    return base64.b64decode(out["data"][0]["b64_json"]), out.get("usage")


def recolor(hero, src_n, note):
    """A new option: raw image <src_n> kept as it is, with the colour change asked for."""
    n = len(list(RAW.glob(f"{hero}_*.png")))
    prompt = ("Keep this exact image: the same character, pose, face, outfit, details, framing and pixel art style. "
              f"Only change the colour: {note} Keep the background transparent.")
    png, usage = edit(RAW / f"{hero}_{src_n}.png", prompt)
    (RAW / f"{hero}_{n}.png").write_bytes(png)
    with (OUT / "usage.log").open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {hero}_{n} edit of {src_n} {json.dumps(usage)}\n")
    pixelize(Image.open(RAW / f"{hero}_{n}.png")).save(OUT / f"{hero}_{n}.png")
    print("saved", hero, n, "(edit of", src_n, ")", flush=True)
    review(hero)


def pixelize(raw: Image.Image) -> Image.Image:
    """The model's big image -> a PORTRAIT_W x PORTRAIT_H pixel-art portrait on flat grey."""
    im = raw.convert("RGBA")
    box = im.getbbox()
    if box:
        im = im.crop(box)
    k = min((PORTRAIT_W - 8) / im.width, (PORTRAIT_H - 6) / im.height)
    small = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    # Hard edges: no half-transparent pixels.
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    small = rgb.convert("RGBA")
    small.putalpha(a)
    out = Image.new("RGBA", (PORTRAIT_W, PORTRAIT_H), BG)
    ox = (PORTRAIT_W - small.width) // 2
    oy = PORTRAIT_H - small.height - 3
    out.alpha_composite(small, (ox, oy))
    # A one-pixel dark outline around the silhouette, like the rest of the game's art.
    px, sp = out.load(), small.load()
    for y in range(-1, small.height + 1):
        for x in range(-1, small.width + 1):
            inside = 0 <= x < small.width and 0 <= y < small.height and sp[x, y][3] > 0
            if inside:
                continue
            near = any(0 <= x + dx < small.width and 0 <= y + dy < small.height and sp[x + dx, y + dy][3] > 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if near and 0 <= ox + x < PORTRAIT_W and 0 <= oy + y < PORTRAIT_H:
                px[ox + x, oy + y] = OUTLINE
    return out


def gen(hero, count=2):
    RAW.mkdir(parents=True, exist_ok=True)
    prompt = f"{STYLE}\n\nThe character: {HEROES[hero]}"
    n0 = len(list(RAW.glob(f"{hero}_*.png")))
    for i in range(n0, n0 + count):
        png, usage = generate(prompt)
        (RAW / f"{hero}_{i}.png").write_bytes(png)
        with (OUT / "usage.log").open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {hero}_{i} {json.dumps(usage)}\n")
        pixelize(Image.open(RAW / f"{hero}_{i}.png")).save(OUT / f"{hero}_{i}.png")
        print("saved", hero, i, flush=True)
    review(hero)


def pixel(hero):
    for p in sorted(RAW.glob(f"{hero}_*.png")):
        pixelize(Image.open(p)).save(OUT / p.name)
        print("pixelized", p.name)


def review(hero):
    ims = [Image.open(p).convert("RGBA") for p in sorted(OUT.glob(f"{hero}_*.png")) if "review" not in p.name]
    if not ims:
        return
    sheet = Image.new("RGBA", (sum(i.width + 6 for i in ims), PORTRAIT_H), (40, 36, 44, 255))
    x = 0
    for i in ims:
        sheet.alpha_composite(i, (x, 0))
        x += i.width + 6
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    sheet.save(OUT / f"{hero}_review.png")
    print("saved", OUT / f"{hero}_review.png")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gen":
        gen(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 2)
    elif cmd == "recolor":
        recolor(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif cmd == "pixel":
        pixel(sys.argv[2])
    elif cmd == "review":
        review(sys.argv[2])
