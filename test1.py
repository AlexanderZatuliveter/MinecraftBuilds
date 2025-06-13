from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')

mc.postToChat("Hello Minecraft!")

start_x = -279
start_y = 76
start_z = -75

colors = [
    "red",
    "orange",
    "yellow",
    "lime",
    "light blue",
    "blue",
    "purple"
]

mc.setBlock("smooth quartz stairs", Vec3(1, 1, 1))

# for y, color in enumerate(colors):
#     for x in range(1, 100):
#         pos = Vec3(start_x + x, start_y + y, start_z)
#         mc.setBlock(f"{color} concrete", pos)
