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
    "wolf": [("idle", None, 1), ("walk", "wolf running fast, loping gallop", 12), ("attack", "wolf lunging forward and biting", 14)],
    "goblin": [("idle", None, 1), ("walk", "goblin running forward hunched over with its dagger", 12),
               ("attack", "goblin lunging forward and stabbing with its dagger", 14)],
    "archer": [("idle", None, 1), ("walk", "skeleton walking forward holding a bow", 10),
               ("attack", "skeleton drawing the bow and shooting an arrow", 12)],
    "npc_elder": [("idle", None, 1)],
    "npc_merchant": [("idle", None, 1)],
    "npc_healer": [("idle", None, 1)],
    "npc_guard": [("idle", None, 1)],
    "npc_villager": [("idle", None, 1), ("walk", "villager walking calmly", 8)],
    "boss_bone": [("idle", None, 1), ("walk", "giant skeleton knight walking heavily, greatsword in hand", 8),
                  ("attack", "giant skeleton knight swinging the greatsword in a wide overhead cleave", 10)],
    "boss_plague": [("idle", None, 1), ("walk", "bloated zombie lumbering forward slowly", 6),
                    ("attack", "bloated zombie slamming both fists down", 9)],
    "boss_hex": [("idle", None, 1), ("walk", "lich floating forward, robes trailing", 8),
                 ("attack", "lich thrusting the skull staff forward and casting a spell", 10)],
    "boss_ashking": [("idle", None, 1), ("walk", "demon lich king striding forward, cloak of embers billowing", 8),
                     ("attack", "demon lich king raising both hands and casting a burst of fire", 10)],
    # ---- Act 2 (tools/act2_art.py) ----
    "frost_wolf": [("idle", None, 1), ("walk", "wolf running fast, loping gallop", 12), ("attack", "wolf lunging forward and biting", 14)],
    "raider": [("idle", None, 1), ("walk", "barbarian walking forward with the axe ready", 10),
               ("attack", "barbarian swinging the axe in a fast overhead chop", 14)],
    "yeti": [("idle", None, 1), ("walk", "yeti lumbering forward on two legs, arms swinging", 8), ("attack", "yeti smashing both fists down", 11)],
    "ice_troll": [("idle", None, 1), ("walk", "troll loping forward hunched over", 11), ("attack", "troll slashing with its long claws", 14)],
    "ice_wraith": [("idle", None, 1), ("walk", "wraith gliding forward, robes trailing", 9),
                   ("attack", "wraith lunging forward and raking with its claws", 12)],
    "npc_captain": [("idle", None, 1)],
    "npc_trader": [("idle", None, 1)],
    "npc_seer": [("idle", None, 1)],
    "npc_fisher": [("idle", None, 1), ("walk", "townsman walking calmly", 8)],
    "boss_giant": [("idle", None, 1), ("walk", "giant walking heavily forward, maul in hand", 7),
                   ("attack", "giant slamming the maul down onto the ground", 9)],
    "boss_yeti": [("idle", None, 1), ("walk", "giant yeti lumbering forward", 7),
                  ("attack", "giant yeti roaring and swiping with both arms", 10)],
    "boss_witch": [("idle", None, 1), ("walk", "ice witch gliding forward, gown trailing", 8),
                   ("attack", "ice witch raising the crystal staff and casting a spell", 10)],
    "inventor": [("idle", None, 1), ("walk", "walking confidently forward, skirt swaying", 10),
                 ("cast", "aiming the brass ray pistol forward and firing", 16),
                 ("throw", "throwing a small brass bomb forward with the mechanical arm", 14)],
    "steam_suit": [("idle", None, 1), ("walk", "heavy mech suit stomping forward, steam venting from its back", 8),
                   ("cast", "heavy mech suit firing its arm cannon forward with a blast of steam", 14)],
    "vampire": [("idle", None, 1), ("walk", "walking gracefully forward, cape flowing behind her", 10),
                ("cast", "casting a blood spell, thrusting one clawed hand forward", 16),
                ("attack", "slashing forward with long clawed fingers", 18)],
    "boss_dragon": [("idle", None, 1), ("walk", "dragon prowling forward on all four legs, wings folded", 7),
                    ("attack", "dragon lowering its head and breathing a blast of frost, staying on all four legs", 9)],
}
# Directions where PixelLab drifted mid-animation: keep only the first N frames (then hold).
TRIM = {
    ("boss_bone", "attack", "north"): 3,
    ("boss_dragon", "attack", "north"): 2,
    # The Rime Witch tips over and flies flat in the second half of her walk.
    ("boss_witch", "walk", "south"): 3,
    ("boss_witch", "walk", "south-east"): 3,
    ("boss_witch", "walk", "east"): 3,
    # The Yeti Matriarch shrinks as she walks toward the camera.
    ("boss_yeti", "walk", "south"): 2,
}
# Frames where PixelLab painted glowing effects onto an attack: (name, anim, dir) ->
#   ("drop", [frame indices])  replace those frames with the nearest clean one
#   ("use", "walk")            use another animation's frames for this direction
#   ("key", (r_max, g_min, b_min))  erase pixels that look like the stray effect colour
FIX = {
    # The vampire: a red-silhouette frame in the south cast, a cyan flash and a floating cape in the claw slash.
    ("vampire", "cast", "south"): ("drop", [2]),
    ("vampire", "attack", "south-east"): ("drop", [1]),
    ("vampire", "attack", "east"): ("use", "cast"),
    ("vampire", "attack", "north"): ("drop", [1, 2]),
    # Act 2: the ice troll's attack paints glowing frost rings over frames 2-4.
    ("ice_troll", "attack", "south"): ("drop", [2, 3, 4]),
    ("ice_troll", "attack", "south-east"): ("drop", [2, 3, 4]),
    ("ice_troll", "attack", "east"): ("drop", [2, 3, 4]),
    ("ice_troll", "attack", "north-east"): ("drop", [2, 3, 4]),
    ("ice_troll", "attack", "north"): ("drop", [2, 3, 4]),
    ("skeleton", "attack", "north"): ("drop", [0, 1]),
    ("zombie", "attack", "south"): ("drop", [2, 3]),
    ("zombie", "attack", "north"): ("use", "walk"),
    ("archer", "attack", "east"): ("key", (130, 150, 150)),
    ("boss_plague", "attack", "south-east"): ("drop", [2]),
    ("boss_hex", "attack", "east"): ("drop", [3]),
}


