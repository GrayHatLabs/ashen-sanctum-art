"""The four town jewelers (sets and gems update). Idle rotations only: they stand at their benches.

    python tools/jeweler_art.py          # generate the missing ones (one character each)
    python tools/jeweler_art.py review   # contact sheet: generated/jeweler_review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
JEWELERS = [
    # Hollowmere (Act 1): Master Odo.
    ("npc_jeweler0", f"an old bald human jeweler with a white beard, a brass loupe over one eye, a purple velvet coat "
                     f"and a leather apron with small tools, {HEADS}", 48, "realistic_male"),
    # Kaldholm (Act 2): Ingrid Stonehand.
    ("npc_jeweler1", f"a sturdy northern woman gem cutter with blonde braids, a grey fur cloak over a blue tunic, "
                     f"a leather apron and a small hammer, {HEADS}", 48, "realistic_female"),
    # Mournhold (Act 3): Silas Greave.
    ("npc_jeweler2", f"a thin pale gothic man jeweler in a long black coat and top hat, a green gem pendant, "
                     f"holding a small lantern, {HEADS}", 48, "realistic_male"),
    # The Last Escapement (Act 4): the Lapidary.
    ("npc_jeweler3", f"a slender brass clockwork automaton jeweler with a tall cylinder head, one large magnifying lens eye "
                     f"and delicate multi-jointed fingers, wearing a small velvet apron, {HEADS}", 48, "heroic"),
]


def main():
    if sys.argv[1:] == ["review"]:
        ps = [gen.GEN / n / f"rotation_urls_{d}.png" for n, *_ in JEWELERS for d in ["south", "south-east", "east"]]
        gen.review(gen.GEN / "jeweler_review.png", *[p for p in ps if p.exists()])
        return
    for name, desc, size, prop in JEWELERS:
        if not (gen.GEN / name / "rotation_urls_south.png").exists():
            act2_art.safe(gen.character, name, desc, size, prop, "")
    print("jewelers done", flush=True)


if __name__ == "__main__":
    main()
