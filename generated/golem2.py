import sys
sys.path.insert(0, r"D:\projects\AshenSanctum-art\tools")
import gen, world_art, act2_art
act2_art.safe(gen.character, "boss_junkgolem2", "a crude hulking golem built from rusty orange-brown scrap metal junk: a dented old boiler for a chest glowing orange through cracks, mismatched riveted plates, bent pipes for arms, cog wheels stuck in its shoulders, huge clumsy iron fists, rust and grime everywhere, not sleek, not a robot, falling apart", 96, "heroic", "")
for a in ["scrap golem stomping forward heavily", "scrap golem smashing both iron fists down"]:
    act2_art.safe(world_art.run_anim, "boss_junkgolem2", a, 6)
print("golem2 done")
