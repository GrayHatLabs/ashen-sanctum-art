"""The Sky Pirate's sprite hair, matched to her portrait (the user, 2026-10-06): PixelLab drew it pale cream-blonde;
the portrait's is darker honey and ash-blonde. Hair pixels (warm, red ~ green > blue, unlike the cool white blouse
or the redder skin) are darkened and warmed. pack.py runs fix_frame on every "inventor" frame.

    python tools/pirate_hair.py     preview: generated/pirate_hair_preview.png
"""
from pathlib import Path

from PIL import Image

GEN = Path(__file__).resolve().parent.parent / "generated"


def is_hair(p):
    r, g, b, a = p
    return a > 0 and r - g < 30 and g - b > 8 and 18 <= r - b <= 95 and r > 110


def fix_frame(im):
    im = im.convert("RGBA").copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if is_hair(p):
                px[x, y] = (int(p[0] * 0.80), int(p[1] * 0.68), int(p[2] * 0.52), p[3])
    return im


if __name__ == "__main__":
    dirs = ["south", "south-east", "east", "north-east", "north"]
    ims = [Image.open(GEN / "inventor" / f"rotation_urls_{d}.png").convert("RGBA") for d in dirs]
    sheet = Image.new("RGBA", (72 * len(ims), 144), (40, 36, 44, 255))
    for i, im in enumerate(ims):
        sheet.alpha_composite(im, (i * 72, 0))
        sheet.alpha_composite(fix_frame(im), (i * 72, 72))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(GEN / "pirate_hair_preview.png")
    print("saved", GEN / "pirate_hair_preview.png")
