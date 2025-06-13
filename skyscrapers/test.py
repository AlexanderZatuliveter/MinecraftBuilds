from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')

start = Vec3(-396, 65, -603)

block = mc.getBlockWithData(start)

print(block)