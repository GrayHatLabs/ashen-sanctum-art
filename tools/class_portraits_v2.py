"""Second pass at the class-select figures for the Valkyrie, Berserker and Reaper.

The first pass ("cartoon character design portrait ...") came back as head-and-shoulder busts in
oval frames, doubled faces, a bearded man, and bikinis instead of armor. This asks for full-body
concept art on flat grey (keyed out by pack.py and composited on the class backgrounds).

    python tools/class_portraits_v2.py [valkyrie|berserker|reaper ...]   -> generated/<class>/full_{d,e,f}.png
    python tools/class_portraits_v2.py review                            -> generated/class_portraits_v2.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402
import valkyrie_art  # noqa: E402
import berserker_art  # noqa: E402
import reaper_art  # noqa: E402

# Short, feature-first prompts: bitforge seems to drop the end of long descriptions (the first try,
# with a long full-body preamble, came back as generic women in jeans).
NEG_ALL = ("bust, close-up, cropped, oval frame, border, two faces, multiple people, chibi, big head, jeans, modern clothes, "
           "text, watermark, scenery, extra limbs, deformed hands")

CLASSES = {
    "valkyrie": (
        "full body dark nordic frost valkyrie woman holding a long ice-bladed rune spear upright, silver crown, very long "
        "black hair with silver-blue tips, blackened steel breastplate with glowing blue runes, black fur mantle, layered black "
        "and midnight blue battle skirt, tall steel boots, frost magic in her other hand, head to boots visible",
        "red, crimson, nudity, " + NEG_ALL,
    ),
    "berserker": (
        "full body muscular barbarian warrior queen with a huge two-handed battle axe on her shoulder, iron spike crown, long "
        "wild brown braided hair, war paint, black leather and iron plate corset armor, big grey wolf-fur mantle, leather "
        "bracers, fur and leather skirt, knee-high fur boots, head to boots visible",
        "bikini, bra, exposed belly, nudity, man, male, beard, sword, " + NEG_ALL,
    ),
    "reaper": (
        "full body gothic reaper woman holding a huge rune scythe with a small blue spirit lantern under the blade, deep black "
        "hood, long black cloak trailing smoke, very long silver-grey hair, pale face, amber eyes, black corset, long black "
        "skirt, keys and hourglasses on her belt, a floating chained black book beside her, head to boots visible",
        "red, gore, skeleton, nudity, " + NEG_ALL,
    ),
}


def make(name):
    desc, neg = CLASSES[name]
    for tag in "ghi":
        out = gen.d_of(name) / f"full_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": f"{desc}, plain flat grey background, bold clean outlines, cel shading",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": neg,
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"{name} full {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", name, tag, flush=True)


def review():
    ps = [gen.GEN / n / f"full_{t}.png" for n in CLASSES for t in "ghi"]
    gen.review(gen.GEN / "class_portraits_v2.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    args = sys.argv[1:] or list(CLASSES)
    if args == ["review"]:
        review()
    else:
        for a in args:
            make(a)
        review()
