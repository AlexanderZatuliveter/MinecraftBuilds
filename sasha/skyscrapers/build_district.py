from mcpq import Minecraft, Vec3
from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams
from sasha.skyscrapers.my_skyscraper import MySkyscraper
from sasha.skyscrapers.luxury_tower import LuxuryTower
from sasha.skyscrapers.crystal_crown_tower import CrystalCrownTower
from sasha.skyscrapers.gemini_skyscraper import GeminiSkyscraper

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-1500, 70, -800)

skyscraper = MySkyscraper(mc)
luxury = LuxuryTower(mc)
crystal = CrystalCrownTower(mc)
gemini = GeminiSkyscraper(mc)

skyscraper.build(BuildParams(floors=20, floor_height=5, width=19, depth=15, start=start))
luxury.build(BuildParams(floors=18, floor_height=5, width=21, depth=17, start=start + Vec3(50, 0, 0)))
crystal.build(BuildParams(floors=22, floor_height=5, width=23, depth=19, start=start + Vec3(50, 0, 50)))
gemini.build(BuildParams(floors=20, floor_height=5, width=19, depth=15, start=start + Vec3(0, 0, 50)))
