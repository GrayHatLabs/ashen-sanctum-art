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


# Take 2 (2026-10-06): PixelLab animates from the standing pose, where each weapon is held LOW. Asking for it
# raised made the first frames lift it, so it snapped back down as the walk looped. Keep the standing grip.
WALKS2 = {
    "reaper": "walking forward with steady steps, holding the scythe low at her side exactly as in her standing pose, the "
              "scythe does not move up or down, legs stepping under the gown",
    "berserker": "walking forward with heavy strides, holding the giant axe low at her right side exactly as in her standing "
                 "pose, the axe does not lift or swing, one axe only, legs stepping",
    "valkyrie": "walking forward with steady strides, holding the spear low at her side exactly as in her standing pose, the "
                "spear does not lift or turn, legs stepping",
}


# One direction only (the user, 2026-10-06: the valkyrie's diagonal walk). Walking down-right her spear passed
# behind her with a head showing at both ends, and her legs barely strode. pack.py's ALT uses this for that direction.
ONE_DIR = {
    ("valkyrie", "south"): "walking straight toward the viewer with clear strides, holding one short spear low in her right "
                           "hand with the spearhead pointing down at the ground, a single spearhead at the bottom end only, "
                           "the top end of the shaft is a plain wooden butt, the spear does not rise above her waist",
    ("valkyrie", "south-east"): "walking diagonally forward with clear long strides, holding one spear low in her right hand "
                                "pointing down and forward, a single spearhead at the front end only, the spear does not "
                                "cross behind her body",
}


def one_dir(hero, direction):
    import gen
    act2_art.safe(gen.animate, hero, ONE_DIR[(hero, direction)], 6, direction)
    print("one-direction retake done", hero, direction, flush=True)


def main(heroes):
    import world_art
    table = WALKS2 if heroes and heroes[0] == "take2" else WALKS
    heroes = heroes[1:] if heroes and heroes[0] == "take2" else heroes
    for h in heroes or list(table):
        act2_art.safe(world_art.run_anim, h, table[h], 6)
        print("walk retake done", h, flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["one"]:
        one_dir(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1:])
