"""Side content art (docs/SIDE_CONTENT_PLAN.md in the game repo): shrines, the optional dungeons' entrances and their
bosses. Phase 1 is Act 1: the ash shrine, the Charnel Well and the Well-Witch.

python side_art.py props     shrines + entrances (fast)
python side_art.py chars     bosses, then their animations (long; resumable)
python side_art.py review    contact sheet

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

PROPS = [
    # Act 1: the Ashlands
    ("shrine_ash", "a small ancient shrine: a weathered grey stone altar with a carved hooded figure on top, a bowl of glowing orange embers and a rune carved on its front, a single isometric object", 40, 56),
    ("ent_wyrm", "a dark cave mouth in a jagged red-brown mountain rock face, scorched black around the opening, smoke curling out, a few gold coins and a broken shield scattered on the ground in front, glowing orange light deep inside, a single isometric object", 104, 96),
    ("hoard_gold", "a heap of shining gold coins with a jeweled golden goblet, a crown and a few gems, a single isometric object", 40, 32),
    ("ent_charnel", "a wide round old stone well seen from above at an angle, a black pit in the middle glowing sickly green, a rotten wooden winch frame with a rope over it, white human skulls and bones scattered on the ground around it, dark and creepy, a single isometric object", 96, 88),
]

CHARS = [
    ("boss_firewyrm", "a colossal ancient red fire dragon on four thick clawed legs, huge tattered bat wings half spread above its back, crimson and black scales glowing orange between the plates like embers, smoke from its nostrils, horned head, thick long spiked tail, quadruped beast", 128, "none", "bear"),
    ("boss_wellwitch", f"a hunched old swamp hag witch, grey-green warty skin, long stringy wet black hair, ragged dark brown robes dripping water, a necklace of small bones, a crooked wooden staff topped with a skull, glowing sickly green eyes, {HEADS}", 84, "realistic_female", ""),
]

ANIMS = [
    ("boss_firewyrm", "dragon prowling forward on all four legs, wings folded", 6),
    ("boss_firewyrm", "dragon lowering its head and breathing a torrent of fire, staying on all four legs", 6),
    ("boss_firewyrm", "dragon lying down curled up asleep on the ground, breathing slowly, eyes closed", 6),
    ("boss_wellwitch", "hag witch hobbling forward leaning on her staff", 6),
    ("boss_wellwitch", "hag witch thrusting her skull staff forward to cast a green curse", 6),
]


def props():
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, platform")
    print("side props done", flush=True)


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
    print("side chars done", flush=True)


def review():
    pngs = [GEN / n / "image.png" for n, *_ in PROPS if (GEN / n / "image.png").exists()]
    pngs += [GEN / n / "rotation_urls_south.png" for n, *_ in CHARS if (GEN / n / "rotation_urls_south.png").exists()]
    gen.review(GEN / "side_review.png", *pngs)


if __name__ == "__main__":
    {"props": props, "chars": chars, "review": review}[sys.argv[1] if len(sys.argv) > 1 else "props"]()
