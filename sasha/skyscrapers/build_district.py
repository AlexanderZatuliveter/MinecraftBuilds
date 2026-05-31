from mcpq import Minecraft, Vec3
from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.my_skyscraper import MySkyscraper

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-1300, 70, -650)


skyscraper = MySkyscraper(mc)
skyscraper.build(start)
