"""Act 2 art: the Frostmarch (snow overworld, Kaldholm town, ice dungeons, the white dragon).

python act2_art.py props     snow / ice tiles + isometric props (fast, synchronous)
python act2_art.py chars     8-direction characters, then their animations (stall-aware, long)
python act2_art.py review    contact sheet of the props: generated/act2_props_review.png

Style rules: STYLE.md (small heads, realistic proportions, heroic / realistic_* presets).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import world_art  # noqa: E402

GEN = gen.GEN
HEADS = "small head, realistic adult body proportions, long legs"

# name, description, size, proportions, template
CHARS = [
    ("frost_wolf", "lean white-furred winter wolf with icy blue eyes and frost crusted on its fur", 48, "none", "dog"),
    ("raider", f"northern barbarian raider in heavy furs and a horned iron helm holding a hand axe, {HEADS}", 48, "heroic", ""),
    ("yeti", f"hulking white-furred yeti with long powerful arms and a blue-grey face, {HEADS}", 56, "heroic", ""),
    ("ice_troll", f"gaunt pale blue ice troll with long clawed arms and icicles growing on its back, {HEADS}", 52, "heroic", ""),
    ("ice_wraith", f"floating translucent pale blue wraith in tattered frosty robes with long clawed hands, {HEADS}", 48, "heroic", ""),
    ("npc_captain", f"stern northern woman captain in fur-lined chainmail with a long blonde braid and a sheathed sword, {HEADS}", 48, "realistic_female", ""),
    ("npc_trader", f"burly bearded fur trader in a heavy bear-fur coat and a fur hat, {HEADS}", 48, "realistic_male", ""),
    ("npc_seer", f"old northern seer woman in grey furs with bone charms and a gnarled staff, {HEADS}", 48, "realistic_female", ""),
    ("npc_fisher", f"townsman ice fisherman in a thick wool coat and a knit cap carrying a fishing spear, {HEADS}", 48, "realistic_male", ""),
    ("boss_giant", f"towering frost giant overseer with blue skin, a white braided beard, iron armor and a huge ice-crusted maul, {HEADS}", 88, "heroic", ""),
    ("boss_yeti", f"enormous ancient yeti matriarch with frost-crusted white fur and great curved ram horns, {HEADS}", 80, "heroic", ""),
    ("boss_witch", f"tall pale ice witch sorceress in a flowing gown of frost with an icicle crown and a crystal staff, {HEADS}", 72, "heroic", ""),
    ("boss_dragon", "ancient white dragon wyrm with pale icy scales, frost-rimmed spread wings, a long neck and a horned head, on four legs", 128, "none", ""),
]

# Regular monsters first, then bosses, then town extras.
ANIMS = [
    ("frost_wolf", "wolf running fast, loping gallop", 6),
    ("frost_wolf", "wolf lunging forward and biting", 6),
    ("raider", "barbarian walking forward with the axe ready", 6),
    ("raider", "barbarian swinging the axe in a fast overhead chop", 6),
    ("yeti", "yeti lumbering forward on two legs, arms swinging", 6),
    ("yeti", "yeti smashing both fists down", 6),
    ("ice_troll", "troll loping forward hunched over", 6),
    ("ice_troll", "troll slashing with its long claws", 6),
    ("ice_wraith", "wraith gliding forward, robes trailing", 6),
    ("ice_wraith", "wraith lunging forward and raking with its claws", 6),
    ("boss_dragon", "dragon walking forward on four legs, wings folded", 6),
    ("boss_dragon", "dragon rearing its head back and breathing a blast of frost", 6),
    ("boss_giant", "giant walking heavily forward, maul in hand", 6),
    ("boss_giant", "giant slamming the maul down onto the ground", 6),
    ("boss_yeti", "giant yeti lumbering forward", 6),
    ("boss_yeti", "giant yeti roaring and swiping with both arms", 6),
    ("boss_witch", "ice witch gliding forward, gown trailing", 6),
    ("boss_witch", "ice witch raising the crystal staff and casting a spell", 6),
    ("npc_fisher", "townsman walking calmly", 6),
]

TILES = [
    ("snow1", "fresh white snow ground tile with soft drifts and a few pale blue shadows", "thin tile"),
    ("snow2", "white snow ground tile with tiny frozen grass tufts poking through", "thin tile"),
    ("snow_road", "trampled snowy dirt path tile with footprints and wheel ruts", "thin tile"),
    ("lake_ice", "frozen lake ice tile, pale blue translucent ice with white cracks", "thin tile"),
    ("ice_floor1", "dungeon floor tile of pale blue ice with frost patterns", "thin tile"),
    ("ice_floor2", "dungeon floor tile of frozen stone flagstones covered in hoarfrost", "thin tile"),
    ("ice_wall", "wall block of glacial blue ice with frozen rock inside", "block"),
    ("palisade_snow", "wooden log palisade wall block with snow on top and icicles hanging", "block"),
]

PROPS = [
    ("tree_snowpine", "a tall dark green pine tree heavily covered in snow", 56, 96),
    ("tree_snowdead", "a bare twisted dead tree with snow on its branches", 56, 80),
    ("rock_snow", "a large grey boulder with a cap of snow", 40, 32),
    ("ice_crystal", "a cluster of tall jagged pale blue ice crystals", 40, 48),
    ("longhouse1", "a norse timber longhouse with a steep snowy roof, carved dragon gable ends and a wooden door, standing on white snow-covered ground, no grass", 128, 112),
    ("longhouse2", "a small log cabin with a snow covered roof, a stone chimney and smoke", 112, 104),
    ("stall_furs", "a fur trader's stall with a wooden frame, hanging pelts and crates", 96, 80),
    ("ent_mines", "a timber-framed mine entrance cut into a snowy rock cliff, with a mine cart track leading in", 96, 88),
    ("ent_caves", "a gaping ice cave mouth in a snowy hillside with huge icicles like teeth", 96, 88),
    ("ent_temple", "the frozen entrance of an ancient stone temple half buried in ice, with pale blue glowing runes", 96, 96),
    ("pass_gate", "a narrow snowy mountain pass between two grey rock cliffs with a wooden signpost and a trail", 96, 80),
    ("ent_glacier", "a towering gate carved into a blue glacier wall, with dragon skulls and frost mist", 128, 128),
]


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            world_art.retry(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            world_art.retry(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, pot, planter, platform")


def safe(fn, *args, tries=6):
    """Retries network hiccups (timeouts, resets) as well as API errors."""
    for k in range(tries):
        try:
            return fn(*args)
        except Exception as e:  # noqa: BLE001
            print("retry", fn.__name__, args[0], k, str(e)[:120], flush=True)
            time.sleep(30 * (k + 1))
    print("FAILED", fn.__name__, args[0], flush=True)


def chars():
    for name, desc, size, prop, tmpl in CHARS:
        if (GEN / name / "rotation_urls_south.png").exists():
            print("have", name, flush=True)
            continue
        if gen.state(name).get("character_id"):
            # Made on the server already (an earlier run was interrupted): just download it.
            safe(gen.fetch, name)
            if (GEN / name / "rotation_urls_south.png").exists():
                print("fetched", name, flush=True)
                continue
        safe(gen.character, name, desc, size, prop, tmpl)
        print("made", name, flush=True)
    for name, action, frames in ANIMS:
        safe(world_art.run_anim, name, action, frames)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in TILES + PROPS if (GEN / n / "image.png").exists()]
    gen.review(GEN / "act2_props_review.png", *pngs)


if __name__ == "__main__":
    {"chars": chars, "props": props, "review": review}[sys.argv[1]]()
