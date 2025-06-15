from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')

start = Vec3(-1090, 75, -110)


mc.setBlockCube("oak_planks", start, start + Vec3(2, 2, 2))
