from mcpq import Minecraft, Vec3

mc = Minecraft('localhost')

start = Vec3(455, 63, 252)

block = mc.getBlockWithData(start)

print(block)