"""Act 3 art: the Mistwood (Ravenloft style: misty forest, neon green and blue-grey earth),
the village of Mournhold, three skeleton-lord dungeons and Castle Vardak.

python act3_art.py props     tiles + isometric props (fast)
python act3_art.py chars     characters, then animations (long; resumable)
python act3_art.py review    contact sheet of tiles + props

Style rules: STYLE.md (small heads, realistic proportions, heroic / realistic_* presets).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import world_art  # noqa: E402
import act2_art  # noqa: E402

GEN = gen.GEN
HEADS = "small head, realistic adult body proportions, long legs"
MOOD = "eerie misty dark forest, neon green glow, cold blue-grey earth"

CHARS = [
    ("ghoul", f"gaunt grey-skinned ghoul crouching with long claws and glowing green eyes, {HEADS}", 48, "heroic", ""),
    ("werewolf", f"hulking werewolf with dark grey fur, standing on two legs, claws and fangs, {HEADS}", 56, "heroic", ""),
    ("banshee", f"floating pale ghostly woman banshee in tattered grey robes with long white hair and a glowing green mouth, {HEADS}", 48, "heroic", ""),
    ("wisp", "a small floating will-o'-wisp, a glowing neon green ball of ghost fire with wispy tendrils", 32, "none", ""),
    ("cultist", f"hooded dark cultist in a black and crimson robe holding a ritual dagger and a glowing green tome, {HEADS}", 48, "heroic", ""),
    ("npc_hunter", f"grim vampire hunter man with a wide-brimmed hat, long leather coat and a crossbow, {HEADS}", 48, "realistic_male", ""),
    ("npc_widow", f"old village widow in a black shawl and dress carrying a basket, {HEADS}", 48, "realistic_female", ""),
    ("npc_priest", f"village priest in black robes with a silver holy symbol, {HEADS}", 48, "realistic_male", ""),
    ("npc_peasant", f"frightened peasant man in a patched brown coat holding a lantern, {HEADS}", 48, "realistic_male", ""),
    ("boss_ossric", f"skeleton lord in rusted noble armor and a tattered fur cloak with a bone crown and a bone spear, {HEADS}", 80, "heroic", ""),
    ("boss_grimhilde", f"skeleton lich duchess in a ragged black gown with a tall bone crown and green necrotic flames in her hands, {HEADS}", 76, "heroic", ""),
    ("boss_malgrave", f"skeleton death knight in black plate armor with a tower shield and a long sword, glowing green eye sockets, {HEADS}", 80, "heroic", ""),
    ("boss_vardak", f"ancient vampire count in a black coat with a high crimson-lined collar, pale skin, slicked back dark hair and red eyes, {HEADS}", 80, "heroic", ""),
    ("boss_vardak_bat", "an enormous black vampire bat with leathery wings spread, red eyes and fangs, monstrous", 112, "none", ""),
]

ANIMS = [
    ("ghoul", "ghoul loping forward hunched over", 6),
    ("ghoul", "ghoul slashing with both claws", 6),
    ("werewolf", "werewolf running forward on two legs", 6),
    ("werewolf", "werewolf slashing with its claws", 6),
    ("banshee", "ghost floating forward, robes drifting", 6),
    ("banshee", "ghost leaning forward and screaming", 6),
    ("cultist", "cultist walking forward holding the tome", 6),
    ("cultist", "cultist raising the glowing tome and casting a spell", 6),
    ("boss_vardak", "vampire count walking forward with a sweep of his coat", 6),
    ("boss_vardak", "vampire count thrusting his hand forward and casting blood magic", 6),
    ("boss_vardak_bat", "giant bat flapping its wings and flying forward", 6),
    ("boss_vardak_bat", "giant bat diving forward to bite", 6),
    ("boss_ossric", "skeleton lord walking forward with the spear", 6),
    ("boss_ossric", "skeleton lord thrusting the bone spear", 6),
    ("boss_grimhilde", "lich gliding forward, gown trailing", 6),
    ("boss_grimhilde", "lich raising both hands and casting green fire", 6),
    ("boss_malgrave", "death knight marching forward with shield raised", 6),
    ("boss_malgrave", "death knight swinging the long sword", 6),
    ("npc_peasant", "peasant walking nervously", 6),
]

TILES = [
    ("mist_earth1", f"dark blue-grey earth ground tile with damp soil and a few dead leaves, {MOOD}", "thin tile"),
    ("mist_earth2", f"dark blue-grey earth ground tile with small tufts of glowing neon green moss, {MOOD}", "thin tile"),
    ("mist_moss", "ground tile covered in thick glowing neon green moss and tiny mushrooms", "thin tile"),
    ("mist_road", "a muddy dirt road tile with puddles and old cart ruts, blue-grey tones", "thin tile"),
    ("castle_floor", "dark castle flagstone floor tile with a worn crimson carpet runner", "thin tile"),
    ("castle_wall", "wall block of dark gothic castle stone with a narrow arched window", "block"),
    ("palisade_mist", "a crooked old wooden fence wall block, rotten planks with green moss", "block"),
]

PROPS = [
    ("tree_twisted", "a spooky gnarled dead tree with black twisted bark and bare clawing branches, only a few yellow autumn leaves clinging on and a few falling, halloween style", 56, 88),
    ("tree_mistpine", "a tall spooky dead tree with a hollow split trunk and bare crooked branches, sparse yellow fall leaves, halloween style", 48, 88),
    ("glow_shrooms", "a cluster of glowing neon green mushrooms", 28, 24),
    ("gravestone", "a crooked old gravestone with moss", 24, 28),
    ("cottage_mist", "a small crooked timber village cottage with a sagging roof, shuttered windows and a faint lantern", 112, 104),
    ("cottage_mist2", "a narrow tall stone house with a steep roof and garlic hanging at the door", 96, 104),
    ("gallows", "an old wooden gallows with a hanging empty noose", 48, 64),
    ("merchant_cart", "an old covered merchant wagon with lanterns and sacks", 80, 64),
    ("ent_chapel", "a ruined sunken stone chapel half drowned in a bog, broken bell tower, green glow inside", 96, 96),
    ("ent_gallows", "a dark stone stairway down into catacombs beneath a ring of gallows, skulls and candles", 96, 88),
    ("ent_barrow", "an ancient burial barrow mound with a stone doorway flanked by standing stones", 96, 80),
    ("ent_castle", "the great iron-bound gate of a gothic vampire castle with tall towers and red-lit windows", 128, 128),
    ("pass_mist", "a narrow forest road into thick mist between two dead trees with a crooked signpost", 96, 80),
]


def props():
    for name, desc, shape in TILES:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.isotile, name, desc, 32, shape)
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, pot, planter, platform")
    print("act3 props done", flush=True)


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
    print("act3 chars done", flush=True)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in TILES + PROPS if (GEN / n / "image.png").exists()]
    gen.review(GEN / "act3_props_review.png", *pngs)


if __name__ == "__main__":
    {"chars": chars, "props": props, "review": review}[sys.argv[1]]()
    _ = time
