"""The Astronomer, the Fallen Observatory's boss (Act 6, 2026-10-08): an OpenAI turnaround (8 directions, idle) sliced to
boss-sized pixel art, like tools/junkgolem_oai.py. Before this the game drew a scaled, tinted fallen seraph.

    python tools/astronomer_oai.py gen        new sheet -> generated/oai/sprite_astronomer_raw_<n>.png (+ preview)
    python tools/astronomer_oai.py slice <n>  re-slice sheet n
    python tools/astronomer_oai.py use <n>    install sheet n as generated/boss_astronomer (rotations only)
"""
import sys
import shutil
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

os_.DESIGNS["astronomer"] = (
    "a tall fallen angel astronomer, a gaunt seraph with long silver-white hair and a pale stern face, six tattered "
    "grey-gold feathered wings, a long midnight-blue robe embroidered with golden constellations and star-charts, a "
    "brass armillary sphere orbiting one raised hand, a glowing golden astrolabe staff in the other, small stars and "
    "glowing points of light circling him. Small realistic head, tall adult proportions")
H = 96


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
        os_.gen("astronomer")
    elif sys.argv[1] == "slice":
        # Sheet 0: five views, two of them touching (split by hand at x=1051); mirrors fill in the rest.
        from PIL import ImageOps
        n = int(sys.argv[2])
        im = Image.open(os_.OUT / f"sprite_astronomer_raw_{n}.png").convert("RGBA")
        spans = [(0, 284), (291, 651), (682, 1051), (1062, 1249), (1262, 1531)]

        def cut(x0, x1):
            f = im.crop((x0, 0, x1, im.height))
            return f.crop(f.getchannel("A").point(lambda v: 255 if v > 100 else 0).getbbox())

        figs = [cut(*sp) for sp in spans]
        m = ImageOps.mirror
        views = {"south": figs[0], "south-east": figs[1], "north-east": figs[2], "north": figs[3], "east": figs[4],
                 "south-west": m(figs[1]), "west": m(figs[4]), "north-west": m(figs[2])}
        d = os_.OUT / f"sprite_astronomer_{n}"
        d.mkdir(parents=True, exist_ok=True)
        sprites = []
        for name in os_.DIRS:
            s_ = pixel(views[name])
            s_.save(d / f"rotation_urls_{name}.png")
            sprites.append(s_)
        _preview("astronomer", n, sprites)
        print("sliced", n)
    elif sys.argv[1] == "use":
        n = int(sys.argv[2])
        src = os_.OUT / f"sprite_astronomer_{n}"
        d = gen.GEN / "boss_astronomer"
        if d.exists():
            old = gen.GEN / "_old" / f"astronomer_before_{n}"
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(old))
        d.mkdir(parents=True, exist_ok=True)
        for p in src.glob("rotation_urls_*.png"):
            shutil.copy(p, d / p.name)
        (d / "character.json").write_text('{"animations": []}')
        print("installed", n)
