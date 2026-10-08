"""The Junk Golem (user's choice, 2026-10-08): an OpenAI turnaround sheet (8 directions, idle), sliced to pixel
art like tools/oai_sprite.py but boss-sized. The character generator made sleek robots twice and bitforge a rock golem
(all kept: _old/junkgolem_take1, boss_junkgolem2, _old/junkgolem_bitforge).

    python tools/junkgolem_oai.py gen      new sheet -> generated/oai/sprite_junkgolem_raw_<n>.png (+ preview)
    python tools/junkgolem_oai.py use <n>  install sheet n as generated/boss_junkgolem (rotations only)
"""
import sys
import shutil
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

os_.DESIGNS["junkgolem"] = (
    "a huge hulking golem built from a heap of rusty scrap metal junk: a dented old riveted boiler for a chest glowing orange "
    "through its cracks, bent pipes and chains for arms ending in two huge mismatched iron fists, broken gears, cog wheels, "
    "springs and a crooked chimney stuck all over its shoulders and back, rust-brown, dirty iron grey and copper, lopsided and "
    "crude, stumpy legs of piled scrap. It is a monster, not a person, not a robot, not sleek"
)
H = 104


def pixel(fig):
    k = H / fig.height
    small = fig.resize((max(1, round(fig.width * k)), H), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=40, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    canvas = Image.new("RGBA", (140, 132), (0, 0, 0, 0))
    canvas.alpha_composite(out, ((140 - out.width) // 2, 126 - out.height))
    return canvas


os_.pixel_sprite = pixel

if __name__ == "__main__":
    if sys.argv[1] == "gen":
        os_.gen("junkgolem")
    elif sys.argv[1] == "slice2":
        # This sheet came as two rows of five (the first of each row cut off at the edge): pick the views by hand.
        from PIL import ImageOps
        n = int(sys.argv[2])
        im = Image.open(os_.OUT / f"sprite_junkgolem_raw_{n}.png").convert("RGBA")
        a = im.getchannel("A")
        figs = []
        for y0, y1 in [(0, 512), (512, 1024)]:
            band = a.crop((0, y0, im.width, y1))
            cols = [band.crop((x, 0, x + 1, y1 - y0)).getextrema()[1] for x in range(im.width)]
            spans, inside, s0 = [], False, 0
            for x, v in enumerate(cols):
                if v > 20 and not inside:
                    s0, inside = x, True
                if v <= 20 and inside:
                    spans.append((s0, x))
                    inside = False
            if inside:
                spans.append((s0, im.width))
            figs += [im.crop((x0, y0, x1, y1)) for x0, x1 in spans if x1 - x0 > 40]

        def clean(f):
            f = f.crop(f.getbbox())
            px = f.load()
            for y in range(int(f.height * 0.82), f.height):
                for x in range(f.width):
                    r, g, b, al = px[x, y]
                    if al and r > 90 and g > 0.7 * r and b < 0.5 * g:
                        px[x, y] = (0, 0, 0, 0)
            return f.crop(f.getbbox())

        pick = {"south": 1, "south-east": 2, "north-east": 3, "east": 4, "north": 7, "north-west": 8, "west": 9}
        d = os_.OUT / f"sprite_junkgolem_{n}"
        d.mkdir(parents=True, exist_ok=True)
        sprites = []
        for name in os_.DIRS:
            f = clean(figs[pick[name]]) if name in pick else ImageOps.mirror(clean(figs[2]))
            s_ = pixel(f)
            s_.save(d / f"rotation_urls_{name}.png")
            sprites.append(s_)
        sheet = Image.new("RGBA", (144 * 8, 136), (40, 36, 44, 255))
        for i, s_ in enumerate(sprites):
            sheet.alpha_composite(s_, (i * 144 + 2, 2))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os_.OUT / f"sprite_junkgolem_dirs_{n}.png")
        print("sliced", n)
    elif sys.argv[1] == "use":
        n = int(sys.argv[2])
        src = os_.OUT / f"sprite_junkgolem_{n}"
        d = gen.GEN / "boss_junkgolem"
        old = gen.GEN / "_old" / "junkgolem_bitforge"
        if d.exists() and not old.exists():
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(old))
        d.mkdir(parents=True, exist_ok=True)
        for p in src.glob("rotation_urls_*.png"):
            shutil.copy(p, d / p.name)
        (d / "character.json").write_text('{"animations": []}')
        print("installed", n)
