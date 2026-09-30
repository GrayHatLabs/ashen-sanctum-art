"""Pack generated PixelLab art into game sheets (the art contract read by the game's import_art.py).

python pack.py            -> sheets/<name>.png + sheets/manifest.json + sheets/preview_<name>.png

Character sheets: one row per (animation, direction), directions in PixelLab order
(south, south-east, east, north-east, north, north-west, west, south-west). A direction
that hasn't been animated yet is filled by mirroring its opposite (east <-> west), or the
idle rotation as a last resort, so the game always gets 8 complete rows.
"""
import json
from pathlib import Path

from PIL import Image, ImageOps

ART = Path(__file__).resolve().parent.parent
GEN = ART / "generated"
OUT = ART / "sheets"
DIRS = ["south", "south-east", "east", "north-east", "north", "north-west", "west", "south-west"]
MIRROR = {"east": "west", "west": "east", "north-east": "north-west", "north-west": "north-east",
          "south-east": "south-west", "south-west": "south-east", "south": "south", "north": "north"}

# name -> list of (game anim name, PixelLab animation display name or None for the idle rotation, fps)
CHARS = {
    "mage": [("idle", None, 1),
             ("walk", "walking forward, robe swaying, holding staff", 10),
             ("cast", "casting a fireball, thrusting the staff forward with one hand", 16)],
    "zombie": [("idle", None, 1),
               ("walk", "shambling slow zombie walk, arms reaching forward", 7),
               ("attack", "zombie clawing attack, lunging and swiping both arms", 12)],
    "skeleton": [("idle", None, 1),
                 ("walk", "skeleton walking, rattling bones, sword and shield raised", 10),
                 ("attack", "skeleton swinging its rusty sword in a fast slash", 14)],
}
# Directions where PixelLab drifted mid-animation: keep only the first N frames (then hold).
TRIM = {("zombie", "attack", "north"): 3, ("skeleton", "attack", "south-east"): 3, ("skeleton", "attack", "north-east"): 2}
FLOORS = ["floor_stone1", "floor_stone2"]
WALL = "wall_stone"
WALL_STACK = 3


def load(p):
    return Image.open(p).convert("RGBA")


def clean(im):
    """Remove a solid background PixelLab occasionally leaves behind (keyed from the corners)."""
    b = im.getbbox()
    if not b:
        return im
    w, h = im.size
    px = im.load()
    # Corners of the opaque region: a leftover background box fills its own bounding box.
    corners = [px[b[0], b[1]], px[b[2] - 1, b[1]], px[b[0], b[3] - 1], px[b[2] - 1, b[3] - 1]]
    bg = [c for c in corners if c[3] > 0]
    if len(bg) < 3:
        return im
    r0, g0, b0 = bg[0][:3]
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a and abs(r - r0) + abs(g - g0) + abs(b - b0) < 24:
                px[x, y] = (0, 0, 0, 0)
    return im


def char_frames(name):
    """{anim display name: {direction: [Image]}} plus {'__rot__': {direction: Image}}."""
    d = GEN / name
    info = json.loads((d / "character.json").read_text())
    out = {}
    for ai, a in enumerate(info.get("animations") or []):
        key = a.get("display_name")
        for di, dd in enumerate(a.get("directions") or []):
            frames = []
            for fi in range(len(dd.get("frames") or [])):
                p = d / f"animations_{ai}_directions_{di}_frames_{fi}.png"
                if p.exists():
                    im = clean(load(p))
                    # A blank frame (failed generation) repeats the previous one.
                    frames.append(im if im.getbbox() or not frames else frames[-1])
            if frames:
                out.setdefault(key, {})[dd["direction"]] = frames
    rot = {k: load(d / f"rotation_urls_{k}.png") for k in DIRS if (d / f"rotation_urls_{k}.png").exists()}
    return out, rot


def pack_char(name, spec):
    anims, rot = char_frames(name)
    rows = []  # (anim name, fps, [[Image] per dir])
    report = []
    for game_name, display, fps in spec:
        per_dir = []
        have = anims.get(display, {}) if display else {}
        if display and not have:
            report.append(f"{game_name}: missing")
            continue
        for dname in DIRS:
            if display is None:
                per_dir.append([rot[dname]])
            elif dname in have:
                fr = have[dname]
                keep = TRIM.get((name, game_name, dname))
                per_dir.append(fr[:keep] + [fr[keep - 1]] * (len(fr) - keep) if keep else fr)
            elif MIRROR[dname] in have:
                per_dir.append([ImageOps.mirror(im) for im in have[MIRROR[dname]]])
            else:
                per_dir.append([rot[dname]])
        n = max(len(f) for f in per_dir)
        per_dir = [(f * n)[:n] if len(f) < n else f for f in per_dir]
        rows.append((game_name, fps, per_dir))
        report.append(f"{game_name}: {sum(1 for d in DIRS if d in have) if display else 8}/8 dirs, {n} frames")
    # Common crop over every frame.
    boxes = [im.getbbox() for _, _, pd in rows for fr in pd for im in fr if im.getbbox()]
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    cw, ch = x1 - x0, y1 - y0
    sb = rot["south"].getbbox()
    anchor = ((sb[0] + sb[2]) // 2 - x0, sb[3] - 2 - y0)
    cols = max(len(pd[0]) for _, _, pd in rows)
    sheet = Image.new("RGBA", (cols * cw, len(rows) * 8 * ch))
    meta = []
    r = 0
    for game_name, fps, per_dir in rows:
        meta.append({"name": game_name, "row": r, "frames": len(per_dir[0]), "fps": fps})
        for fr in per_dir:
            for i, im in enumerate(fr):
                sheet.alpha_composite(im.crop((x0, y0, x1, y1)), (i * cw, r * ch))
            r += 1
    OUT.mkdir(exist_ok=True)
    sheet.save(OUT / f"{name}.png")
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(OUT / f"preview_{name}.png")
    print(name, f"cell {cw}x{ch} anchor {anchor}", "; ".join(report))
    return {"name": name, "file": f"{name}.png", "cell": [cw, ch], "anchor": list(anchor), "anims": meta}


def pack_tiles():
    tiles = []
    for n in FLOORS:
        p = GEN / n / "image.png"
        if not p.exists():
            continue
        im = load(p)
        b = im.getbbox()
        im = im.crop(b)
        im.save(OUT / f"{n}.png")
        # Thin tile: the top face is a 32x16 diamond starting at the top of the bbox.
        tiles.append({"name": n, "file": f"{n}.png", "anchor": [16 - b[0], 8]})
    p = GEN / WALL / "image.png"
    if p.exists():
        im = load(p)
        im = im.crop(im.getbbox())
        # Stack blocks: each block's face is (height - 16) tall.
        face = im.height - 16
        h = im.height + face * (WALL_STACK - 1)
        st = Image.new("RGBA", (im.width, h))
        for k in range(WALL_STACK):
            st.alpha_composite(im, (0, h - im.height - k * face))
        st.save(OUT / f"{WALL}.png")
        tiles.append({"name": "wall", "file": f"{WALL}.png", "anchor": [im.width // 2, h - 8]})
        print("wall", st.size, "face", face * WALL_STACK)
    return tiles


def main():
    OUT.mkdir(exist_ok=True)
    chars = []
    for name, spec in CHARS.items():
        if (GEN / name / "character.json").exists():
            chars.append(pack_char(name, spec))
    tiles = pack_tiles()
    (OUT / "manifest.json").write_text(json.dumps({"chars": chars, "tiles": tiles}, indent=2))
    print("wrote", OUT / "manifest.json")


if __name__ == "__main__":
    main()
