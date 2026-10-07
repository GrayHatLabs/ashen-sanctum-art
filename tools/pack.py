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
    # The Sky Pirate (the Inventor redesigned, tools/pirate_art.py; the old art is in generated/_old/inventor_v1).
    "inventor": [("idle", None, 1), ("walk", "walking confidently forward, tattered coat swaying", 10),
                 ("cast", "aiming the brass flintlock pistol forward and firing", 16),
                 ("throw", "throwing a small brass bomb forward with the mechanical arm", 14)],
    "steam_suit": [("idle", None, 1), ("walk", "heavy mech suit stomping forward, steam venting from its back", 8),
                   ("cast", "heavy mech suit firing its arm cannon forward with a blast of steam", 14)],
    "vampire": [("idle", None, 1), ("walk", "walking gracefully forward, cape flowing behind her", 10),
                ("cast", "casting a blood spell, thrusting one clawed hand forward", 16),
                ("attack", "slashing forward with long clawed fingers", 18)],
    # ---- Act 4 (tools/act4_art.py); the Ordinals are single floating-shape images (no limbs, by design) ----
    "brass_scarab": [("idle", None, 1), ("walk", "clockwork beetle scuttling forward fast on its piston legs", 12),
                     ("attack", "clockwork beetle lunging forward and snapping its mandibles", 14)],
    "inquisitor": [("idle", None, 1), ("walk", "automaton monk walking forward swinging the censer", 9),
                   ("attack", "automaton monk swinging the censer forward in a burst of steam", 11)],
    "gearwraith": [("idle", None, 1), ("walk", "caged ghost floating forward", 9), ("attack", "caged ghost lunging forward and shrieking", 12)],
    "spring_jack": [("idle", None, 1), ("walk", "spring-legged automaton sprinting forward in long bounds", 12),
                    ("attack", "spring-legged automaton slashing with blade fingers", 14)],
    "boiler_brute": [("idle", None, 1), ("walk", "iron golem stomping forward heavily", 7), ("attack", "iron golem smashing both fists down", 10)],
    "ordinal": [("idle", None, 1)],
    "ordinal_prism": [("idle", None, 1)],
    "ordinal_marshal": [("idle", None, 1)],
    "clock_crow": [("idle", None, 1)],  # tools/crow_art.py (bitforge, mirrored)
    "npc_tally": [("idle", None, 1)],
    "npc_vesper": [("idle", None, 1)],
    "npc_oiler": [("idle", None, 1)],
    "npc_servant": [("idle", None, 1), ("walk", "clockwork butler walking stiffly", 8)],
    "boss_forgemother": [("idle", None, 1), ("walk", "molten brass matriarch striding forward", 8),
                         ("attack", "molten brass matriarch hurling molten slag", 10)],
    "boss_cantor": [("idle", None, 1)],
    "boss_archivist": [("idle", None, 1), ("walk", "many-armed librarian gliding forward", 8),
                       ("attack", "many-armed librarian casting a spell with punch cards", 10)],
    "boss_clockmaker": [("idle", None, 1), ("walk", "clockmaker striding forward, coat flowing", 9),
                        ("attack", "clockmaker slashing with the clock-hand blade", 12)],
    "boss_clockmaker_engine": [("idle", None, 1), ("walk", "clockwork colossus walking forward heavily", 7),
                               ("attack", "clockwork colossus slamming its pendulum arm down", 9)],
    # ---- the Valkyrie (tools/valkyrie_art.py) ----
    "valkyrie": [("idle", None, 1), ("walk", "walking forward with steady strides, holding the spear low at her side exactly as in her standing pose, the spear does not lift or turn, legs stepping", 9),
                 ("attack", "thrusting the long spear forward in a fast lunge", 16),
                 ("sweep", "sweeping the long spear in a wide horizontal arc", 14),
                 ("whirl", "spinning around in a full circle whirling the spear", 14),
                 ("throw", "throwing the spear forward like a javelin", 14),
                 ("cast", "raising one hand to summon swirling frost magic", 12)],
    # (frost_raven came out as a raven-headed person: the character endpoint only draws humanoids. The game draws
    #  her raven in code, so it isn't packed.)
    "valkyrie_horse": [("idle", None, 1), ("walk", "warhorse galloping forward at full charge, rider leveling the spear", 14)],
    "einherjar": [("idle", None, 1), ("walk", "ghost warrior walking forward with shield raised", 9),
                  ("attack", "ghost warrior swinging the axe", 12)],
    # ---- the Berserker (tools/berserker_art.py) ----
    "berserker": [("idle", None, 1), ("walk", "walking forward with heavy strides, holding the one axe in her right hand in front of her exactly as in her standing pose, legs stepping", 9),
                  ("attack", "swinging the single axe in a wide horizontal cleave", 14),
                  ("chop", "raising the single axe high and chopping straight down", 12),
                  ("whirl", "spinning around in a full circle with the single axe held out", 14),
                  ("throw", "hurling the single axe forward with both hands", 14),
                  ("cast", "throwing her head back and roaring a war cry, the single axe raised", 10)],
    "dire_wolf": [("idle", None, 1), ("walk", "dire wolf running fast, loping gallop", 12),
                  ("attack", "dire wolf lunging forward and biting", 14)],
    # ---- the Druid (tools/druid_art.py) ----
    # The Inquisitor (tools/inquisitor_art.py); her iron halo is painted on by tools/inquisitor_halo.py.
    "inquisitor_hero": [("idle", None, 1), ("walk", "walking forward, long gown swaying with each step, feet stepping out under the hem, censer swinging", 9),
                        ("attack", "swinging the golden censer on its long chain forward like a flail", 14),
                        ("cast", "pointing one hand forward to burn a glowing sigil, censer hanging", 12),
                        ("spin", "spinning in place swinging the censer on its chain around her body, gown flaring", 14)],
    "druid": [("idle", None, 1), ("walk", "walking forward with clear steps, her legs visibly stepping one after the other under the torn skirt, holding the tall twisted thorn staff upright in one hand, the whole staff always visible from the ground to the glowing green orb at the top", 9),
              ("cast", "raising the thorn staff and casting glowing green plague magic", 12),
              ("summon", "kneeling and pressing one hand to the ground to summon creatures", 10)],
    "moss_wolf": [("idle", None, 1), ("walk", "wolf running fast, loping gallop", 12), ("attack", "wolf lunging forward and biting", 14)],
    "thorn_warden": [("idle", None, 1), ("walk", "tree guardian walking forward heavily", 7),
                     ("attack", "tree guardian smashing down with its root arm", 9)],
    # ---- the Reaper (tools/reaper_art.py) ----
    "reaper": [("idle", None, 1), ("walk", "walking forward with steady steps, holding the scythe low at her side exactly as in her standing pose, the scythe does not move up or down, legs stepping under the gown", 8),
               ("attack", "sweeping the great scythe in a wide horizontal arc", 14),
               ("cast", "raising one hand to cast spectral blue rune magic, scythe in the other hand", 12),
               ("spin", "spinning in a full circle with the scythe held out", 14)],
    # ---- Act 3 (tools/act3_art.py) ----
    "ghoul": [("idle", None, 1), ("walk", "ghoul loping forward hunched over", 10), ("attack", "ghoul slashing with both claws", 14)],
    "werewolf": [("idle", None, 1), ("walk", "werewolf running forward on two legs", 11), ("attack", "werewolf slashing with its claws", 14)],
    "banshee": [("idle", None, 1), ("walk", "ghost floating forward, robes drifting", 8), ("attack", "ghost leaning forward and screaming", 11)],
    "wisp": [("idle", None, 1)],
    "cultist": [("idle", None, 1), ("walk", "cultist walking forward holding the tome", 10),
                ("attack", "cultist raising the glowing tome and casting a spell", 11)],
    "npc_hunter": [("idle", None, 1)],
    "npc_widow": [("idle", None, 1)],
    # Jewelers, one per town (tools/jeweler_art.py).
    "npc_jeweler0": [("idle", None, 1)],
    "npc_jeweler1": [("idle", None, 1)],
    "npc_jeweler2": [("idle", None, 1)],
    "npc_jeweler3": [("idle", None, 1)],
    "npc_priest": [("idle", None, 1)],
    "npc_peasant": [("idle", None, 1), ("walk", "peasant walking nervously", 8)],
    "boss_ossric": [("idle", None, 1), ("walk", "skeleton lord walking forward with the spear", 8),
                    ("attack", "skeleton lord thrusting the bone spear", 10)],
    "boss_grimhilde": [("idle", None, 1), ("walk", "lich gliding forward, gown trailing", 8),
                       ("attack", "lich raising both hands and casting green fire", 10)],
    "boss_malgrave": [("idle", None, 1), ("walk", "death knight marching forward with shield raised", 8),
                      ("attack", "death knight swinging the long sword", 10)],
    "boss_vardak": [("idle", None, 1), ("walk", "vampire count walking forward with a sweep of his coat", 8),
                    ("attack", "vampire count thrusting his hand forward and casting blood magic", 10)],
    "boss_vardak_bat": [("idle", None, 1), ("walk", "giant bat flapping its wings and flying forward", 10),
                        ("attack", "giant bat swooping forward with fangs bared", 11)],
    "boss_dragon": [("idle", None, 1), ("walk", "dragon prowling forward on all four legs, wings folded", 7),
                    ("attack", "dragon lowering its head and breathing a blast of frost, staying on all four legs", 9)],
}
# Frames to use, in order, where a few in the middle went wrong (the rest of the cycle stays).
PICK = {
    # The Druid's walk (retake): the first frames raise the staff from her standing grip; use the upright ones.
    ("druid", "walk", "south"): [2, 3, 4, 5],
    ("druid", "walk", "south-east"): [2, 3, 4, 5],
    ("druid", "walk", "east"): [2, 3, 4, 5],
    ("druid", "walk", "north-east"): [2, 3, 4, 5],
    ("druid", "walk", "north"): [2, 3, 4, 5],
    # The Reaper's walk (take 2): walking away she lifts the scythe for two frames; skip them.
    ("reaper", "walk", "north"): [0, 1, 4, 5],
}
# A different animation for one direction (a one-direction retake; tools/walk_fix.py ONE_DIR).
ALT = {
    ("valkyrie", "walk", "south-east"): "walking diagonally forward with clear long strides, holding one spear low in her right "
                                        "hand pointing down and forward, a single spearhead at the front end only, the spear "
                                        "does not cross behind her body",
}
# Stray detached blobs to erase (smaller than this many pixels, not touching the figure).
CLEAN = {
    ("valkyrie", "walk", "east"): 120,
}


