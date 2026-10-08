"""Old Barnacle, the Pearl Grotto's boss (Act 5, 2026-10-08): an OpenAI turnaround (8 directions, idle) sliced to
boss-sized pixel art, like tools/junkgolem_oai.py. Before this the game drew a scaled, tinted shellguard.

    python tools/barnacle_oai.py gen        new sheet -> generated/oai/sprite_barnacle_raw_<n>.png (+ preview)
    python tools/barnacle_oai.py slice <n>  re-slice sheet n
    python tools/barnacle_oai.py use <n>    install sheet n as generated/boss_barnacle (rotations only)
"""
import sys
import shutil
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

os_.DESIGNS["barnacle"] = (
    "a gigantic ancient crab monster, as big as a cottage, standing on six thick armored crab legs: a huge domed shell "
    "crusted with grey-white barnacles, pale pink coral, dark green seaweed and old rusty sword blades stuck in it, one "
    "enormous crushing claw and one smaller claw, both raised, small black eyes on stalks, dark blue-grey and dirty "
    "orange-brown shell, a few glowing pearls caught in the barnacles. It is a crab monster, not a person, no human parts"
)
H = 84


def pixel(fig):
    k = H / fig.height
    w = round(fig.width * k)
    if w > 136:
        k = 136 / fig.width
    small = fig.resize((max(1, round(fig.width * k)), max(1, round(fig.height * k))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=40, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    canvas = Image.new("RGBA", (140, 132), (0, 0, 0, 0))
    canvas.alpha_composite(out, ((140 - out.width) // 2, 126 - out.height))
    return canvas


os_.pixel_sprite = pixel


def _preview(hero, n, sprites):
    sheet = Image.new("RGBA", (144 * len(sprites), 136), (40, 36, 44, 255))
    for i, s in enumerate(sprites):
        sheet.alpha_composite(s, (i * 144 + 2, 2))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os_.OUT / f"sprite_{hero}_dirs_{n}.png")


os_.preview = _preview

if __name__ == "__main__":
    if sys.argv[1] == "gen":
        os_.gen("barnacle")
    elif sys.argv[1] == "slice":
        # Sheet 0 came with 5 views and a sand puddle under each: drop the sand, mirror for the missing views.
        from PIL import ImageOps
        n = int(sys.argv[2])
        figs = os_.slice_sheet(Image.open(os_.OUT / f"sprite_barnacle_raw_{n}.png"))

        def clean(f):
            px = f.load()
            for y in range(int(f.height * 0.6), f.height):
                for x in range(f.width):
                    r, g, b, al = px[x, y]
                    if al and abs(r - g) < 34 and b < g and r > 110:
                        px[x, y] = (0, 0, 0, 0)
            return f.crop(f.getchannel("A").point(lambda v: 255 if v > 100 else 0).getbbox())

        figs = [clean(f) for f in figs]
        m = ImageOps.mirror
        views = {"south": figs[2], "south-west": figs[0], "south-east": m(figs[0]), "west": figs[1], "east": m(figs[1]),
                 "north": figs[3], "north-east": figs[4], "north-west": m(figs[4])}
        d = os_.OUT / f"sprite_barnacle_{n}"
        d.mkdir(parents=True, exist_ok=True)
        sprites = []
        for name in os_.DIRS:
            s_ = pixel(views[name])
            s_.save(d / f"rotation_urls_{name}.png")
            sprites.append(s_)
        _preview("barnacle", n, sprites)
        print("sliced", n)
    elif sys.argv[1] == "use":
        n = int(sys.argv[2])
        src = os_.OUT / f"sprite_barnacle_{n}"
        d = gen.GEN / "boss_barnacle"
        if d.exists():
            old = gen.GEN / "_old" / f"barnacle_before_{n}"
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(old))
        d.mkdir(parents=True, exist_ok=True)
        for p in src.glob("rotation_urls_*.png"):
            shutil.copy(p, d / p.name)
        (d / "character.json").write_text('{"animations": []}')
        print("installed", n)
