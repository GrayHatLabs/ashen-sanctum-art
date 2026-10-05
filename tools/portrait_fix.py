"""Cleans up the class-select portraits (hands, duplicated limbs) by redrawing each original
with bitforge, using the original as the init image so the composition stays.

The untouched originals are kept in reference/portraits_original/.

    python tools/portrait_fix.py            two variants per portrait -> generated/portrait_fix/
    python tools/portrait_fix.py review     side-by-side sheet: generated/portrait_fix/review.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import pixellab  # noqa: E402

REF = Path(__file__).resolve().parent.parent / "reference" / "portraits_original"
OUT = gen.GEN / "portrait_fix"
ANATOMY = "anatomically correct, exactly two arms, exactly two hands with five fingers, exactly two legs, clean hands"
NEGATIVE = "extra hands, extra fingers, extra arms, extra legs, duplicated limbs, floating hands, deformed hands, text, watermark, nudity, chibi, big head"

PORTRAITS = {
    "vampire": (
        "vampire_portrait.png",
        "glamorous goth vampire woman in a plum velvet gown in front of a moonlit gothic castle, long black hair, pale skin, "
        "one hand resting on her hip, the other hand at her side holding the gown",
    ),
    "sorceress": (
        "sorceress_portrait.png",
        "fire sorceress in a long red hooded robe with gold trim, holding a wooden staff with a burning ember in her right hand, "
        "her left hand open with a small flame above the palm, plain grey background",
    ),
    "inventor": (
        "inventor_portrait.png",
        "steampunk goth woman inventor with dark auburn curls and a small tilted top hat with brass goggles, brown corset dress "
        "with a leg slit, black lace-up boots, one brass clockwork mechanical arm holding an ornate brass ray pistol, "
        "hand on hip, standing on two legs, plain grey background",
    ),
}


def fix(name, src, desc, strength):
    body = {
        "description": f"{desc}, {ANATOMY}, cel shading, bold outlines, {gen.STYLE}",
        "image_size": {"width": 140, "height": 200},
        "no_background": False,
        "outline": "single color black outline",
        "shading": "flat shading",
        "detail": "highly detailed",
        "view": "side",
        "init_image": pixellab.b64img(REF / src),
        "init_image_strength": int(strength),
        "negative_description": NEGATIVE,
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge(f"portrait fix {name} {strength}", r.get("usage"))
    OUT.mkdir(parents=True, exist_ok=True)
    gen.save_b64(r["image"], OUT / f"{name}_s{strength}.png")
    print("saved", name, strength, flush=True)


def review():
    from PIL import Image
    rows = []
    for name, (src, _) in PORTRAITS.items():
        ims = [Image.open(REF / src).convert("RGBA")] + [Image.open(p).convert("RGBA") for p in sorted(OUT.glob(f"{name}_s*.png"))]
        w = sum(i.width for i in ims) + 8 * len(ims)
        row = Image.new("RGBA", (w, 200), (40, 36, 44, 255))
        x = 0
        for i in ims:
            row.alpha_composite(i, (x, 0))
            x += i.width + 8
        rows.append(row)
    sheet = Image.new("RGBA", (max(r.width for r in rows), 208 * len(rows)), (40, 36, 44, 255))
    for k, r in enumerate(rows):
        sheet.alpha_composite(r, (0, k * 208))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(OUT / "review.png")
    print("saved", OUT / "review.png")


if __name__ == "__main__":
    if sys.argv[1:] == ["review"]:
        review()
    else:
        for name, (src, desc) in PORTRAITS.items():
            for strength in (300, 200):
                gen.call  # noqa: B018 (keeps the import obviously used)
                try:
                    fix(name, src, desc, strength)
                except Exception as e:  # noqa: BLE001
                    print("FAILED", name, strength, str(e)[:200], flush=True)
