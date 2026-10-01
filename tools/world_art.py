"""World expansion art (overworld, town, new monsters, bosses).

python world_art.py chars     8-direction characters, then their animations (stall-aware, long)
python world_art.py props     overworld tiles + isometric props (fast, synchronous)

Characters already generated are skipped; animations already on the server are waited for,
not re-requested. 5 directions per animation; pack.py mirrors the other 3.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import pixellab  # noqa: E402

GEN = gen.GEN
DIRS5 = ["south", "south-east", "east", "north-east", "north"]
STALL = 1500

# name, description, size, proportions, template
CHARS = [
    ("wolf", "gaunt grey dire wolf with glowing yellow eyes and matted fur", 48, "none", "dog"),
    ("imp", "small red demon imp with little horns, a crude spear and a ragged loincloth", 40, "default", ""),
    ("archer", "undead skeleton archer with a longbow, a quiver of arrows and a tattered dark hood", 48, "default", ""),
    ("npc_elder", "old village elder woman with grey braided hair, a long green shawl and a wooden walking cane", 48, "default", ""),
    ("npc_merchant", "stout merchant woman with a leather apron, a coin pouch and a red headscarf", 48, "default", ""),
    ("npc_healer", "bald monk healer in white and blue robes holding a prayer book", 48, "default", ""),
    ("npc_guard", "town guard in chainmail and a tabard, holding a spear and a round shield", 48, "heroic", ""),
    ("npc_villager", "peasant villager man in a brown tunic and a straw hat", 48, "default", ""),
    ("boss_bone", "huge armored skeleton warden knight with a massive bone greatsword and a horned helm", 80, "heroic", ""),
    ("boss_plague", "enormous bloated rotting plague zombie with green boils, dripping slime and huge fists", 80, "default", ""),
    ("boss_hex", "skeletal lich sorcerer in tattered purple robes holding a staff topped with a glowing violet skull", 72, "default", ""),
    ("boss_ashking", "the Ash King, a towering demonic lich king with a crown of black horns, burning ember eyes, "
                     "cracked charcoal skin and a cloak of ash and embers", 96, "heroic", ""),
]

# Priority order: regular monsters move first, then bosses, then extras.
ANIMS = [
    ("wolf", "wolf running fast, loping gallop", 6),
    ("imp", "imp scurrying forward hunched over with its spear", 6),
    ("archer", "skeleton walking forward holding a bow", 6),
    ("archer", "skeleton drawing the bow and shooting an arrow", 6),
    ("wolf", "wolf lunging forward and biting", 6),
    ("imp", "imp stabbing forward with its spear", 6),
    ("boss_bone", "giant skeleton knight walking heavily, greatsword in hand", 6),
    ("boss_bone", "giant skeleton knight swinging the greatsword in a wide overhead cleave", 6),
    ("boss_ashking", "demon lich king striding forward, cloak of embers billowing", 6),
    ("boss_ashking", "demon lich king raising both hands and casting a burst of fire", 6),
    ("boss_plague", "bloated zombie lumbering forward slowly", 6),
    ("boss_plague", "bloated zombie slamming both fists down", 6),
    ("boss_hex", "lich floating forward, robes trailing", 6),
    ("boss_hex", "lich thrusting the skull staff forward and casting a spell", 6),
    ("npc_villager", "villager walking calmly", 6),
]

# Overworld tiles: name, description, shape
TILES = [
    ("grass1", "lush dark green grass ground tile with a few small weeds", "thin tile"),
    ("grass2", "dark green grass ground tile with tiny white flowers and clover", "thin tile"),
    ("dirt1", "packed brown dirt ground tile with small pebbles", "thin tile"),
    ("road1", "worn cobblestone road tile, grey stones with dirt between", "thin tile"),
    ("palisade", "wooden log palisade wall block, sharpened vertical logs bound with rope", "block"),
]
# Props: name, description, w, h
PROPS = [
    ("tree_oak", "a leafy dark green oak tree with a thick brown trunk", 64, 88),
    ("tree_pine", "a tall dark green pine tree", 56, 96),
    ("tree_dead", "a twisted dead leafless tree with grey bark", 56, 80),
    ("rock1", "a large mossy grey boulder", 40, 32),
    ("bush1", "a round dark green shrub bush", 32, 28),
    ("house1", "a medieval timber-framed cottage with a thatched straw roof and a small wooden door", 128, 112),
    ("house2", "a small stone cottage with a dark slate roof, a chimney and a lit window", 112, 104),
    ("tent1", "a merchant market stall with a striped red and white canvas awning and crates of goods", 96, 80),
    ("campfire", "a crackling campfire ringed with stones and burning logs", 40, 36),
    ("well", "an old stone water well with a wooden roof and a bucket", 48, 56),
    ("ent_crypt", "a stone crypt entrance with a dark doorway, steps leading down and skull carvings", 96, 88),
    ("ent_warrens", "a dark cave mouth in a mound of earth and rocks, roots hanging, a gaping hole", 96, 80),
    ("ent_catacombs", "ancient purple stone catacomb gate with a heavy arch and violet glowing runes", 96, 96),
    ("ent_sanctum", "an ominous blackened cathedral gate with tall spires, red glowing runes and drifting ash", 128, 128),
    ("stairs_down", "a square stone stairwell going down into darkness in the floor", 64, 48),
    ("stairs_up", "a short stone staircase going up to a doorway of light", 64, 64),
    ("seal", "a glowing round magic seal amulet with a rune, item pickup", 32, 32),
]


def anim_dirs(name, display):
    st = gen.state(name)
    info = pixellab.call("GET", f"/characters/{st['character_id']}")
    dirs, group = set(), None
    for a in info.get("animations") or []:
        if a["display_name"] == display:
            group = a.get("animation_group_id")
            dirs |= {d["direction"] for d in a["directions"]}
    return dirs, group


def request(name, action, frames, dirs, group):
    body = {
        "character_id": gen.state(name)["character_id"],
        "action_description": action,
        "animation_name": action,
        "mode": "v3",
        "frame_count": int(frames),
        "keep_first_frame": False,
        "directions": dirs,
        "isometric": True,
    }
    if group:
        body["animation_group_id"] = group
    r = gen.call("POST", "/animate-character", body)
    gen.log_charge(f"{name} request {action} {dirs}", r.get("usage"))
    print("requested", name, action, dirs, flush=True)


def run_anim(name, action, frames):
    have, group = anim_dirs(name, action)
    last_change, last_have, requested = time.time(), set(have), False
    while not set(DIRS5) <= have:
        missing = [d for d in DIRS5 if d not in have]
        if not have and not requested:
            request(name, action, frames, missing, None)
            requested, last_change = True, time.time()
        elif time.time() - last_change > STALL:
            request(name, action, frames, missing, group)
            last_change = time.time()
        time.sleep(30)
        have, group = anim_dirs(name, action)
        if have != last_have:
            last_have, last_change = set(have), time.time()
            print(name, action, "now", sorted(have), flush=True)
    gen.fetch(name)
    print("done", name, action, flush=True)


def chars():
    for name, desc, size, prop, tmpl in CHARS:
        if (GEN / name / "rotation_urls_south.png").exists():
            print("have", name, flush=True)
            continue
        retry(gen.character, name, desc, size, prop, tmpl)
        print("made", name, flush=True)
    for name, action, frames in ANIMS:
        try:
            run_anim(name, action, frames)
        except Exception as e:  # keep going with the rest
            print("FAILED", name, action, e, flush=True)


def retry(fn, *args, tries=4):
    for k in range(tries):
        try:
            return fn(*args)
        except (RuntimeError, SystemExit) as e:
            print("retry", args[0], k, str(e)[:120], flush=True)
            time.sleep(30 * (k + 1))
    print("FAILED", args[0], flush=True)


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            retry(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            retry(gen.prop, name, desc, w, h)


if __name__ == "__main__":
    {"chars": chars, "props": props}[sys.argv[1]]()