def drop_specks(im, limit):
    """Erases small groups of opaque pixels that aren't part of the largest one (the figure)."""
    im = im.convert("RGBA").copy()
    px = im.load()
    w, h = im.size
    seen, comps = set(), []
    for y in range(h):
        for x in range(w):
            if (x, y) in seen or px[x, y][3] == 0:
                continue
            st, comp = [(x, y)], []
            seen.add((x, y))
            while st:
                a, b = st.pop()
                comp.append((a, b))
                for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1), (a + 1, b + 1), (a - 1, b - 1), (a + 1, b - 1), (a - 1, b + 1)):
                    if 0 <= q[0] < w and 0 <= q[1] < h and q not in seen and px[q][3] > 0:
                        seen.add(q)
                        st.append(q)
            comps.append(comp)
    comps.sort(key=len)
    for c in comps[:-1]:
        if len(c) < limit:
            for q in c:
                px[q] = (0, 0, 0, 0)
    return im


# Directions where PixelLab drifted mid-animation: keep only the first N frames (then hold).
TRIM = {
    # Duchess Grimhilde's glide tips into a flat dive at the end (east, and the south-east crouch).
    ("boss_grimhilde", "walk", "east"): 3,
    ("boss_grimhilde", "walk", "south-east"): 3,
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
          "snow1", "snow2", "snow_road", "lake_ice", "ice_floor1", "ice_floor2",
          "mist_earth1", "mist_earth2", "mist_moss", "mist_road", "castle_floor",
          "brass_plate1", "brass_plate2", "grate_glow", "conveyor_road", "verdigris_floor", "clock_floor"]
