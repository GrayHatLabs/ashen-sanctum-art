"""Breakable props (docs/BREAKABLES_PLAN.md in the game repo): crates, barrels and urns, a set per act.
Isometric bitforge props, one generation each. Named brk_<kind>_<act>, which is what the game looks for
(breakables::art_name); pack.py's PROPS list packs them at full size.

    python tools/breakables_art.py           generate the missing ones
    python tools/breakables_art.py review    contact sheet: generated/breakables_review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

PROPS = [
    # Act 1: the Ashlands crypts.
    ("brk_crate_0", "a small old wooden crate with iron corners, a single isometric object", 28, 28),
    ("brk_barrel_0", "a small old wooden barrel with dark iron hoops, a single isometric object", 24, 28),
    ("brk_urn_0", "a small cracked clay funeral urn with a narrow neck, a single isometric object", 20, 24),
    # Act 2: the Frostmarch.
    ("brk_crate_1", "a small wooden crate crusted with frost and snow and icicles, a single isometric object", 28, 28),
    ("brk_barrel_1", "a small frozen wooden barrel covered in ice and frost, a single isometric object", 24, 28),
    ("brk_urn_1", "a small pale blue urn bound in frost and ice, a single isometric object", 20, 24),
    # Act 3: the Mistwood (gothic).
    ("brk_crate_2", "a small upright dark wooden coffin with a tarnished silver cross, a single isometric object", 22, 34),
    ("brk_barrel_2", "a small rotten mossy old wooden barrel, a single isometric object", 24, 28),
    ("brk_urn_2", "a small bone-white urn decorated with carved skulls, a single isometric object", 20, 24),
    # Act 4: Mechanus (steampunk).
    ("brk_crate_3", "a small riveted brass crate with copper bands, a single isometric object", 28, 28),
    ("brk_barrel_3", "a small dark iron oil drum with brass bands and a valve, a single isometric object", 24, 28),
    ("brk_urn_3", "a small brass clockwork box with a gear on the lid, a single isometric object", 22, 22),
]


def main():
    for name, desc, w, h in PROPS:
        if not (gen.GEN / name / "image.png").exists():
            act2_art.safe(gen.prop, name, desc, w, h, "text, character, person, background, floor tiles, ground, shadow, multiple objects")
    print("breakables done", flush=True)


def review():
    gen.review(gen.GEN / "breakables_review.png", *[gen.GEN / n / "image.png" for n, *_ in PROPS if (gen.GEN / n / "image.png").exists()])


if __name__ == "__main__":
    review() if sys.argv[1:] == ["review"] else main()
