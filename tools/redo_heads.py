"""Second pass (2026-10-01): goblins instead of imps, and smaller, realistic heads (like the
mage's) for skeletons, archers, zombies, townsfolk and two bosses.

python redo_heads.py      backs up the old art to generated/_old/<name>, then regenerates
Characters already redone (rotation exists in generated/<name>) are skipped, as are animations
already on the server, so it's safe to re-run.
"""
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import world_art  # noqa: E402

GEN = gen.GEN
SMALL = "small head, realistic adult body proportions, long legs"
CHARS = [
    ("goblin", f"lean green goblin with pointed ears, a crude iron dagger and a ragged leather loincloth, {SMALL}", 44, "heroic", ""),
    ("skeleton", f"undead skeleton warrior with a rusty sword and a cracked round shield, {SMALL}", 48, "heroic", ""),
    ("archer", f"undead skeleton archer with a longbow, a quiver of arrows and a tattered dark hood, {SMALL}", 48, "heroic", ""),
    ("zombie", f"rotting shambling zombie with grey-green skin and torn rags, arms outstretched, {SMALL}", 48, "heroic", ""),
    ("npc_villager", f"peasant villager man in a brown tunic and a straw hat, {SMALL}", 48, "realistic_male", ""),
    ("npc_elder", f"old village elder woman with grey braided hair, a long green shawl and a wooden walking cane, {SMALL}", 48, "realistic_female", ""),
    ("npc_merchant", f"stout merchant woman with a leather apron, a coin pouch and a red headscarf, {SMALL}", 48, "realistic_female", ""),
    ("npc_healer", f"bald monk healer in white and blue robes holding a prayer book, {SMALL}", 48, "realistic_male", ""),
    ("boss_plague", f"enormous bloated rotting plague zombie with green boils, dripping slime and huge fists, {SMALL}", 80, "heroic", ""),
    ("boss_hex", f"tall skeletal lich sorcerer in tattered purple robes holding a staff topped with a glowing violet skull, {SMALL}", 72, "heroic", ""),
]
# Same action names as before (pack.py maps them), goblin ones are new. Monsters first.
ANIMS = [
    ("goblin", "goblin running forward hunched over with its dagger", 6),
    ("skeleton", "skeleton walking, rattling bones, sword and shield raised", 6),
    ("zombie", "shambling slow zombie walk, arms reaching forward", 6),
    ("archer", "skeleton walking forward holding a bow", 6),
    ("goblin", "goblin lunging forward and stabbing with its dagger", 6),
    ("skeleton", "skeleton swinging its rusty sword in a fast slash", 6),
    ("zombie", "zombie clawing attack, lunging and swiping both arms", 6),
    ("archer", "skeleton drawing the bow and shooting an arrow", 6),
    ("boss_plague", "bloated zombie lumbering forward slowly", 6),
    ("boss_plague", "bloated zombie slamming both fists down", 6),
    ("boss_hex", "lich floating forward, robes trailing", 6),
    ("boss_hex", "lich thrusting the skull staff forward and casting a spell", 6),
    ("npc_villager", "villager walking calmly", 6),
]


def main():
    old = GEN / "_old"
    old.mkdir(exist_ok=True)
    marker = GEN / "_old" / "redone.txt"
    done = set(marker.read_text().split()) if marker.exists() else set()
    for name, desc, size, prop, tmpl in CHARS:
        if name in done:
            print("have", name, flush=True)
            continue
        if (GEN / name).exists():
            dest = old / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(GEN / name), str(dest))
        world_art.retry(gen.character, name, desc, size, prop, tmpl)
        if (GEN / name / "rotation_urls_south.png").exists():
            done.add(name)
            marker.write_text("\n".join(sorted(done)))
            print("made", name, flush=True)
    for name, action, frames in ANIMS:
        try:
            world_art.run_anim(name, action, frames)
        except Exception as e:  # keep going with the rest
            print("FAILED", name, action, e, flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