WALL = "wall_stone"
ITEMS = ["food_apple", "food_bread", "food_roast", "seal"]
# Overworld and dungeon props (full size, anchored at the bottom centre).
PROPS = ["tree_oak", "tree_pine", "tree_dead", "rock1", "bush1", "house1", "house2", "tent1", "campfire", "well",
         "ent_crypt", "ent_warrens", "ent_catacombs", "ent_sanctum", "stairs_down", "stairs_up",
         "tree_snowpine", "tree_snowdead", "rock_snow", "ice_crystal", "longhouse1", "longhouse2", "stall_furs",
         "ent_mines", "ent_caves", "ent_temple", "ent_glacier", "pass_gate",
         "gadget_turret", "gadget_spider", "gadget_airship", "gadget_bomb",
         "tree_twisted", "tree_mistpine", "glow_shrooms", "gravestone", "cottage_mist", "cottage_mist2", "gallows",
         "merchant_cart", "ent_chapel", "ent_gallows", "ent_barrow", "ent_castle", "pass_mist",
         "gear_tower", "steam_pipes", "steam_vent", "gas_lamp", "cog_pile", "workshop1", "workshop2", "clock_tower",
         "pendulum", "ent_foundry", "ent_choir", "ent_archive", "ent_clock", "gear_gate",
         # Breakables (tools/breakables_art.py): brk_<crate|barrel|urn>_<act>.
         "brk_crate_0", "brk_barrel_0", "brk_urn_0", "brk_crate_1", "brk_barrel_1", "brk_urn_1",
         "brk_crate_2", "brk_barrel_2", "brk_urn_2", "brk_crate_3", "brk_barrel_3", "brk_urn_3"]
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
    if name == "druid":
        # Her standing pose held the staff as a short orb; stand her with it upright instead (a frame of her walk),
        # so the staff doesn't vanish whenever she stops (the user, 2026-10-06).
        walk = out.get(walk_fix_druid_walk())
        if walk:
            for k in ["south", "south-east", "east", "north-east", "north"]:
                if k in walk:
                    rot[k] = walk[k][4]
            for k, src in [("north-west", "north-east"), ("west", "east"), ("south-west", "south-east")]:
                if src in walk:
                    rot[k] = ImageOps.mirror(walk[src][4])
    if name == "inventor":
        # The Sky Pirate's hair, matched to her portrait (tools/pirate_hair.py).
        from pirate_hair import fix_frame as hair
        out = {k: {dd: [hair(f) for f in fs] for dd, fs in v.items()} for k, v in out.items()}
        rot = {k: hair(v) for k, v in rot.items()}
    if name == "inquisitor_hero":
        # The user's iron halo (spikes with an arching band) and more iron, on every frame.
        from inquisitor_halo import fix_frame
        out = {k: {dd: [fix_frame(f) for f in fs] for dd, fs in v.items()} for k, v in out.items()}
        rot = {k: fix_frame(v) for k, v in rot.items()}
    return out, rot


