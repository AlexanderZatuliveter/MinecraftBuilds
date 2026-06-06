
from mcpq import Minecraft, Vec3
from city.castle import MassiveCastle
from city.castle2 import UltimateCastle
from common.minecraft_wrap import MinecraftWrap
from city.build_params import BuildParams

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-332, 64, -30)


castle = UltimateCastle(mc)
castle.build(BuildParams(floors=10, floor_height=6, width=162, depth=162, start=start))
