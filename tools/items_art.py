"""Inventory icons for equipment (bitforge, side view, transparent background).

    python tools/items_art.py          # generate every missing icon (1 generation each)
    python tools/items_art.py review   # contact sheet: generated/icons_review.png

pack.py scales them to ICON_SIZE for the inventory grid; the game draws them smaller on the floor.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402

ICON = "single game inventory item icon, centered, no background"
ICONS = [
    ("icon_staff_gnarled", "a gnarled crooked wooden mage staff, long diagonal"),
    ("icon_staff_ash", "a smooth pale ashwood mage staff with an iron cap, long diagonal"),
    ("icon_staff_runed", "a dark wooden mage staff carved with glowing orange runes, long diagonal"),
    ("icon_staff_ember", "a blackened mage staff topped with a burning red ember crystal, long diagonal"),
    ("icon_helm_hood", "an empty brown cloth hood, clothing item only, no face"),
    ("icon_helm_circlet", "a thin silver tiara circlet headband seen from the front, a small red gem in the middle, jewelry"),
    ("icon_helm_horned", "an empty dark iron helmet with two small curved horns, no face"),
    ("icon_helm_crown", "a jagged blackened iron crown glowing with embers"),
    ("icon_armor_robe", "an empty dark red mage robe with gold trim laid flat, clothing item only, no body"),
    ("icon_armor_leather", "an empty brown studded leather armor vest, clothing item only, no body"),
    ("icon_armor_chain", "an empty grey chain mail shirt laid flat, armor item only, no body"),
    ("icon_gloves_cloth", "a pair of empty dark cloth gloves, no hands"),
    ("icon_gloves_leather", "one empty brown leather glove with fingers, armored gauntlet, no hand inside"),
    ("icon_boots_cloth", "a pair of soft brown traveller boots"),
    ("icon_boots_heavy", "a pair of heavy iron-shod boots"),
    ("icon_belt_sash", "a coiled red cloth sash belt"),
    ("icon_belt_leather", "a coiled brown leather belt strap with a square bronze buckle"),
    ("icon_ring", "a single gold ring with a red gem"),
    ("icon_amulet", "a bronze amulet pendant on a chain with an orange gem"),
    # Gems (the game scales them by grade).
    ("icon_gem_ruby", "one loose faceted cut red ruby gemstone on its own, no handle, no stick, sparkling"),
    ("icon_gem_sapphire", "one faceted cut deep blue sapphire gemstone, sparkling"),
    ("icon_gem_topaz", "one faceted cut golden yellow topaz gemstone, sparkling"),
    ("icon_gem_emerald", "one faceted cut green emerald gemstone, sparkling"),
    ("icon_gem_amethyst", "one faceted cut purple amethyst gemstone, sparkling"),
    ("icon_gem_diamond", "one faceted cut clear white diamond gemstone, sparkling"),
    ("icon_gem_skull", "one tiny polished ivory human skull carved like a jewel"),
]


def icon(name, desc):
    body = {
        "description": f"{desc}, {ICON}, {gen.STYLE}",
        "image_size": {"width": 32, "height": 32},
        "no_background": True,
        "outline": "single color black outline",
        "shading": "medium shading",
        "detail": "medium detail",
        "view": "side",
        "negative_description": "text, character, person, hand, background, floor, shadow, multiple items",
    }
    r = gen.call("POST", "/create-image-bitforge", body)
    gen.log_charge(f"{name} icon", r.get("usage"))
    gen.save_b64(r["image"], gen.d_of(name) / "image.png")
    print("saved", name, flush=True)


def main():
    if sys.argv[1:] == ["review"]:
        gen.review(gen.GEN / "icons_review.png", *[gen.GEN / n / "image.png" for n, _ in ICONS if (gen.GEN / n / "image.png").exists()])
        return
    for name, desc in ICONS:
        if (gen.GEN / name / "image.png").exists():
            continue
        for k in range(4):
            try:
                icon(name, desc)
                break
            except (RuntimeError, SystemExit) as e:
                print("retry", name, k, str(e)[:120], flush=True)
                time.sleep(30 * (k + 1))


if __name__ == "__main__":
    main()