def walk_fix_druid_walk():
    import walk_fix
    return walk_fix.WALKS["druid"]


def pack_char(name, spec):
    anims, rot = char_frames(name)
    rows = []  # (anim name, fps, [[Image] per dir])
    report = []
    for game_name, display, fps in spec:
        per_dir = []
        have = anims.get(display, {}) if display else {}
        # Hand-picked frames and stray-blob cleanup (applied before mirroring, so the mirrored side is fixed too).
        for (n_, g_, d_), alt in ALT.items():
            if n_ == name and g_ == game_name and alt in anims and d_ in anims[alt]:
                have = {**have, d_: anims[alt][d_]}
        for dname in list(have):
            fr = have[dname]
            if (name, game_name, dname) in CLEAN:
                fr = [drop_specks(f, CLEAN[(name, game_name, dname)]) for f in fr]
            pick = PICK.get((name, game_name, dname))
            if pick:
                fr = [fr[i] for i in pick if i < len(fr)]
            have = {**have, dname: fr}
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
# Act 3 ground: pull toward a target colour and flatten the contrast so the forest floor reads
# as dim blue-grey earth (the moss keeps its glow, just quieter). name -> (target rgb, pull, contrast)
TONE_TILES = {"mist_earth1": ((58, 68, 78), 0.55, 0.45), "mist_earth2": ((54, 64, 72), 0.55, 0.45),
              "mist_road": ((74, 68, 60), 0.5, 0.5), "mist_moss": ((66, 78, 72), 0.72, 0.4),
              "castle_floor": ((70, 40, 46), 0.45, 0.5),
              # Act 4: quiet sooty brass and iron, so monsters and effects read on top.
              "brass_plate1": ((78, 62, 40), 0.6, 0.3), "brass_plate2": ((70, 58, 42), 0.6, 0.3),
              "verdigris_floor": ((52, 80, 70), 0.6, 0.3), "conveyor_road": ((44, 42, 44), 0.55, 0.4),
              "clock_floor": ((34, 32, 38), 0.55, 0.35), "grate_glow": ((70, 40, 24), 0.55, 0.35)}


