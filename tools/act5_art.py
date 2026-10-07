"""Act 5 art: The Drowned Deep (docs/ACT5_ACT6_PLAN.md in the game repo): a sunken realm under a black sea, lit by
glowing sea life: abyssal teal and black, cyan and violet glow, pale coral, rusted wrecks, kelp and pearl-white bone.
The town of Brinehollow (stilt houses on a giant wreck inside an air bubble), four drowned dungeons and the Leviathan.

python act5_art.py props     tiles + isometric props (fast)
python act5_art.py chars     characters, then animations (long; resumable)
python act5_art.py review    contact sheet of tiles + props

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
MOOD = "dark sunken sea floor, abyssal teal and black, glowing cyan and violet sea life, pale coral"

CHARS = [
    # monsters
    ("drowned_sailor", f"a drowned undead sailor, bloated pale grey-green waterlogged skin, empty white eyes, tattered dark grey rags of a sailor's coat dripping water, seaweed tangled in its hair, barnacles on its shoulders, a rusty cutlass, hunched, {HEADS}", 52, "heroic", ""),
    ("merrow", f"a fish-folk merrow warrior with dark teal scales, fin crest, webbed hands and a coral-tipped spear, hunched, {HEADS}", 52, "heroic", ""),
    ("anglerlurk", "a deep-sea anglerfish monster seen from above at an angle, a big round dark fish body low to the ground pulling itself along on two stubby front fins, an enormous gaping jaw of needle teeth, a glowing cyan lure dangling on a stalk from its forehead, no arms, no legs, not humanoid", 52, "none", ""),
    ("jelly_drift", "a floating glowing violet jellyfish with long crackling electric tentacles, translucent bell", 44, "none", ""),
    ("shellguard", "a large armoured crab knight with a huge barnacled shell and one giant shield-like claw raised in front", 52, "none", ""),
    ("siren", f"a siren sea witch woman with pale blue-green skin, shimmering teal fish scales on her arms and legs, fins on her forearms and ears, long dark wet hair tangled with seaweed, a torn dress of kelp, webbed hands, glowing teal eyes, {HEADS}", 52, "realistic_female", ""),
    ("ink_horror", "a squat dark octopus horror walking on its tentacles, many glowing violet eyes, dripping black ink", 52, "none", ""),
    # townsfolk of Brinehollow
    ("npc_ysolde", f"a one-eyed salvage captain woman with an eyepatch, a long weathered sea coat, a brass diving knife and a tricorn hat, {HEADS}", 48, "realistic_female", ""),
    ("npc_nessa", f"a young pearl-diver woman in a dark wetsuit-like leather outfit with a net bag of pearls and a diving mask on her head, {HEADS}", 48, "realistic_female", ""),
    ("npc_coral", f"an old tide-priest man in sea-green robes with coral jewellery and a staff topped with a glowing shell, {HEADS}", 48, "realistic_male", ""),
    ("npc_diver", f"a diver in an old brass diving helmet and canvas suit with weighted boots, {HEADS}", 48, "heroic", ""),
    # heralds and the Leviathan
    ("boss_dregmoor", f"a drowned admiral, a towering undead naval commander in a rotting admiral's coat and bicorne hat, barnacles and kelp, holding a huge anchor on a chain, {HEADS}", 84, "heroic", ""),
    ("boss_nacre", f"Mother Nacre, a tall siren queen with a crown of pearls, pale nacre skin, a long flowing dress of kelp and shells, glowing teal eyes, {HEADS}", 84, "realistic_female", ""),
    ("boss_angler", "a colossal deep-sea anglerfish monster, a huge round black and dark blue fish body resting low on the ground on fins, an enormous gaping jaw with rows of glassy needle teeth, small white eyes, a large glowing cyan lure on a long stalk arching over its head, not humanoid, no arms, no legs", 96, "none", ""),
    ("boss_leviathan", "the head and neck of an enormous sea serpent leviathan rising from the water, dark teal scales, glowing cyan eyes, fins like sails, huge jaws", 120, "none", ""),
]

ANIMS = [
    ("drowned_sailor", "drowned zombie shambling forward", 6),
    ("drowned_sailor", "drowned zombie slashing with its cutlass", 6),
    ("merrow", "fish-folk warrior running forward hunched", 6),
    ("merrow", "fish-folk warrior lunging forward with the spear", 6),
    ("anglerlurk", "anglerfish monster crawling forward", 6),
    ("anglerlurk", "anglerfish monster lunging and snapping its jaws", 6),
    ("jelly_drift", "jellyfish floating forward, tentacles trailing", 6),
    ("jelly_drift", "jellyfish crackling with electricity", 6),
    ("shellguard", "crab knight scuttling sideways forward", 6),
    ("shellguard", "crab knight smashing down with its big claw", 6),
    ("siren", "siren walking forward gracefully", 6),
    ("siren", "siren singing with arms spread, magic notes", 6),
    ("ink_horror", "octopus horror crawling forward on its tentacles", 6),
    ("ink_horror", "octopus horror spraying a cloud of black ink", 6),
    ("boss_dregmoor", "drowned admiral striding forward heavily", 6),
    ("boss_dregmoor", "drowned admiral swinging the anchor on its chain", 6),
    ("boss_nacre", "siren queen gliding forward", 6),
    ("boss_nacre", "siren queen singing a spell, arms raised", 6),
    ("boss_angler", "giant anglerfish crawling forward", 6),
    ("boss_angler", "giant anglerfish lunging with jaws wide", 6),
    ("boss_leviathan", "sea serpent rearing and swaying", 6),
    ("boss_leviathan", "sea serpent striking down with open jaws", 6),
    ("npc_diver", "diver walking slowly in weighted boots", 6),
]

TILES = [
    ("sea_sand1", f"floor tile of dark blue-grey sea floor sand with tiny shells, {MOOD}", "thin tile"),
    ("sea_sand2", f"floor tile of dark sea floor sand with small glowing cyan specks, {MOOD}", "thin tile"),
    ("coral_floor", "floor tile of dark blue-grey sea floor with small muted pink and white coral fragments and shells, dim, not bright", "thin tile"),
    ("flood_water", "floor tile of shallow dark teal water with ripples and a faint cyan glow", "thin tile"),
    ("wreck_deck", "floor tile of old dark wet wooden ship deck planks with iron nails", "thin tile"),
    ("sanctum_floor", "floor tile of drowned ancient pale stone with carved wave patterns and barnacles", "thin tile"),
    ("sanctum_wall", "wall block of ancient drowned stone covered in barnacles, kelp and a glowing cyan rune", "block"),
    ("coral_wall", "wall block of a dense reef of dark coral with glowing violet anemones", "block"),
]

PROPS = [
    ("kelp1", "a clump of tall dark olive-green kelp seaweed, several long wavy ribbon fronds rising from a rock, a plant", 32, 64),
    ("coral1", "a branching pale pink and white coral tree", 40, 44),
    ("coral2", "a low mound of brain coral and sea anemones with glowing violet tentacles on a rock", 36, 32),
    ("wreck_hull", "a small old wooden rowing boat lying broken and tilted on the sand, cracked dark planks, a hole in its side, seaweed, a single object", 72, 56),
    ("whale_bones", "a giant whale skull and a row of curved white rib bones sticking up out of the sand like arches", 96, 72),
    ("stilt_house1", "a small fishing shack on wooden stilts built from ship timbers with a round porthole window glowing warm", 96, 104),
    ("stilt_house2", "a tall narrow house made from an upturned ship's hull on stilts, with nets and lanterns", 96, 112),
    ("shell_lamp", "a lamp post made of driftwood topped with a giant glowing cyan shell", 24, 64),
    ("anchor_rock", "a classic ship anchor shape, dark rusty iron, a straight vertical shaft with a ring on top and two curved arms at the bottom, standing upright, a single object", 40, 52),
    ("diving_bell", "a large round brass diving bell with riveted plates, a round glass porthole and an open hatch, hanging from heavy chains from a wooden gantry frame", 80, 96),
    ("ent_wreck", "the curved wooden hull of a giant sunken galleon tilted on the sea floor, rows of small cannon ports, a large dark broken opening in the hull used as a cave entrance, barnacles and seaweed", 96, 96),
    ("ent_cathedral", "the entrance of a sunken cathedral made of coral and mother-of-pearl, pale arches and glowing windows", 96, 104),
    ("ent_trench", "a dark cave mouth plunging down into a deep trench, ringed by glowing anglerfish lures and bones", 96, 96),
    ("ent_drowned", "the colossal drowned gate of an ancient temple of pale stone, carved sea serpents coiling around it, glowing cyan", 128, 128),
    ("leviathan_coil", "a single huge arched coil of a dark teal scaled sea serpent's body rising out of the ground and back down", 96, 64),
    ("brk_crate_4", "a small old wooden crate covered in barnacles and seaweed, a single isometric object", 28, 28),
    ("brk_barrel_4", "a tall sealed brown clay amphora jar with two handles, crusted with barnacles, standing upright, a single isometric object", 24, 32),
    ("brk_urn_4", "a big closed giant clam with a ridged pale grey shell lying on the sand, a single isometric object", 30, 24),
]


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, pot, planter, platform")
    print("act5 props done", flush=True)


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
    print("act5 chars done", flush=True)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in TILES + PROPS if (GEN / n / "image.png").exists()]
    gen.review(GEN / "act5_props_review.png", *pngs)


def review_chars():
    pngs = [GEN / n / "rotation_urls_south.png" for n, *_ in CHARS if (GEN / n / "rotation_urls_south.png").exists()]
    gen.review(GEN / "act5_chars_review.png", *pngs)


if __name__ == "__main__":
    {"chars": chars, "props": props, "review": review, "review_chars": review_chars}[sys.argv[1]]()
