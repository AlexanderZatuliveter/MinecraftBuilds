

from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')

start = Vec3(-360, 70, -403)

# cmd = mc.Block("command_block")#.withData({"value": "tp @p 0 0 0"})

# mc.setBlock(cmd, start)

block = mc.getBlockWithData(start)

#print(block)

mc.setBlock(block, start + Vec3(0, 2, 0))