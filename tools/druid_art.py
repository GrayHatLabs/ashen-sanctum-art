"""Art for the Druid class (seventh playable class: plague summoner).

    python tools/druid_art.py portrait   3 full-body class-select figures (flat grey, keyed later) + background
    python tools/druid_art.py sprite     8-direction in-game character
    python tools/druid_art.py anims      walk / cast / summon
    python tools/druid_art.py extras     moss wolf, Thorn Warden
    python tools/druid_art.py review     contact sheet: generated/druid_review.png

Lessons from the other heroes: keep bitforge prompts short and feature-first (long ones lose their ending),
say "full body ... head to boots visible" (the word "portrait" gives busts), and the character endpoint only
draws humanoids (her rats and raven are drawn in code).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
FIGURE = (
    "full body gothic plague druid woman with a crown of black thorn branches like antlers, very long tangled chestnut hair "
    "with ivy, pale freckled skin, yellow-green eyes, black raven feather mantle, dark bark and leather corset, long torn "
    "green and brown skirt turning into roots, holding a twisted thorn staff with a glowing green orb, head to boots visible"
)
SPRITE = (
    "gothic plague druid woman, black thorn antler crown, long tangled chestnut hair with ivy, black feather mantle, dark "
    "leather corset, long torn green and brown skirt, twisted thorn staff with a glowing green orb"
)

ANIMS = [
    ("druid", "walking forward calmly with the thorn staff, skirt trailing", 6),
    ("druid", "raising the thorn staff and casting glowing green plague magic", 6),
    ("druid", "kneeling and pressing one hand to the ground to summon creatures", 6),
]

EXTRAS = [
    ("moss_wolf", "a huge charcoal grey wolf with moss and leaves tangled in its fur and glowing yellow-green eyes", 56, "none", "dog"),
    ("thorn_warden", "a towering humanoid guardian made of dead trees, roots, bones and antlers, an animal skull face swallowed by "
     "bark, a glowing green light in its hollow chest", 88, "heroic", ""),
]
EXTRA_ANIMS = [
    ("moss_wolf", "wolf running fast, loping gallop", 6),
    ("moss_wolf", "wolf lunging forward and biting", 6),
    ("thorn_warden", "tree guardian walking forward heavily", 6),
    ("thorn_warden", "tree guardian smashing down with its root arm", 6),
]


def portrait():
    for tag in "abc":
        out = gen.d_of("druid") / f"full_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": f"{FIGURE}, plain flat grey background, bold clean outlines, cel shading",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "bust, close-up, cropped, oval frame, border, two faces, multiple people, chibi, big head, "
                                    "jeans, modern clothes, nudity, text, watermark, scenery, extra limbs, deformed hands",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"druid full {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "druid.png"
    if not bg.exists():
        body = {
            "description": "the overgrown ruins of a gothic cathedral swallowed by a diseased forest, huge trees through the "
                           "collapsed roof, roots splitting the stone floor, candles among moss and poisonous mushrooms, green "
                           f"mist, ivy-covered statues, a twisted plague tree, background scenery only, no people, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "people, person, character, figure, woman, text, watermark",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if r:
            gen.log_charge("portrait bg druid", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


def sprite():
    if not (gen.GEN / "druid" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "druid", f"{SPRITE}, {HEADS}", 56, "realistic_female", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("druid anims done", flush=True)


def extras():
    import world_art
    for name, desc, size, prop, tmpl in EXTRAS:
        if not (gen.GEN / name / "rotation_urls_south.png").exists():
            act2_art.safe(gen.character, name, desc, size, prop, tmpl)
    for name, action, frames in EXTRA_ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("druid extras done", flush=True)


def review():
    d = gen.GEN / "druid"
    ps = [d / f"full_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "druid.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "druid_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "anims": anims, "extras": extras, "review": review}[sys.argv[1]]()
