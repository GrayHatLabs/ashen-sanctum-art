"""Animation review (the user, 2026-10-06: "run a test that shows me every character's animations").
Reads each hero's packed sheet (sheets/<name>.png, exactly what the game draws) and the layout from the game's
src/art_gen.rs, and writes one animated GIF per hero: a row per animation, a column per direction, each playing
at its in-game speed.

    python tools/anim_review.py [names...]     -> generated/anim_review/<name>.gif  (default: all heroes)
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ART = Path(__file__).resolve().parent.parent
GAME = ART.parent / "AshenSanctum"
OUT = ART / "generated" / "anim_review"
HEROES = ["mage", "vampire", "inventor", "valkyrie", "berserker", "reaper", "druid", "inquisitor_hero"]
DIRS = ["S", "SE", "E", "NE", "N", "NW", "W", "SW"]
TICK_MS = 50
LOOP_TICKS = 60  # 3 seconds


def layout(name):
    src = (GAME / "src" / "art_gen.rs").read_text(encoding="utf8")
    line = next(l for l in src.splitlines() if f'CharDef {{ name: "{name}"' in l)
    cw, ch = map(int, re.search(r"cell: \((\d+), (\d+)\)", line).groups())
    anims = [(n, int(r), int(f), int(fps)) for n, r, f, fps in
             re.findall(r'AnimDef \{ name: "(\w+)", row: (\d+), frames: (\d+), fps: (\d+) \}', line)]
    return cw, ch, anims


def review(name):
    cw, ch, anims = layout(name)
    sheet = Image.open(ART / "sheets" / f"{name}.png").convert("RGBA")
    label_w, head_h, scale = 56, 14, 2
    W = label_w + cw * 8
    H = head_h + ch * len(anims)
    frames = []
    for t in range(LOOP_TICKS):
        img = Image.new("RGBA", (W, H), (34, 30, 38, 255))
        d = ImageDraw.Draw(img)
        for k, dn in enumerate(DIRS):
            d.text((label_w + k * cw + cw // 2 - 6, 2), dn, fill=(200, 180, 140))
        for r, (an, row, nf, fps) in enumerate(anims):
            d.text((4, head_h + r * ch + ch // 2 - 6), an, fill=(230, 200, 140))
            i = int(t * TICK_MS / 1000 * fps) % nf
            for k in range(8):
                cell = sheet.crop((i * cw, (row + k) * ch, (i + 1) * cw, (row + k + 1) * ch))
                img.alpha_composite(cell, (label_w + k * cw, head_h + r * ch))
        frames.append(img.resize((W * scale, H * scale), Image.NEAREST).convert("P", palette=Image.ADAPTIVE, colors=255))
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{name}.gif"
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=TICK_MS, loop=0, disposal=2)
    print("saved", out, f"{len(anims)} animations")


if __name__ == "__main__":
    for n in sys.argv[1:] or HEROES:
        review(n)
