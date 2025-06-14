from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')  # connect to server on localhost

mc.postToChat("Hello Minecraft!")
#pos = Vec3(83, 73, -112)  # origin of world, coordinates x, y and z = 0
#block = mc.getBlock(pos)  # get block at origin
start_x = 138
start_y = 83
start_z = -95

for x in range(2, 5):
    for z in range(1, 1000):
        pos = Vec3(start_x + x, start_y, start_z + z)    
        mc.setBlock("stone", pos)  # replace block with obsidian
# mc.postToChat("Replaced", block, "with obsidian at", pos)
