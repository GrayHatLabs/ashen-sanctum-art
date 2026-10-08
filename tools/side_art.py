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
    # Act 6: the Shattered Heavens
    ("shrine_sky", "a small sky shrine: a white marble pedestal with a pair of small carved golden wings, a floating glowing golden sun-disc above it, a few white feathers at its base, a single isometric object", 40, 56),
    ("ent_observatory", "a ruined white marble observatory tower on a rock, its dome cracked open, a big brass telescope poking out, golden star-charts and constellations glowing on its walls, a dark arched doorway, a single isometric object", 104, 112),
    ("star_metal", "a jagged chunk of fallen meteorite rock, dark iron-black with glowing violet and pale blue crystal veins, faint sparkles, smoking slightly, a single isometric object", 40, 40),
    # Act 5: the Drowned Deep
    ("kraken_arm", "one long thick octopus tentacle arm alone, no head, no eyes, no body, rising straight up from the ground and curling over at the tip like a shepherd's crook, dark murky purple-grey skin, two rows of round pale suckers on the inner side, a few barnacles, realistic muted dark colours, a single isometric object", 64, 104),
    ("shrine_coral", "a small undersea shrine: a pale coral and mother-of-pearl altar shaped like a giant scallop shell, a glowing cyan pearl in its middle, kelp at its base, a single isometric object", 40, 56),
    ("ent_grotto", "a sea cave mouth in a mound of dark rock crusted with barnacles and pale coral, glowing pearls and shells around the opening, wet sand and seaweed, a single isometric object", 104, 96),
    # Act 4: Mechanus
    ("shrine_gear", "a small brass shrine: a polished brass pillar with a big glowing golden clock face and turning gears on its sides, steam hissing from a pipe, a single isometric object", 40, 56),
    ("ent_scrapheap", "a huge heap of rusted scrap metal, broken gears, pipes and dead automaton parts piled into a hill, with a dark tunnel opening into it held up by a bent iron girder, a single isometric object", 104, 96),
    # Act 3: the Mistwood
    ("shrine_mist", "a small ancient shrine: a mossy weathered stone grave-altar with a carved weeping angel, pale green ghost-light candles burning on it, a single isometric object", 40, 56),
    ("ent_cellar", "a slanted wooden cellar door set into an old earth mound in a graveyard, chains and a broken padlock, a dark stair going down, a rusty shovel leaning against it, a single isometric object", 96, 88),
    ("ent_manor", "a creepy abandoned gothic manor house, dark charcoal grey stone walls, black slate roof with a crooked chimney and a broken tower, boarded black windows, one window glowing ghostly pale green, dead black vines, gloomy and sinister, a single isometric object", 104, 112),
    ("bell_shrine", "a big dark bronze church bell hanging from a simple wooden A-frame gallows-like beam on the ground, a rope dangling from it, moss and candles at its foot, a single isometric object", 40, 72),
    ("tomb_shade", "an old stone crypt tomb with a cracked lid, a carved skull and a faint pale blue glow leaking from the crack, a single isometric object", 56, 48),
    # Act 2: the Frostmarch
    ("shrine_frost", "a small ancient shrine: a frosted grey-blue standing stone carved with a glowing pale blue rune, icicles hanging from it, a bowl of blue cold fire in front, snow at its base, a single isometric object", 40, 56),
    ("ent_longship", "the bow of a big viking longship frozen into thick blue ice, a carved dragon head on the prow, broken oars, a dark hole cut into its side as a doorway, snow on the deck, a single isometric object", 104, 96),
    # Act 1: the Ashlands
    ("shrine_ash", "a small ancient shrine: a weathered grey stone altar with a carved hooded figure on top, a bowl of glowing orange embers and a rune carved on its front, a single isometric object", 40, 56),
    ("ent_wyrm", "a dark cave mouth in a jagged red-brown mountain rock face, scorched black around the opening, smoke curling out, a few gold coins and a broken shield scattered on the ground in front, glowing orange light deep inside, a single isometric object", 104, 96),
    ("hoard_gold", "a heap of shining gold coins with a jeweled golden goblet, a crown and a few gems, a single isometric object", 40, 32),
    ("ent_charnel", "a wide round old stone well seen from above at an angle, a black pit in the middle glowing sickly green, a rotten wooden winch frame with a rope over it, white human skulls and bones scattered on the ground around it, dark and creepy, a single isometric object", 96, 88),
]

CHARS = [
    ("npc_magistrate", f"a stern clockwork magistrate judge, tall powdered white wig over a brass mask face, long black judge's robe with brass gears and a golden scale emblem, holding a gavel, {HEADS}", 52, "heroic", ""),
    ("automaton", f"a brass clockwork automaton knight, riveted polished brass armor plates, a glowing blue eye slit, a big wind-up key in its back, a sword arm made of a gear blade, {HEADS}", 52, "heroic", ""),
    ("boss_junkgolem", "a hulking golem made of rusted scrap metal, broken gears, pipes and a cracked boiler for a chest glowing orange, mismatched huge iron fists, hunched and massive", 96, "heroic", ""),
    ("npc_bogwitch", f"an old bog witch woman with a wide-brimmed tattered black hat, a cloak of moss and reeds, frog and bone charms on strings, a crooked walking stick, sly smile, {HEADS}", 48, "realistic_female", ""),
    ("boss_gravedigger", f"a huge hunched ghoul gravedigger, grey rotting skin, a filthy leather apron, a big iron shovel held in both hands, a lantern on his belt, long claws, {HEADS}", 84, "heroic", ""),
    ("boss_firewyrm", "a colossal ancient red fire dragon on four thick clawed legs, huge tattered bat wings half spread above its back, crimson and black scales glowing orange between the plates like embers, smoke from its nostrils, horned head, thick long spiked tail, quadruped beast", 128, "none", "bear"),
    ("boss_wellwitch", f"a hunched old swamp hag witch, grey-green warty skin, long stringy wet black hair, ragged dark brown robes dripping water, a necklace of small bones, a crooked wooden staff topped with a skull, glowing sickly green eyes, {HEADS}", 84, "realistic_female", ""),
]

ANIMS = [
    ("automaton", "clockwork knight marching forward stiffly", 6),
    ("automaton", "clockwork knight slashing with its gear blade", 6),
    ("boss_junkgolem", "scrap golem stomping forward heavily", 6),
    ("boss_junkgolem", "scrap golem smashing both iron fists down", 6),
    ("boss_gravedigger", "giant ghoul lumbering forward dragging a shovel", 6),
    ("boss_gravedigger", "giant ghoul slamming the shovel down onto the ground", 6),
    ("boss_firewyrm", "dragon prowling forward on all four legs, wings folded", 6),
    ("boss_firewyrm", "dragon lowering its head and breathing a torrent of fire, staying on all four legs", 6),
    ("boss_firewyrm", "dragon lying down curled up asleep on the ground, breathing slowly, eyes closed", 6),
    ("boss_wellwitch", "hag witch hobbling forward leaning on her staff", 6),
    ("boss_wellwitch", "hag witch thrusting her skull staff forward to cast a green curse", 6),
]


def props():
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, platform" + (", eyes, face, head, octopus body, cartoon, bright green" if name == "kraken_arm" else ""))
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
