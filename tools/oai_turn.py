"""Boss turnarounds by OpenAI (8 directions, idle), sliced to boss-sized pixel art like tools/astronomer_oai.py,
for any boss in DESIGNS.

    python tools/oai_turn.py gen <name>          new sheet -> generated/oai/sprite_<name>_raw_<n>.png (+ preview)
    python tools/oai_turn.py slice <name> <n>    re-slice sheet n
    python tools/oai_turn.py use <name> <n>      install sheet n as generated/boss_<name> (rotations only)
"""
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oai_sprite as os_  # noqa: E402
import gen  # noqa: E402

os_.DESIGNS.update({
    "architect": "a tall gaunt faceless figure in long grey-violet robes made of shifting stone blocks and half-built "
                 "masonry, scaffolding and floating bricks orbiting its shoulders like a crown, a smooth blank stone "
                 "mask for a face with a single glowing gold crack, long thin hands holding a builder's square and a "
                 "plumb line of light. Small realistic head, tall adult proportions",
    "mirrorabbot": "a gaunt fallen monk abbot in tattered dark violet and grey robes, his body cracked like a broken "
                   "mirror with shards of reflective glass embedded in his skin and floating around him, a hood, a "
                   "pale face half covered by a cracked silver mirror mask, a long staff topped with a round hand "
                   "mirror. Small realistic head, adult proportions",
})
H = 96


def pixel(fig):
    k = H / fig.height
    if fig.width * k > 136:
        k = 136 / fig.width
    small = fig.resize((max(1, round(fig.width * k)), max(1, round(fig.height * k))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=40, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = rgb.convert("RGBA")
    out.putalpha(a)
    canvas = Image.new("RGBA", (140, 132), (0, 0, 0, 0))
    canvas.alpha_composite(out, ((140 - out.width) // 2, 126 - out.height))
    return canvas


def _preview(hero, n, sprites):
    sheet = Image.new("RGBA", (144 * len(sprites), 136), (40, 36, 44, 255))
    for i, s in enumerate(sprites):
        sheet.alpha_composite(s, (i * 144 + 2, 2))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os_.OUT / f"sprite_{hero}_dirs_{n}.png")


os_.pixel_sprite = pixel
os_.preview = _preview

if __name__ == "__main__":
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == "gen":
        os_.gen(name)
    elif cmd == "slice":
        os_.do_slice(name, int(sys.argv[3]))
    elif cmd == "use":
        n = int(sys.argv[3])
        src = os_.OUT / f"sprite_{name}_{n}"
        d = gen.GEN / f"boss_{name}"
        if d.exists():
            old = gen.GEN / "_old" / f"boss_{name}_before_{n}"
            old.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(old))
        d.mkdir(parents=True, exist_ok=True)
        for p in src.glob("rotation_urls_*.png"):
            shutil.copy(p, d / p.name)
        # Directions the sheet didn't have: mirror the opposite side.
        from PIL import ImageOps
        pairs = {"south-west": "south-east", "west": "east", "north-west": "north-east",
                 "south-east": "south-west", "east": "west", "north-east": "north-west", "north": "south"}
        for want, have in pairs.items():
            if not (d / f"rotation_urls_{want}.png").exists() and (d / f"rotation_urls_{have}.png").exists():
                ImageOps.mirror(Image.open(d / f"rotation_urls_{have}.png")).save(d / f"rotation_urls_{want}.png")
        (d / "character.json").write_text('{"animations": []}')
        print("installed", name, n)
