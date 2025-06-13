

from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')

start = Vec3(-370, 70, -402)

chest = mc.Block("chest").withData({"facing": "east"})

mc.setBlock(chest, start)
