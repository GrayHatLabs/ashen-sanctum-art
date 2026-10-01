"""Ashen Sanctum art generation (isometric, D2-style). Uses pixellab.py for the API.

python gen.py character <name> "<desc>" <size> [proportions] [template]   (8 directions, standard = 1 gen)
python gen.py animate <name> "<action>" <frames> [dirs]                   (v3, all 8 dirs by default)
python gen.py isotile <name> "<desc>" [size] [shape] [seed]               (isometric floor/wall tile)
python gen.py image <name> <outfile> "<desc>" <w> <h> [negative]         (bitforge, transparent bg)
python gen.py prop <name> "<desc>" <w> <h> [negative]                    (isometric map object)
python gen.py fetch <name>                                               (free) re-download a character
python gen.py review <out.png> <png> [png ...]                           (free) 4x contact sheet
python gen.py spent                                                      (free) generations logged here

Everything lands in generated/<name>/. Charges are appended per job to generated/ashen_usage.log.
The API key is handled by pixellab.py and never printed.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pixellab  # noqa: E402
from pixellab import GEN, download, find_b64, find_urls, save_b64  # noqa: E402

LOG = GEN / "ashen_usage.log"
DIRS8 = "south,south-east,east,north-east,north,north-west,west,south-west"
STYLE = "dark gothic fantasy, Diablo 2 style, gritty muted colors"


def call(method, path, body=None):
    """pixellab.call with retry while the account is at its concurrent-job limit (HTTP 429)."""
    for _ in range(120):
        try:
            return pixellab.call(method, path, body)
        except SystemExit as e:
            if "HTTP 429" not in str(e):
                raise
            time.sleep(20)
    raise RuntimeError("still rate limited")


def log_charge(tag, usage):
    GEN.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {tag} {json.dumps(usage)}\n")


def wait(job_id, tag):
    t0 = time.time()
    while time.time() - t0 < 3600:
        j = pixellab.call("GET", f"/background-jobs/{job_id}")
        st = j.get("status")
        if st in ("completed", "failed"):
            log_charge(f"{tag} job={job_id} status={st}", j.get("usage"))
            if st == "failed":
                raise RuntimeError(f"job failed: {json.dumps(j.get('last_response'))[:600]}")
            return j
        time.sleep(5)
    raise RuntimeError("timeout")


def d_of(name):
    d = GEN / name
    d.mkdir(parents=True, exist_ok=True)
    return d


def state(name, upd=None):
    p = d_of(name) / "state.json"
    s = json.loads(p.read_text()) if p.exists() else {}
    if upd:
        s.update(upd)
        p.write_text(json.dumps(s, indent=2))
    return s


def fetch(name):
    s = state(name)
    d = d_of(name)
    info = pixellab.call("GET", f"/characters/{s['character_id']}")
    (d / "character.json").write_text(json.dumps(info, indent=2))
    for path, url in find_urls(info):
        download(url, d / (path.replace(".", "_") + ".png"))
    print("fetched", name)


def character(name, desc, size, proportions="heroic", template=""):
    size = int(size)
    body = {
        "description": f"{desc}, {STYLE}",
        "image_size": {"width": size, "height": size},
        "mode": "standard",
        "outline": "single color black outline",
        "shading": "medium shading",
        "detail": "medium detail",
        "view": "high top-down",
        "isometric": True,
    }
    if proportions and proportions != "none":
        body["proportions"] = {"type": "preset", "name": proportions}
    if template:
        body["template_id"] = template
    r = call("POST", "/create-character-with-8-directions", body)
    cid = r["character_id"]
    state(name, {"character_id": cid, "description": desc, "size": size})
    print("character", cid)
    if r.get("background_job_id"):
        wait(r["background_job_id"], f"{name} character")
    fetch(name)


def animate(name, action, frames=6, dirs=DIRS8):
    s = state(name)
    body = {
        "character_id": s["character_id"],
        "action_description": action,
        "animation_name": action,
        "mode": "v3",
        "frame_count": int(frames),
        "keep_first_frame": False,
        "directions": dirs.split(","),
        "isometric": True,
    }
    r = call("POST", "/animate-character", body)
    for jid in r.get("background_job_ids") or []:
        wait(jid, f"{name} animate {action}")
    fetch(name)


def isotile(name, desc, size=32, shape="thin tile", seed=0):
    body = {
        "description": f"{desc}, {STYLE}",
        "image_size": {"width": int(size), "height": int(size)},
        "isometric_tile_size": int(size),
        "isometric_tile_shape": shape,
        "outline": "lineless",
        "shading": "medium shading",
        "detail": "medium detail",
    }
    if int(seed):
        body["seed"] = int(seed)
    r = call("POST", "/create-isometric-tile", body)
    d = d_of(name)
    (d / "create.json").write_text(json.dumps(r, indent=2)[:20000])
    tid = r.get("tile_id") or r.get("id")
    if r.get("background_job_id"):
        wait(r["background_job_id"], f"{name} isotile")
    else:
        log_charge(f"{name} isotile", r.get("usage"))
    info = call("GET", f"/isometric-tiles/{tid}") if tid else r
    (d / "tile.json").write_text(json.dumps(info, indent=2)[:20000])
    n = 0
    for path, url in find_urls(info):
        download(url, d / (path.replace(".", "_") + ".png"))
        n += 1
    for path, img in find_b64(info):
        save_b64(img, d / (path.replace(".", "_") + ".png"))
        n += 1
    print("isotile", tid, "saved", n)


def image(name, outfile, desc, w, h, negative=""):
    body = {
        "description": f"{desc}, {STYLE}",
        "image_size": {"width": int(w), "height": int(h)},
        "no_background": True,
        "outline": "single color black outline",
        "shading": "medium shading",
        "detail": "medium detail",
        "view": "high top-down",
    }
    if negative:
        body["negative_description"] = negative
    r = call("POST", "/create-image-bitforge", body)
    log_charge(f"{name} image {outfile}", r.get("usage"))
    save_b64(r["image"], d_of(name) / outfile)
    print("saved", d_of(name) / outfile)


def prop(name, desc, w, h, negative=""):
    """Isometric map object (bitforge, transparent background, synchronous)."""
    body = {
        "description": f"{desc}, {STYLE}",
        "image_size": {"width": int(w), "height": int(h)},
        "no_background": True,
        "isometric": True,
        "outline": "single color black outline",
        "shading": "medium shading",
        "detail": "medium detail",
        "view": "high top-down",
        "negative_description": negative or "text, character, person, background, floor tiles",
    }
    r = call("POST", "/create-image-bitforge", body)
    log_charge(f"{name} prop", r.get("usage"))
    save_b64(r["image"], d_of(name) / "image.png")
    print("saved", d_of(name) / "image.png")


def review(out, *pngs):
    from PIL import Image
    ims = [Image.open(p).convert("RGBA") for p in pngs]
    w = sum(i.width for i in ims) + 4 * len(ims)
    h = max(i.height for i in ims)
    sheet = Image.new("RGBA", (w, h), (40, 36, 44, 255))
    x = 0
    for i in ims:
        sheet.alpha_composite(i, (x, 0))
        x += i.width + 4
    sheet.resize((w * 4, h * 4), Image.NEAREST).save(out)
    print("saved", out)


def spent():
    tot = 0.0
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            if "{" not in line:
                continue
            try:
                u = json.loads(line[line.index("{"):])
            except ValueError:
                continue
            if u and u.get("type") == "generations":
                tot += u.get("generations", 0)
    print("generations spent by gen.py:", tot)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmds = {"character": character, "animate": animate, "isotile": isotile, "image": image,
            "fetch": fetch, "review": review, "spent": spent, "prop": prop}
    cmds[a[0]](*a[1:])
