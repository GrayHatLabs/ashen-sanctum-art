# Ashen Sanctum art style

Rules for every new sprite. Decided with the user on 2026-10-01.

## Characters

- **Realistic proportions with small heads, like the mage.** No chibi or big-head characters.
  - Prompt suffix: `small head, realistic adult body proportions, long legs`.
  - PixelLab `proportions` preset: `heroic` for the hero, monsters and bosses;
    `realistic_male` / `realistic_female` for townsfolk.
  - Never use the `default` or `chibi` presets for people or humanoid monsters (that's what
    made the first skeletons, zombies and villagers big-headed).
- **Goblins, not imps.** The small, cowardly pack monster is a lean **green** goblin with pointed
  ears and a crude dagger (art name `goblin`). No red imps.
- 8-direction isometric characters: `create-character-with-8-directions`, standard mode,
  `view: high top-down`, `isometric: true`, size 48 for people and monsters (40-44 for small
  ones), 72-96 for bosses.
- Dark gothic fantasy, Diablo 2 style, gritty muted colours (`gen.py` adds this to every prompt).
- Animations: v3, 6 frames, 5 directions (S, SE, E, NE, N); `pack.py` mirrors W, SW, NW.

## Fixing generated animations (`tools/pack.py`)

PixelLab sometimes paints glowing effects or drifts mid-animation. Check every new animation
with a contact sheet before importing, then fix it in `pack.py`, not by hand:

- `FIX` per (character, animation, direction): `drop` glowing frames, `use` another animation
  for that direction, or `key` out a stray effect colour.
- `TRIM` keeps only the first N frames when the figure turns around or the weapon morphs.
- Slash smears and impact sparks that read as part of the attack can stay.
- After animations finish, re-fetch the character (`python gen.py fetch <name>`, free). The
  server reorders animations, so local frame files can go stale.

## Props and tiles

- Props use bitforge with `isometric: true` (`gen.py prop`). Floor items are scaled so their
  longest side is 14 px (D2-size).
- Watch out for pots, planters or base platforms under trees. Use negative prompts (`pot,
  planter, base, platform`) or key them out in `pack.py`.
- The old big-head art is kept in `generated/_old/` for reference.
