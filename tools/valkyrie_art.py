"""Concept art for the Valkyrie class (fourth playable class, frost spear melee).

    python tools/valkyrie_art.py portrait   3 class-select portrait variants (figure on flat grey, keyed later) + background
    python tools/valkyrie_art.py sprite     8-direction in-game character
    python tools/valkyrie_art.py anims      walk / thrust / sweep / whirl / throw / cast
    python tools/valkyrie_art.py extras     frost raven, warhorse charge, einherjar
    python tools/valkyrie_art.py review     contact sheet: generated/valkyrie_review.png

Palette rule from the user: blackened steel, charcoal, silver, glacier blue, midnight blue; absolutely no red.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen  # noqa: E402
import act2_art  # noqa: E402

HEADS = "small head, realistic adult body proportions, long legs"
NO_RED = "absolutely no red, blackened steel, charcoal, silver, glacier blue and midnight blue palette"
LOOK = (
    "glamorous dark nordic frost valkyrie warrior queen, very long ash-black hair fading to icy silver-blue at the ends "
    "with nordic braids, raven feathers and blue crystals, pale skin, glowing glacier-blue eyes, charcoal war paint, "
    "smoky winged eyeliner, dark blue-black lips, jagged silver crown of frozen branches and runes with ice shards, "
    "blackened-steel breastplate and corset engraved with glowing icy-blue runes and silver knotwork, heavy black fur "
    "mantle over one shoulder with frosted raven feathers, layered battle skirt of torn black leather, charcoal cloth, "
    "grey fur and midnight-blue fabric with edges freezing into ice, engraved blackened-steel gauntlets with glowing "
    "blue cracks, tall over-the-knee dark steel boots with ice spikes"
)
SPEAR = "an enormous dark iron and silver rune spear whose blade is a glowing shard of glacier ice"
SPRITE = (
    "nordic frost valkyrie woman warrior, long ash-black hair with silver-blue ends and braids, silver crown, "
    "blackened-steel breastplate with glowing blue runes, black fur mantle on one shoulder, layered black and "
    f"midnight-blue battle skirt, dark steel knee-high boots, holding {SPEAR} upright, no wings, {NO_RED}"
)

ANIMS = [
    ("valkyrie", "walking forward with purpose, spear held upright, fur mantle swaying", 6),
    ("valkyrie", "thrusting the long spear forward in a fast lunge", 6),
    ("valkyrie", "sweeping the long spear in a wide horizontal arc", 6),
    ("valkyrie", "spinning around in a full circle whirling the spear", 6),
    ("valkyrie", "throwing the spear forward like a javelin", 6),
    ("valkyrie", "raising one hand to summon swirling frost magic", 6),
]

EXTRAS = [
    ("frost_raven", "a black raven with glowing blue eyes and frost crystals on its feathers, wings spread, flying", 32, "none", ""),
    ("valkyrie_horse", "a nordic frost valkyrie woman warrior with a long spear riding a huge black warhorse in dark nordic "
     f"plate armor with silver runes, the horse has a frost-white mane and glowing icy-blue eyes, {NO_RED}", 80, "none", "horse"),
    ("einherjar", f"a ghostly spectral viking warrior made of pale blue light with a round shield and an axe, translucent, {HEADS}", 48, "heroic", ""),
]
EXTRA_ANIMS = [
    ("frost_raven", "raven flying forward flapping its wings", 6),
    ("valkyrie_horse", "warhorse galloping forward at full charge, rider leveling the spear", 6),
    ("einherjar", "ghost warrior walking forward with shield raised", 6),
    ("einherjar", "ghost warrior swinging the axe", 6),
]


def portrait():
    for tag in "abc":
        out = gen.d_of("valkyrie") / f"portrait_{tag}.png"
        if out.exists():
            continue
        body = {
            "description": (
                f"cartoon character design portrait of one {LOOK}, standing confidently in a three-quarter pose, one hand "
                f"gripping {SPEAR} planted upright, the other hand summoning swirling blue frost runes, a black raven with "
                "glowing blue eyes on her shoulder, huge wings of black raven feathers turning into translucent blue ice "
                f"shards spread behind her, {NO_RED}, plain flat grey background, bold clean outlines, cel shading, "
                "anatomically correct, exactly two arms, exactly two legs, five fingers"
            ),
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "flat shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "red, crimson, blood, text, watermark, multiple characters, chibi, big head, nudity, "
                                    "exposed chest, extra limbs, extra arms, extra legs, duplicated limbs, deformed hands, scenery",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if not r:
            continue
        gen.log_charge(f"valkyrie portrait {tag}", r.get("usage"))
        gen.save_b64(r["image"], out)
        print("saved portrait", tag, flush=True)
    bg = gen.d_of("portrait_bg") / "valkyrie.png"
    if not bg.exists():
        body = {
            "description": "a frozen northern battlefield in a raging blizzard beneath snow-covered mountains, broken viking "
                           "shields and swords in deep snow, frozen longships in a distant fjord, ancient standing stones with "
                           "glowing blue runes, pale blue aurora in a dark stormy sky, circling ravens, background scenery only, "
                           f"no people, portrait orientation, {NO_RED}, {gen.STYLE}",
            "image_size": {"width": 140, "height": 200},
            "no_background": False,
            "outline": "single color black outline",
            "shading": "medium shading",
            "detail": "highly detailed",
            "view": "side",
            "negative_description": "people, person, character, figure, woman, text, watermark, red",
        }
        r = act2_art.safe(gen.call, "POST", "/create-image-bitforge", body)
        if r:
            gen.log_charge("portrait bg valkyrie", r.get("usage"))
            gen.save_b64(r["image"], bg)
            print("saved background", flush=True)


def sprite():
    if not (gen.GEN / "valkyrie" / "rotation_urls_south.png").exists():
        act2_art.safe(gen.character, "valkyrie", f"{SPRITE}, {HEADS}", 56, "realistic_female", "")
    print("sprite done", flush=True)


def anims():
    import world_art
    for name, action, frames in ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("valkyrie anims done", flush=True)


def extras():
    import world_art
    for name, desc, size, prop, tmpl in EXTRAS:
        # "horse" may not be a template PixelLab knows; the bear template made the dragon a good quadruped.
        for t in [tmpl] + (["bear"] if tmpl == "horse" else []):
            if (gen.GEN / name / "rotation_urls_south.png").exists():
                break
            act2_art.safe(gen.character, name, desc, size, prop, t, tries=2)
    for name, action, frames in EXTRA_ANIMS:
        act2_art.safe(world_art.run_anim, name, action, frames)
    print("valkyrie extras done", flush=True)


def review():
    d = gen.GEN / "valkyrie"
    ps = [d / f"portrait_{t}.png" for t in "abc"] + [gen.GEN / "portrait_bg" / "valkyrie.png"]
    ps += [d / f"rotation_urls_{k}.png" for k in ["south", "south-east", "east", "north-east", "north"]]
    gen.review(gen.GEN / "valkyrie_review.png", *[p for p in ps if p.exists()])


if __name__ == "__main__":
    {"portrait": portrait, "sprite": sprite, "anims": anims, "extras": extras, "review": review,
     "all": lambda: (portrait(), sprite(), anims(), extras())}[sys.argv[1]]()
