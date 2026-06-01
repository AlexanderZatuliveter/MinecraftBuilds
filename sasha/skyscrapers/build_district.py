import random

from mcpq import Minecraft, Vec3
from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams
from sasha.skyscrapers.my_skyscraper import MySkyscraper
from sasha.skyscrapers.luxury_tower import LuxuryTower
from sasha.skyscrapers.crystal_crown_tower import CrystalCrownTower
from sasha.skyscrapers.gemini_skyscraper import GeminiSkyscraper

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(484, 70, -1231)


# skyscraper.build(BuildParams(floors=20, floor_height=5, width=19, depth=15, start=start))
# luxury.build(BuildParams(floors=18, floor_height=5, width=21, depth=17, start=start + Vec3(50, 0, 0)))
# crystal.build(BuildParams(floors=22, floor_height=5, width=23, depth=19, start=start + Vec3(50, 0, 50)))
# gemini.build(BuildParams(floors=20, floor_height=5, width=19, depth=15, start=start + Vec3(0, 0, 50)))

builders = [
    MySkyscraper(mc),
    LuxuryTower(mc),
    CrystalCrownTower(mc),
    GeminiSkyscraper(mc),
]

ROWS = 10
COLS = 10
SPACING_X = 45
SPACING_Z = 45

random.seed(42)

for i in range(ROWS * COLS):
    row = i // COLS
    col = i % COLS

    builder = random.choice(builders)

    floors = random.randint(10, 25)
    floor_height = 5
    width = random.choice([15, 17, 19, 21, 23])
    depth = random.choice([13, 15, 17, 19, 21])

    pos = start + Vec3(col * SPACING_X, 0, row * SPACING_Z)

    mc.postToChat(f"Строю дом {i + 1}/100 ...")
    builder.build(BuildParams(
        floors=floors,
        floor_height=floor_height,
        width=width,
        depth=depth,
        start=pos,
    ))

mc.postToChat("Город из 100 небоскрёбов готов!")