def tone(im, target, pull, contrast):
    """Flatten contrast around the tile's mean colour, then pull the result toward `target`."""
    px = im.load()
    cs = [px[x, y] for y in range(im.height) for x in range(im.width) if px[x, y][3]]
    mean = [sum(c[i] for c in cs) / len(cs) for i in range(3)]
    for y in range(im.height):
        for x in range(im.width):
            c = px[x, y]
            if c[3]:
                v = [(mean[i] + (c[i] - mean[i]) * contrast) * (1 - pull) + target[i] * pull for i in range(3)]
                px[x, y] = tuple(max(0, min(255, int(k))) for k in v) + (255,)
    return im




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
        if n in TONE_TILES:
            im = tone(im, *TONE_TILES[n])
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
        for y in range(im.height if n in SOFT_TILES or n in ("snow_road", "mist_road", "mist_moss") else 0):
            if sum(1 for x in range(im.width) if px[x, y][3]) >= im.width * 0.9:
                mid = y
                break
        tiles.append({"name": n, "file": f"{n}.png", "anchor": [16 - b[0], mid]})
    for wall_name, src, stack in [("wall", WALL, WALL_STACK), ("palisade", "palisade", 2), ("ice_wall", "ice_wall", WALL_STACK), ("palisade_snow", "palisade_snow", 2),
                                  ("palisade_mist", "palisade_mist", 2), ("castle_wall", "castle_wall", WALL_STACK),
                                  ("fence_iron", "fence_iron", 2), ("brass_wall", "brass_wall", WALL_STACK)]:
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
    # OpenAI portraits turned to pixel art (tools/oai_portraits.py, 2026-10-06; the user's picks). The previous
    # portraits are kept in reference/portraits_v1/ (and their sources in generated/).
    for n, src in [("portrait_vampire", "oai/final/vampire.png"), ("portrait_sorceress", "oai/final/sorceress.png"),
                   ("portrait_inventor", "oai/final/inventor.png"), ("portrait_valkyrie", "oai/final/valkyrie.png"),
                   ("portrait_berserker", "oai/final/berserker.png"), ("portrait_reaper", "oai/final/reaper.png"),
                   ("portrait_druid", "oai/final/druid.png"), ("portrait_inquisitor", "oai/final/inquisitor.png")]:
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
        bg_src = {"portrait_vampire": "portrait_bg/vampire.png", "portrait_sorceress": "portrait_bg/sorceress.png", "portrait_inventor": "portrait_bg/pirate.png",
                  "portrait_valkyrie": "portrait_bg/valkyrie.png", "portrait_berserker": "portrait_bg/berserker.png",
                  "portrait_reaper": "portrait_bg/reaper.png", "portrait_druid": "portrait_bg/druid.png",
                  "portrait_inquisitor": "portrait_bg/inquisitor.png"}.get(n)
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
