
from mcpq import Minecraft, Vec3
from city.castle import MassiveCastle
from common.minecraft_wrap import MinecraftWrap
from city.build_params import BuildParams

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-96, 64, -160)


castle = MassiveCastle(mc)
castle.build(BuildParams(floors=10, floor_height=6, width=160, depth=160, start=start))