def apply_fix(fix, frames, rows_by_name):
    kind, arg = fix
    if kind == "drop":
        keep = [i for i in range(len(frames)) if i not in arg]
        return [frames[min(keep, key=lambda k: abs(k - i))] if i in arg else f for i, f in enumerate(frames)]
    if kind == "use":
        return rows_by_name.get(arg, frames)
    if kind == "key":
        rmax, gmin, bmin = arg
        out = []
        for im in frames:
            im = im.copy()
            px = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b, a = px[x, y]
                    if a and r < rmax and g > gmin and b > bmin:
                        px[x, y] = (0, 0, 0, 0)
            out.append(im)
        return out
    return frames


FLOORS = ["floor_stone1", "floor_stone2", "grass1", "grass2", "dirt1", "road1",
          "snow1", "snow2", "snow_road", "lake_ice", "ice_floor1", "ice_floor2"]
WALL = "wall_stone"
ITEMS = ["food_apple", "food_bread", "food_roast", "seal"]
# Overworld and dungeon props (full size, anchored at the bottom centre).
PROPS = ["tree_oak", "tree_pine", "tree_dead", "rock1", "bush1", "house1", "house2", "tent1", "campfire", "well",
         "ent_crypt", "ent_warrens", "ent_catacombs", "ent_sanctum", "stairs_down", "stairs_up",
         "tree_snowpine", "tree_snowdead", "rock_snow", "ice_crystal", "longhouse1", "longhouse2", "stall_furs",
         "ent_mines", "ent_caves", "ent_temple", "ent_glacier", "pass_gate",
         "gadget_turret", "gadget_spider", "gadget_airship", "gadget_bomb"]
ITEM_SIZE = 14
# Equipment icons (tools/items_art.py): longest side ICON_SIZE px in the inventory.
ICON_SIZE = 24
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
        # Per-direction fixes for glitchy generated frames.
        walk_rows = {r[0]: r[2] for r in rows}
        for di, dname in enumerate(DIRS):
            fix = FIX.get((name, game_name, dname))
            if fix:
                src = {k: v[di] for k, v in walk_rows.items()}
                per_dir[di] = apply_fix(fix, per_dir[di], src)
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


