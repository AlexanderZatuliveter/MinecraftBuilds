from mcpq import Minecraft, Vec3
from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams
from sasha.skyscrapers.my_skyscraper import MySkyscraper

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-1350, 70, -650)


skyscraper = MySkyscraper(mc)


build_params = BuildParams(
    floors=20,
    floor_height=5,
    width=19,
    depth=15,
    start=start
)

skyscraper.build(build_params)
