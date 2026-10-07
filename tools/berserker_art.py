"""Concept art for the Berserker class (fifth playable class, two-handed axe + dire wolf).

    python tools/berserker_art.py portrait   3 class-select portrait variants (figure on flat grey, keyed later) + background
    python tools/berserker_art.py sprite     8-direction in-game character
    python tools/berserker_art.py anims      walk / cleave / chop / whirl / throw / shout
    python tools/berserker_art.py extras     the dire wolf (run, bite, howl)
    python tools/berserker_art.py review     contact sheet: generated/berserker_review.png

Palette from the user: blackened iron, dark leather, charcoal, wolf-fur grey, earthy brown, muted bronze,
subtle dried-crimson accents. No glowing magic.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
PALETTE = "blackened iron, dark leather, charcoal, wolf-fur grey, earthy brown, muted bronze, subtle dried-crimson accents, no glowing magic"
LOOK = (
    "tall muscular gothic barbarian berserker queen, battle-scarred, dangerous half-smile, very long wild ash-brown hair "
    "with thick nordic braids, bronze rings, black feathers and animal teeth, pale weathered skin with small scars, "
    "amber-gold eyes, smoky black eye makeup, black war paint down one eye, brown-black lips, black nordic tattoos on her "
    "shoulders and arms, brutal hammered iron crown of broken spearheads, scratched black leather battle corset reinforced "
    "with blackened iron plates and big buckles, massive charcoal and brown wolf-fur mantle with an iron clasp, bare "
    "muscular arms with leather bracers and scavenged iron, skirt of black leather strips, charcoal cloth, hides and fur, "
    "belts with chains, throwing knives and a skull, huge knee-high brown leather boots with iron plates and wolf fur"
)
AXE = "a gigantic two-handed executioner's battle axe with a chipped dark iron head and rough runes, fur-wrapped haft"
SPRITE = (
    "muscular barbarian berserker woman, long wild ash-brown braided hair, iron spike crown, black leather and iron corset, "
    f"big wolf-fur mantle, bare muscular arms, leather and fur skirt, knee-high fur boots, carrying {AXE} over one shoulder, {PALETTE}"
)

ANIMS = [
    ("berserker", "striding forward with the giant axe over her shoulder", 6),
    ("berserker", "swinging the giant axe in a wide horizontal cleave", 6),
    ("berserker", "raising the giant axe high and chopping straight down", 6),
    ("berserker", "spinning around in a full circle with the axe held out", 6),
    ("berserker", "hurling the giant axe forward with both hands", 6),
    ("berserker", "throwing her head back and roaring a war cry, axe raised", 6),
]

EXTRAS = [
    ("dire_wolf", "a huge scarred black dire wolf with a rough leather collar decorated with iron rings and broken armor, amber eyes", 56, "none", "dog"),
]
EXTRA_ANIMS = [
    ("dire_wolf", "dire wolf running fast, loping gallop", 6),
    ("dire_wolf", "dire wolf lunging forward and biting", 6),
    ("dire_wolf", "dire wolf raising its head and howling", 6),
]


def portrait():
    for tag in "abc":
        out = gen.d_of("berserker") / f"portrait_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": (
                f"cartoon character design portrait of one {LOOK}, standing triumphantly in a three-quarter pose with {AXE} "
                "resting across one shoulder, a huge scarred black dire wolf with an iron-ringed collar at her side, "
                f"{PALETTE}, plain flat grey background, bold clean outlines, cel shading, anatomically correct, "
                "exactly two arms, exactly two legs, five fingers"
            ),
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "glowing magic, text, watermark, multiple people, chibi, big head, nudity, exposed chest, "
                                    "extra limbs, extra arms, extra legs, duplicated limbs, deformed hands, scenery",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"berserker portrait {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved portrait", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "berserker.png"
    if not bg.exists():
        body = {
            "description": "a chaotic ruined muddy battlefield, broken shields and shattered weapons, torn black banners, burning "
                           "wooden fortifications and smoke from burning siege engines, storm clouds, distant snow-covered mountains, "
                           f"patches of melting snow, background scenery only, no people, portrait orientation, {gen.STYLE}",
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
            gen.log_charge("portrait bg berserker", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


# v2 (the user, 2026-10-06: "sometimes she has two weapons"). The long haft passed behind her on the diagonals
# with a head showing at each end. One single-bladed axe, held in front of her, short enough to stay in view.
# v3 (the user: "bring back her fur"): v2 lost the fur mantle and crown. Feature-first: fur and crown lead.
SPRITE_V3 = (
    "barbarian berserker woman with a huge shaggy grey wolf-fur mantle over both shoulders and a wolf-pelt cloak, a jagged "
    "iron spike crown, long wild ash-brown braided hair, bare muscular arms, black leather and iron corset, fur skirt, fur "
    "boots, holding ONE single-bladed battle axe in her right hand in front of her, a single axe head on top of the haft"
)
SPRITE_V2 = (
    "muscular barbarian berserker woman, long wild ash-brown braided hair, iron spike crown, black leather and iron corset, "
    "big wolf-fur mantle, bare muscular arms, leather and fur skirt, knee-high fur boots, holding ONE big single-bladed "
    "battle axe in her right hand in front of her body, a single axe head on top of the haft, the haft does not pass behind "
    f"her, {PALETTE}"
)
ANIMS_V2 = [
    ("berserker", "walking forward with heavy strides, holding the one axe in her right hand in front of her exactly as in "
                  "her standing pose, legs stepping", 6),
    ("berserker", "swinging the single axe in a wide horizontal cleave", 6),
    ("berserker", "raising the single axe high and chopping straight down", 6),
    ("berserker", "spinning around in a full circle with the single axe held out", 6),
    ("berserker", "hurling the single axe forward with both hands", 6),
    ("berserker", "throwing her head back and roaring a war cry, the single axe raised", 6),
]


def sprite_v2():
    if not (gen.GEN / "berserker" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "berserker", f"{SPRITE_V2}, {HEADS}", 56, "heroic", "")
    print("sprite v2 done", flush=True)


def sprite_v3():
    if not (gen.GEN / "berserker" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "berserker", f"{SPRITE_V3}, {HEADS}", 56, "heroic", "")
    print("sprite v3 done", flush=True)


def anims_v2():
    import world_art
    for name, action, frames in ANIMS_V2:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("berserker v2 anims done", flush=True)


def sprite():
    if not (gen.GEN / "berserker" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "berserker", f"{SPRITE}, {HEADS}", 56, "heroic", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("berserker anims done", flush=True)


def extras():
    import world_art
    for name, desc, size, prop, tmpl in EXTRAS:
        if not (gen.GEN / name / "rotation_urls_south.png").exists():
            act2_art.safe(gen.character, name, desc, size, prop, tmpl)
    for name, action, frames in EXTRA_ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("berserker extras done", flush=True)


def review():
    d = gen.GEN / "berserker"
    ps = [d / f"portrait_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "berserker.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "berserker_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "anims": anims, "extras": extras, "review": review,
     "all": lambda: (portrait(), sprite(), anims(), extras()), "sprite2": sprite_v2, "anims2": anims_v2, "sprite3": sprite_v3}[sys.argv[1]]()