# Light ground tiles whose black outline draws a grid across the map: outline pixels are
# replaced by their lighter neighbours.
SOFT_TILES = {"snow1", "snow2", "lake_ice"}


def soften(im):
    px = im.load()
    lum = lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
    for _ in range(2):
        fix = []
        for y in range(im.height):
            for x in range(im.width):
                c = px[x, y]
                if c[3] and lum(c) < 95:
                    near = [px[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1))
                            if 0 <= x + dx < im.width and 0 <= y + dy < im.height]
                    light = [q for q in near if q[3] and lum(q) >= 95]
                    if light:
                        fix.append((x, y, tuple(sum(q[i] for q in light) // len(light) for i in range(3)) + (255,)))
        for x, y, c in fix:
            px[x, y] = c
    return im


def pack_tiles():
    tiles = []
    for n in FLOORS:
        p = GEN / n / "image.png"
        if not p.exists():
            continue
        im = load(p)
        b = im.getbbox()
        im = im.crop(b)
        if n in SOFT_TILES:
            im = soften(im)
        if n == "snow_road":
            # Trampled snow: lift the dark mud cracks toward a pale grey-brown.
            px = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    c = px[x, y]
                    l = 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
                    if c[3] and l < 150:
                        k = 0.75 if l < 90 else 0.45
                        px[x, y] = tuple(int(c[i] * (1 - k) + (168, 160, 150)[i] * k) for i in range(3)) + (255,)
        im.save(OUT / f"{n}.png")
        # Thin tile: anchor on the diamond's widest row (its middle). Drifts or tufts can poke
        # above the diamond, so the top of the bbox isn't always the top of the face.
        px = im.load()
        mid = 8
        for y in range(im.height if n in SOFT_TILES or n == "snow_road" else 0):
            if sum(1 for x in range(im.width) if px[x, y][3]) >= im.width * 0.9:
                mid = y
                break
        tiles.append({"name": n, "file": f"{n}.png", "anchor": [16 - b[0], mid]})
    for wall_name, src, stack in [("wall", WALL, WALL_STACK), ("palisade", "palisade", 2), ("ice_wall", "ice_wall", WALL_STACK), ("palisade_snow", "palisade_snow", 2)]:
        p = GEN / src / "image.png"
        if not p.exists():
            continue
        im = load(p)
        im = im.crop(im.getbbox())
        # Stack blocks: each block's face is (height - 16) tall.
        face = im.height - 16
        h = im.height + face * (stack - 1)
        st = Image.new("RGBA", (im.width, h))
        for k in range(stack):
            st.alpha_composite(im, (0, h - im.height - k * face))
        st.save(OUT / f"{wall_name}_stack.png")
        tiles.append({"name": wall_name, "file": f"{wall_name}_stack.png", "anchor": [im.width // 2, h - 8]})
        print(wall_name, st.size, "face", face * stack)
    return tiles


# Trees PixelLab drew standing on a pale grey disc: key the disc out of the bottom rows.
BASE_KEY = {"tree_oak"}


def key_base(im):
    import colorsys
    px = im.load()
    for y in range(int(im.height * 0.7), im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a:
                continue
            _, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if sat < 0.18 and l > 0.42:
                px[x, y] = (0, 0, 0, 0)
    # Drop the now-orphaned outline ring: dark pixels with no lighter opaque neighbour.
    y0 = int(im.height * 0.7)
    dark = lambda c: c[3] and sum(c[:3]) < 120
    for _ in range(2):
        kill = []
        for y in range(y0, im.height):
            for x in range(im.width):
                if not dark(px[x, y]):
                    continue
                near = [px[x + dx, y + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                        if 0 <= x + dx < im.width and 0 <= y + dy < im.height]
                if not any(c[3] and not dark(c) for c in near):
                    kill.append((x, y))
        for x, y in kill:
            px[x, y] = (0, 0, 0, 0)
    return im.crop(im.getbbox())


def pack_items():
    items = []
    for n in ITEMS:
        p = GEN / n / "image.png"
        if not p.exists():
            continue
        im = load(p)
        im = im.crop(im.getbbox())
        # Floor items are small in D2: longest side ITEM_SIZE px, hard alpha edge.
        f = ITEM_SIZE / max(im.size)
        if f < 1:
            im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
            px = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    c = px[x, y]
                    px[x, y] = (c[0], c[1], c[2], 255) if c[3] > 110 else (0, 0, 0, 0)
        im.save(OUT / f"{n}.png")
        items.append({"name": n, "file": f"{n}.png"})
        print("item", n, im.size)
    # Class-select portraits (tools/vampire_art.py): full size; a flat grey background is keyed out.
    # Cleaned-up versions (tools/portrait_fix.py); originals live in reference/portraits_original/.
    for n, src in [("portrait_vampire", "portrait_fix/vampire_face_a.png"), ("portrait_sorceress", "portrait_fix/sorceress_s300.png"),
                   ("portrait_inventor", "inventor/portrait_v3_220.png")]:
        p = GEN / src
        if not p.exists():
            continue
        im = load(p)
        px = im.load()
        bg = px[0, 0]
        flat = all(abs(px[x, y][i] - bg[i]) < 14 for x, y in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)] for i in range(3))
        if flat:
            # Flood fill from the corners so grey inside the figure stays.
            from collections import deque
            seen = set()
            q = deque([(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)])
            while q:
                x, y = q.popleft()
                if (x, y) in seen or not (0 <= x < im.width and 0 <= y < im.height):
                    continue
                c = px[x, y]
                if c[3] == 0 or max(abs(c[i] - bg[i]) for i in range(3)) > 16:
                    continue
                seen.add((x, y))
                px[x, y] = (0, 0, 0, 0)
                q.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
        # Themed backgrounds (tools/portrait_bg.py) behind the keyed figure, a little darker so she stands out.
        bg_src = {"portrait_sorceress": "portrait_bg/sorceress.png", "portrait_inventor": "portrait_bg/inventor.png"}.get(n)
        if bg_src and (GEN / bg_src).exists() and flat:
            bg = load(GEN / bg_src).resize(im.size)
            dark = Image.new("RGBA", im.size, (8, 6, 10, 70))
            bg.alpha_composite(dark)
            bg.alpha_composite(im)
            im = bg
            im.save(Path(__file__).resolve().parent.parent / "reference" / "portraits_clean" / f"{n.split('_')[1]}_portrait_bg.png")
        im.save(OUT / f"{n}.png")
        items.append({"name": n, "file": f"{n}.png"})
        print("portrait", n, im.size, "keyed" if flat else "", "+bg" if bg_src and flat else "")
    # Title screen background (tools/title_art.py), full size.
    p = GEN / "title" / "title_bg.png"
    if p.exists():
        load(p).save(OUT / "title_bg.png")
        items.append({"name": "title_bg", "file": "title_bg.png"})
    import items_art
    for n, _ in items_art.ICONS:
        p = GEN / n / "image.png"
        if not p.exists():
            continue
        im = load(p)
        im = im.crop(im.getbbox())
        f = ICON_SIZE / max(im.size)
        im = im.resize((max(1, round(im.width * f)), max(1, round(im.height * f))), Image.LANCZOS)
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                c = px[x, y]
                px[x, y] = (c[0], c[1], c[2], 255) if c[3] > 110 else (0, 0, 0, 0)
        im.save(OUT / f"{n}.png")
        items.append({"name": n, "file": f"{n}.png"})
    print("icons", len(items_art.ICONS))
    for n in PROPS:
        p = GEN / n / "image.png"
        if not p.exists():
            continue
        im = load(p)
        im = im.crop(im.getbbox())
        if n in BASE_KEY:
            im = key_base(im)
        im.save(OUT / f"prop_{n}.png")
        items.append({"name": n, "file": f"prop_{n}.png"})
    print("props", len(PROPS))
    return items


def main():
    OUT.mkdir(exist_ok=True)
    chars = []
    for name, spec in CHARS.items():
        if (GEN / name / "character.json").exists():
            chars.append(pack_char(name, spec))
    tiles = pack_tiles()
    items = pack_items()
    (OUT / "manifest.json").write_text(json.dumps({"chars": chars, "tiles": tiles, "items": items}, indent=2))
    print("wrote", OUT / "manifest.json")


if __name__ == "__main__":
    main()
