"""Art for the Inquisitor (eighth playable class: chained-censer hunter of the cursed).

    python tools/inquisitor_art.py portrait   3 full-body class-select figures (flat grey, keyed later) + background
    python tools/inquisitor_art.py sprite     8-direction in-game character
    python tools/inquisitor_art.py anims      walk / attack (flail swing) / cast (brand) / spin (censer sweep)
    python tools/inquisitor_art.py review     contact sheet: generated/inquisitor_review.png

Lessons from the other heroes: keep bitforge prompts short and feature-first (long ones lose their ending),
say "full body ... head to boots visible" (the word "portrait" gives busts). Style rules: small heads,
realistic adult proportions, never chibi.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
# v2 (the user's reference sheet, 2026-10-06): more iron and chains, leather armor, a spiky halo.
FIGURE = (
    "full body gothic inquisitor woman, black hood, tall spiked golden halo of sharp rays behind her head, iron chains "
    "wrapped across her body, black leather corset with iron buckles, holding out a brass censer hanging on long chains "
    "glowing with fire, tattered black ivory and crimson robes, thigh-high black leather boots, pale blonde hair, "
    "head to boots visible"
)
SPRITE = (
    "gothic inquisitor woman, black hood, big spiked gold halo of sharp rays, black leather armor with iron buckles, "
    "iron chains wrapped around her, tattered black and crimson robe, a brass censer hanging on a long chain glowing orange"
)

ANIMS = [
    ("inquisitor_hero", "walking forward, censer on its chain swinging at her side", 6),
    ("inquisitor_hero", "swinging the spiked censer on its long chain forward like a flail", 6),
    ("inquisitor_hero", "pointing one hand forward to burn a glowing sigil, censer hanging", 6),
    ("inquisitor_hero", "spinning in place swinging the censer on its chain around her body", 6),
]


# v3 (the user, 2026-10-06: "a walking gown like the image instead of the leather pants"): the robed look of
# her OpenAI portrait and sprite test. The halo is still painted on by tools/inquisitor_halo.py.
SPRITE_V3 = (
    "tall slender gothic inquisitor woman in a long flowing black hooded gown that reaches the ground, pale face, ash-blonde "
    "hair under the hood, gold chains crossed over her chest and wrapped around her waist, a golden spiked halo behind her "
    "head, holding a golden censer hanging on a chain glowing with holy fire, no trousers, no armor plates"
)
ANIMS_V3 = [
    ("inquisitor_hero", "walking forward, long gown swaying with each step, feet stepping out under the hem, censer swinging", 6),
    ("inquisitor_hero", "swinging the golden censer on its long chain forward like a flail", 6),
    ("inquisitor_hero", "pointing one hand forward to burn a glowing sigil, censer hanging", 6),
    ("inquisitor_hero", "spinning in place swinging the censer on its chain around her body, gown flaring", 6),
]


def sprite_v3():
    if not (gen.GEN / "inquisitor_hero" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "inquisitor_hero", f"{SPRITE_V3}, {HEADS}", 56, "realistic_female", "")
    print("sprite v3 done", flush=True)


def anims_v3():
    import world_art
    for name, action, frames in ANIMS_V3:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("inquisitor v3 anims done", flush=True)


def portrait():
    d = gen.d_of("inquisitor_hero")
    for tag in "abc":
        out = d / f"full_{tag}.png"
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
        gen.log_charge(f"inquisitor full {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "inquisitor.png"
    if not bg.exists():
        body = {
            "description": "an empty ruined gothic cathedral interior at night, hundreds of lit candles, a black altar, a great "
                           "stained glass window with a burning sword, hanging iron chains and cages, incense smoke, "
                           f"empty floor, background scenery only, no people, {gen.STYLE}",
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
            gen.log_charge("portrait bg inquisitor", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


def sprite():
    if not (gen.GEN / "inquisitor_hero" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "inquisitor_hero", f"{SPRITE}, {HEADS}", 56, "realistic_female", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("inquisitor anims done", flush=True)


# Take 2 of the walk (the user: "her legs just float, she doesn't walk" walking down the screen): the long
# coat hid the legs, so ask for clear strides with the coat parting.
WALK2 = ("inquisitor_hero", "walking forward with long clear strides, legs stepping one after the other, long coat parting "
         "around her moving legs, censer swinging at her side", 6)


def walk2():
    import world_art
    act2_art.safe(world_art.run_anim, *WALK2)
    print("walk2 done", flush=True)


def review():
    d = gen.GEN / "inquisitor_hero"
    ps = [d / f"full_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "inquisitor.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "inquisitor_review.png", *[p for p in ps if p.exists()])


# The whip (the user, 2026-10-06: "longer, more of a whipping action"; docs/INQUISITOR_WHIP_PLAN.md in the game repo).
WHIP_ATTACK = ("inquisitor_hero", "drawing her arm back over her shoulder then lashing it far forward with the whole arm "
               "fully extended, cracking the censer on its chain out ahead of her like a whip, gown flaring", 6)


# Take 2: take 1 flung the chain behind her in some directions. Keep the censer in the hand that holds it standing.
WHIP_ATTACK2 = ("inquisitor_hero", "whipping attack toward the direction she faces: her censer arm swings up over her head, "
                "then lashes straight out in front of her, arm fully extended forward, the golden censer flying far ahead "
                "on its taut chain, body leaning into the strike, nothing behind her", 6)


def whip_attack():
    import world_art
    act2_art.safe(world_art.run_anim, *(WHIP_ATTACK2 if sys.argv[2:] == ["2"] else WHIP_ATTACK))


if __name__ == "__main__":
    {"whip": whip_attack, "portrait": portrait, "sprite": sprite, "anims": anims, "review": review, "walk2": walk2, "sprite3": sprite_v3, "anims3": anims_v3}[sys.argv[1]]()
