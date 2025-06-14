from mcpq import Minecraft, Vec3
import random

mc = Minecraft('192.168.1.77')

start = Vec3(-378, 71, -440)


mc.setBlockCube("oak_planks", start, start + Vec3(30, 30, 30))
