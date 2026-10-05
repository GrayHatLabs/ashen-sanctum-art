"""Act 4 art: Mechanus, the Clockwork Dominion (gothic steampunk: brass, copper, verdigris, soot
black and boiler-fire orange), the refuge town of the Last Escapement, four clockwork dungeons
and the Clockmaker.

python act4_art.py props     tiles + isometric props (fast)
python act4_art.py chars     characters, then animations (long; resumable)
python act4_art.py review    contact sheet of tiles + props

Style rules: STYLE.md (small heads, realistic proportions, heroic / realistic_* presets).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import world_art  # noqa: E402
import act2_art  # noqa: E402

GEN = gen.GEN
HEADS = "small head, realistic adult body proportions, long legs"
MOOD = "gothic steampunk clockwork city, brass and copper, soot black, verdigris green"

CHARS = [
    ("cog_hound", "a brass clockwork hound with exposed gears, gear-tooth jaws and glowing orange eyes, steam venting from its back", 48, "none", "dog"),
    ("inquisitor", f"a gothic clockwork automaton monk in a hooded soot-black iron robe swinging a smoking brass censer, {HEADS}", 52, "heroic", ""),
    ("gearwraith", "a ghostly pale blue spirit trapped inside a floating cage-like brass frame of gears", 48, "none", ""),
    ("spring_jack", f"a spindly tall thin clockwork man with spring legs, long blade fingers and a grinning brass mask, {HEADS}", 52, "heroic", ""),
    ("boiler_brute", "a hulking iron golem with a glowing furnace belly, thick riveted arms and smokestacks on its shoulders", 64, "heroic", ""),
    ("ordinal", "a floating geometric brass drone shaped like a cube with a single glowing blue eye and small gear wings", 36, "none", ""),
    ("npc_tally", f"a gentle clockwork servant automaton with a porcelain face, brass body and a small glowing heart in its chest, {HEADS}", 48, "heroic", ""),
    ("npc_vesper", f"a steampunk woman tinkerer with goggles on her top hat, leather apron and a satchel of tools, {HEADS}", 48, "realistic_female", ""),
    ("npc_oiler", f"an old human mechanic monk in grey robes holding an oil can and a wrench, {HEADS}", 48, "realistic_male", ""),
    ("npc_servant", f"a small battered clockwork butler automaton with a round head and a dented bowler hat, {HEADS}", 44, "heroic", ""),
    ("boss_forgemother", f"a towering matriarch made of molten brass with a cauldron body, glowing slag dripping from her arms, {HEADS}", 84, "heroic", ""),
    ("boss_cantor", "a giant cathedral pipe organ walking on six brass spider legs, glowing stained glass and steam", 96, "none", ""),
    ("boss_archivist", f"a tall many-armed clockwork librarian in a long black coat holding punch cards and brass ledgers, {HEADS}", 84, "heroic", ""),
    ("boss_clockmaker", f"a tall gothic clockmaker in a stovepipe hat and long soot-black coat, half his chest an exposed glowing golden clockwork heart, holding a clock-hand blade, {HEADS}", 84, "heroic", ""),
    ("boss_clockmaker_engine", "an enormous clockwork automaton colossus of brass gears with a clock face in its chest and huge pendulum arms", 120, "none", ""),
]

ANIMS = [
    ("cog_hound", "mechanical hound running fast, gears turning", 6),
    ("cog_hound", "mechanical hound lunging forward and biting", 6),
    ("inquisitor", "automaton monk walking forward swinging the censer", 6),
    ("inquisitor", "automaton monk swinging the censer forward in a burst of steam", 6),
    ("gearwraith", "caged ghost floating forward", 6),
    ("gearwraith", "caged ghost lunging forward and shrieking", 6),
    ("spring_jack", "spring-legged automaton sprinting forward in long bounds", 6),
    ("spring_jack", "spring-legged automaton slashing with blade fingers", 6),
    ("boiler_brute", "iron golem stomping forward heavily", 6),
    ("boiler_brute", "iron golem smashing both fists down", 6),
    ("boss_forgemother", "molten brass matriarch striding forward", 6),
    ("boss_forgemother", "molten brass matriarch hurling molten slag", 6),
    ("boss_archivist", "many-armed librarian gliding forward", 6),
    ("boss_archivist", "many-armed librarian casting a spell with punch cards", 6),
    ("boss_clockmaker", "clockmaker striding forward, coat flowing", 6),
    ("boss_clockmaker", "clockmaker slashing with the clock-hand blade", 6),
    ("boss_clockmaker_engine", "clockwork colossus walking forward heavily", 6),
    ("boss_clockmaker_engine", "clockwork colossus slamming its pendulum arm down", 6),
    ("npc_servant", "clockwork butler walking stiffly", 6),
]

TILES = [
    ("brass_plate1", f"floor tile of riveted dark brass plates with soot stains, {MOOD}", "thin tile"),
    ("brass_plate2", f"floor tile of dark iron plates with a small embedded brass gear, {MOOD}", "thin tile"),
    ("grate_glow", "floor tile of iron grating with orange furnace glow underneath", "thin tile"),
    ("conveyor_road", "an iron conveyor belt road tile with rollers and copper rails", "thin tile"),
    ("verdigris_floor", "floor tile of old copper plates covered in green verdigris patina", "thin tile"),
    ("clock_floor", "floor tile of black marble with inlaid golden clock numerals", "thin tile"),
    ("brass_wall", "wall block of dark riveted brass and iron with a round porthole window glowing orange", "block"),
    ("fence_iron", "a gothic wrought iron fence wall block with gear ornaments", "block"),
]

PROPS = [
    ("gear_tower", "a chunky iron machine block with two huge brass cogwheels standing upright on it, bolts and rivets, wide and solid", 64, 80),
    ("steam_pipes", "a bulky copper boiler tank with thick pipes, pressure gauges and valve wheels, a puff of steam", 56, 64),
    ("steam_vent", "an iron steam vent grate in the floor puffing white steam", 32, 32),
    ("gas_lamp", "a gothic iron gas street lamp with a warm glow", 24, 64),
    ("cog_pile", "a pile of broken brass cogs and springs", 36, 28),
    ("workshop1", "a tall narrow gothic steampunk workshop house of soot-black brick with a copper roof and a glowing round window", 112, 112),
    ("workshop2", "a small clockmaker shop with a big clock face above the door and chimneys", 96, 104),
    ("clock_tower", "a gothic clock tower with a glowing clock face and brass spire", 64, 128),
    ("pendulum", "a giant brass pendulum hanging from an iron frame", 56, 96),
    ("ent_foundry", "a fiery foundry entrance with great furnace doors, molten light and smokestacks", 96, 96),
    ("ent_choir", "a gothic cathedral entrance made of organ pipes and stained glass, brass doors", 96, 104),
    ("ent_archive", "a gothic library entrance of dark stone with tall brass doors, walls of brass filing drawers and stacks of punch cards, glowing blue lamps", 96, 96),
    ("ent_clock", "the great door at the base of a colossal clock tower, a huge clock face above, golden light", 128, 128),
    ("gear_gate", "a standing circular stone portal ring with a huge brass cogwheel rim and golden light swirling inside, standing upright like a doorway", 80, 96),
]


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, pot, planter, platform")
    print("act4 props done", flush=True)


def chars():
    for name, desc, size, prop, tmpl in CHARS:
        if (GEN / name / "rotation_urls_south.png").exists():
            print("have", name, flush=True)
            continue
        if gen.state(name).get("character_id"):
            act2_art.safe(gen.fetch, name)
            if (GEN / name / "rotation_urls_south.png").exists():
                print("fetched", name, flush=True)
                continue
        act2_art.safe(gen.character, name, desc, size, prop, tmpl)
        print("made", name, flush=True)
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("act4 chars done", flush=True)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in TILES + PROPS if (GEN / n / "image.png").exists()]
    gen.review(GEN / "act4_props_review.png", *pngs)


if __name__ == "__main__":
    {"chars": chars, "props": props, "review": review}[sys.argv[1]]()
