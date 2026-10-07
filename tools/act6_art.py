"""Act 6 art: The Shattered Heavens (docs/ACT5_ACT6_PLAN.md in the game repo): floating islands above an endless
sea of ash-cloud, pale gold and cracked white marble, storm violet and sunset orange, broken halos and colossal angel
statues. The sky-harbour of Windward Anchorage, four sky dungeons and Solanthos, the Burnt-Out Sun.

python act6_art.py props     tiles + isometric props (fast)
python act6_art.py chars     characters, then animations (long; resumable)
python act6_art.py review    contact sheet of tiles + props

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
MOOD = "floating sky island high above the clouds, pale gold and cracked white marble, warm sunset light"

CHARS = [
    # monsters
    ("fallen_seraph", f"a fallen angel warrior with one broken grey-feathered wing and one torn wing, cracked white marble-like skin, tarnished gold armour, a spear of light, a dim broken halo, {HEADS}", 56, "heroic", ""),
    ("ophanim", "a floating holy wheel made of three interlocking golden rings tilted at different angles, many open eyes set along the rings, a glowing white core in the middle, an abstract floating object, no body, no head, no limbs", 48, "none", ""),
    ("storm_drake", "a small lean violet storm drake standing on four clawed legs like a lizard, leathery wings folded on its back, blue lightning crackling along its spine, long tail, quadruped beast, not humanoid", 56, "none", "dog"),
    ("ash_harpy", f"a harpy, a gaunt grey bird-woman with long ash-grey feathered wings in place of arms, bird legs ending in sharp black talons, a feathered body, wild white hair and a sharp pale face, {HEADS}", 52, "heroic", ""),
    ("gilded_sentinel", "a towering stone angel statue come to life, weathered white marble with gold-leaf robes, a great stone sword, cracks glowing gold", 72, "heroic", ""),
    ("sun_zealot", f"a fanatical sun cultist in sun-bleached white and gold robes with a sunburst mask, holding a burning golden staff, {HEADS}", 52, "heroic", ""),
    ("thunderbird", "a giant storm eagle, a bird flying with huge dark blue feathered wings spread wide, white lightning crackling between its feathers, a hooked beak, glowing white eyes, a bird not a human, no arms, no hands", 64, "none", ""),
    # townsfolk of Windward Anchorage
    ("npc_seraphine", f"a deserter angel woman with clipped short white wings, simple grey traveller's clothes over old gold armour, a scar across one eye, calm, {HEADS}", 48, "realistic_female", ""),
    ("npc_bram", f"an old sky-pirate quartermaster man with a white beard, a long blue coat, brass goggles and a peg leg, {HEADS}", 48, "realistic_male", ""),
    ("npc_aurel", f"a gentle healer nun woman in white and pale gold robes with a small sun pendant, {HEADS}", 48, "realistic_female", ""),
    ("npc_deckhand", f"a young airship deckhand in a leather cap, rolled sleeves and a rope coiled over one shoulder, {HEADS}", 48, "heroic", ""),
    # heralds and Solanthos
    ("boss_vael", f"Seraph-Commander Vael, a tall fallen archangel general in blackened gold plate armour, six dark wings, a burning spear of light, a cracked black halo, {HEADS}", 88, "heroic", ""),
    ("boss_tempest", "a massive storm-violet tempest dragon on four thick clawed legs, huge bat wings half spread above its back, glowing blue lightning veins in its scales, horned head, long spiked tail, quadruped beast", 110, "none", "bear"),
    ("boss_ophan", "a colossal floating holy wheel of many interlocking golden rings turning at different angles, hundreds of open eyes along the rings, a blazing white core, crackling light, an abstract floating object, no body, no head, no limbs", 104, "none", ""),
    ("boss_solanthos", f"Solanthos the burnt-out sun god, a towering figure of charred black stone cracked with molten gold light, a broken sunburst crown, embers and ash falling from him, {HEADS}", 96, "heroic", ""),
]

ANIMS = [
    ("fallen_seraph", "fallen angel walking forward, broken wing dragging", 6),
    ("fallen_seraph", "fallen angel diving forward and thrusting the spear of light", 6),
    ("storm_drake", "storm drake running forward on all four legs", 6),
    ("storm_drake", "storm drake breathing lightning, staying on all four legs", 6),
    ("ash_harpy", "harpy running forward, wings spread", 6),
    ("ash_harpy", "harpy slashing with its talons", 6),
    ("gilded_sentinel", "stone angel statue walking forward heavily", 6),
    ("gilded_sentinel", "stone angel statue slamming its great sword down", 6),
    ("sun_zealot", "sun cultist walking forward", 6),
    ("sun_zealot", "sun cultist raising the burning staff to cast", 6),
    ("boss_vael", "fallen archangel striding forward, wings spread", 6),
    ("boss_vael", "fallen archangel thrusting the burning spear", 6),
    ("boss_tempest", "dragon prowling forward on all four legs, wings folded", 6),
    ("boss_tempest", "dragon lowering its head and breathing lightning, staying on all four legs", 6),
    ("boss_solanthos", "burnt-out sun god striding forward, embers falling", 6),
    ("boss_solanthos", "burnt-out sun god raising both arms and unleashing a solar flare", 6),
    ("npc_deckhand", "deckhand walking forward", 6),
]

TILES = [
    ("cloud_marble1", f"floor tile of cracked white marble with thin gold veins, {MOOD}", "thin tile"),
    ("cloud_marble2", f"floor tile of weathered white marble paving with moss in the cracks, {MOOD}", "thin tile"),
    ("sky_grass", "floor tile of short pale golden grass on a sky island", "thin tile"),
    ("chain_bridge", "floor tile of light brown weathered wooden planks laid side by side with a dark iron chain running along each edge, a rope bridge deck", "thin tile"),
    ("choir_floor", "floor tile of dark marble with an inlaid golden sunburst, a ruined cathedral floor", "thin tile"),
    ("zenith_floor", "floor tile of black stone cracked with glowing molten gold light", "thin tile"),
    ("marble_wall", "wall block of white marble with gold trim and a broken arched window", "block"),
    ("storm_wall", "wall block of dark violet storm stone with blue lightning cracks", "block"),
]

PROPS = [
    ("angel_statue", "a broken colossal stone angel statue with one wing missing, white marble", 48, 96),
    ("halo_arch", "a huge broken golden halo ring standing upright in the ground like an arch", 64, 72),
    ("sky_lamp", "a tall white marble lamp post with a glowing golden orb", 24, 64),
    ("cloud_tree", "a small windswept tree with pale gold leaves on a rock", 40, 64),
    ("marble_ruin", "a few broken white marble columns and rubble", 56, 56),
    ("sky_house1", "a small white stone house with a blue domed roof and a weathervane, sky village", 96, 104),
    ("sky_house2", "a small white stone harbour tower house with a round golden dome, an arched door, a balcony and a hanging lantern", 96, 104),
    ("airship_dock", "a wooden airship dock jutting out over the clouds with a moored small airship with a canvas balloon", 96, 96),
    ("light_stair", "a magical staircase made of glowing translucent golden light, floating steps spiralling upward and fading into the sky, sparkles, no wood, no stone", 64, 112),
    ("ent_brokenchoir", "the entrance of a ruined cathedral in the sky, broken white marble arches and golden doors, angel statues either side", 96, 104),
    ("ent_spire", "a tall slender dark violet stone tower with a pointed spire, blue lightning crackling around the top, a large arched doorway at its base glowing blue", 80, 128),
    ("ent_wheel", "a great golden ring gate covered in carved eyes, light shining from inside", 96, 96),
    ("ent_zenith", "the colossal gate of a burnt black cathedral cracked with molten gold light, a broken sunburst above it", 128, 128),
    ("brk_crate_5", "a small white and gold wooden crate with a sun emblem, a single isometric object", 28, 28),
    ("brk_barrel_5", "a small round white painted wooden barrel with two shiny gold metal bands, standing upright, a single isometric object", 26, 30),
    ("brk_urn_5", "a small white marble urn with gold trim, a single isometric object", 20, 24),
]


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, pot, planter, platform")
    print("act6 props done", flush=True)


# Made as single images instead (the character generator gave them legs): tools/sky_objects_art.py.
OBJECTS = {"ophanim", "boss_ophan", "thunderbird"}


def characters():
    for name, desc, size, prop, tmpl in CHARS:
        if name in OBJECTS:
            continue
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
    print("act6 characters done", flush=True)


def chars():
    characters()
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("act6 chars done", flush=True)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in TILES + PROPS if (GEN / n / "image.png").exists()]
    gen.review(GEN / "act6_props_review.png", *pngs)


if __name__ == "__main__":
    {"chars": chars, "characters": characters, "props": props, "review": review}[sys.argv[1]]()
