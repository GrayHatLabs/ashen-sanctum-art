"""Run the remaining MVP animations. PixelLab shares its job slots with other projects on this
account, and jobs left over from stopped runs can stall, so for each animation:

  * if it already exists on the server, wait for its 5 directions (S, SE, E, NE, N);
  * if a direction hasn't appeared after STALL seconds, request just the missing directions
    (added to the same animation group); pack.py mirrors the other 3 directions.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import pixellab  # noqa: E402

DIRS5 = ["south", "south-east", "east", "north-east", "north"]
STALL = 1500
JOBS = [
    ("zombie", "shambling slow zombie walk, arms reaching forward", 6),
    ("skeleton", "skeleton walking, rattling bones, sword and shield raised", 6),
    ("mage", "casting a fireball, thrusting the staff forward with one hand", 6),
    ("zombie", "zombie clawing attack, lunging and swiping both arms", 6),
    ("skeleton", "skeleton swinging its rusty sword in a fast slash", 6),
]


def anim_info(name, display):
    st = gen.state(name)
    info = pixellab.call("GET", f"/characters/{st['character_id']}")
    dirs, group = set(), None
    for a in info.get("animations") or []:
        if a["display_name"] == display:
            group = a.get("animation_group_id")
            dirs |= {d["direction"] for d in a["directions"]}
    return dirs, group


def request(name, action, frames, dirs, group):
    body = {
        "character_id": gen.state(name)["character_id"],
        "action_description": action,
        "animation_name": action,
        "mode": "v3",
        "frame_count": int(frames),
        "keep_first_frame": False,
        "directions": dirs,
        "isometric": True,
    }
    if group:
        body["animation_group_id"] = group
    r = gen.call("POST", "/animate-character", body)
    gen.log_charge(f"{name} request {action} {dirs}", r.get("usage"))
    print("requested", name, action, dirs, "jobs", r.get("background_job_ids"), flush=True)


# Optional args: indices into JOBS to run (default: all, in order).
selected = [JOBS[int(i)] for i in sys.argv[1:]] or JOBS
for name, action, frames in selected:
    have, group = anim_info(name, action)
    last_change, last_have = time.time(), set(have)
    requested = False
    while not set(DIRS5) <= have:
        missing = [d for d in DIRS5 if d not in have]
        if not have and not requested:
            request(name, action, frames, missing, None)
            requested = True
            last_change = time.time()
        elif time.time() - last_change > STALL:
            request(name, action, frames, missing, group)
            last_change = time.time()
        time.sleep(30)
        have, group = anim_info(name, action)
        if have != last_have:
            last_have, last_change = set(have), time.time()
            print(name, action, "now", sorted(have), flush=True)
    gen.fetch(name)
    print("done", name, action, sorted(have), flush=True)
