"""Walk retakes (the user, 2026-10-06: the reaper's scythe vanishes walking up-right, the berserker walks oddly).
A check of every hero's walk found the weapon unsteady for four of them:
    reaper     the scythe blade floats loose above her, appearing and vanishing (north-east, north)
    berserker  the axe pops in and out, two axes at once in some directions
    valkyrie   the spear flips from pointing down to up mid-step
    druid      the staff shrinks to a floating orb
Each gets a new walk asking for the weapon held the same way through the whole cycle. pack.py's CHARS
then points at the new display names (the old animations stay in each character's folder).

    python tools/walk_fix.py [hero ...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import act2_art  # noqa: E402

WALKS = {
    "reaper": "walking forward calmly holding the huge scythe upright in one hand, the long handle always in her hand and the "
              "blade always above her shoulder, the same grip in every step",
    "berserker": "striding forward with the giant axe resting on her right shoulder held by the haft in both hands, the axe "
                 "stays on her shoulder the whole time, one axe only",
    "valkyrie": "walking forward holding the long spear upright at her side, the spear point always up, the same grip in every step",
    # The user: walking sideways her legs don't move, and up-right looks odd. Ask for clear steps too.
    "druid": "walking forward with clear steps, her legs visibly stepping one after the other under the torn skirt, holding the "
             "tall twisted thorn staff upright in one hand, the whole staff always visible from the ground to the glowing green "
             "orb at the top",
}


def main(heroes):
    import world_art
    for h in heroes or list(WALKS):
        act2_art.safe(world_art.run_anim, h, WALKS[h], 6)
        print("walk retake done", h, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
