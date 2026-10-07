"""Endgame art (docs/ENDGAME_PLAN.md in the game repo): the Riftwarden of the Ash Rifts, the Rekindling brazier in
every town, and the rift portal.

    python tools/endgame_art.py           everything missing
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import world_art  # noqa: E402
import act2_art  # noqa: E402

GEN = gen.GEN
HEADS = "small head, realistic adult body proportions, long legs"

CHARS = [
    ("npc_riftwarden", f"a tall hooded warden in a long coat of charcoal grey and ember orange, a lantern full of swirling ash in one hand, a key ring of black iron keys at her belt, calm glowing eyes, {HEADS}", 52, "realistic_female", ""),
]
PROPS = [
    ("brazier_rekindle", "a tall black iron brazier on three clawed legs holding a bright fire of orange and white flames and glowing coals", 40, 64),
    ("rift_portal", "a swirling oval portal of ash and embers standing upright, dark grey and fiery orange, a ring of broken black stones around its base", 80, 96),
]


def main():
    for name, desc, w, h in PROPS:
        if not (GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles")
    for name, desc, size, prop, tmpl in CHARS:
        if not (GEN / name / "rotation_urls_south.png").exists():
            act2_art.safe(gen.character, name, desc, size, prop, tmpl)
    print("endgame art done", flush=True)


if __name__ == "__main__":
    main()
