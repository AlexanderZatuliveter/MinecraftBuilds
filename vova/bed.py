from mcpq import Minecraft, Vec3

from common import fill_cube

mc = Minecraft('192.168.1.77')
mc.postToChat("Зе бед")

# Начальные координаты (нижний левый угол передней левой ноги)

start = Vec3(-333, 100, 600)

# Размеры
bed_color = Vec3(24, 4, 16)

pillow = Vec3(8, 4, 16)

wooden_layer = Vec3(32, 2, 16)

legs = Vec3(3, 3, 3)

pillow_start = Vec3(start.x + bed_color.x, start.y, start.z)
wooden_layer_start = Vec3(start.x, start.y - wooden_layer.y, start.z)

leg_offset = Vec3(0, -wooden_layer.y - legs.y, 0)

# Позиции ног относительно start
leg_positions = [
    start + Vec3(0, 0, 0),                  # задняя левая
    start + Vec3(0, 0, wooden_layer.z - legs.z),             # задняя правая
    start + Vec3(wooden_layer.x - legs.x, 0, wooden_layer.z - legs.z),        # передняя правая
    start + Vec3(wooden_layer.x - legs.x, 0, 0),            # передняя левая
]

# Строим ноги
for pos in leg_positions:
    fill_cube(mc, pos + leg_offset, legs, "oak planks")