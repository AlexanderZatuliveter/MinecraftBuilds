

from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')
mc.postToChat("Строю архитектурный небоскреб...")

# Положение
start_x = -260
start_y = 70
start_z = 50


# Параметры здания
floors = 10
floor_height = 4
width = 12
depth = 10

# Цвета
wall_block = "white concrete"
window_block = "glass pane"
floor_block = "stone slab"
accent_block = "gray concrete"

for floor in range(floors):
    y0 = start_y + floor * floor_height

    # Стены и окна
    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                x = start_x + dx
                z = start_z + dz
                pos = Vec3(x, y0 + y, z)

                # Внешний каркас (по периметру)
                is_edge = dx == 0 or dx == width - 1 or dz == 0 or dz == depth - 1

                # Окна на втором и третьем уровне каждого этажа
                if is_edge:
                    if y == 1 or y == 2:
                        mc.setBlock(window_block, pos)
                    else:
                        mc.setBlock(wall_block, pos)
                else:
                    # Внутри здание пустое
                    mc.setBlock("air", pos)

    # Пол между этажами
    for dx in range(width):
        for dz in range(depth):
            mc.setBlock(floor_block, Vec3(start_x + dx, y0, start_z + dz))

    # Балкон на каждом третьем этаже
    if floor % 3 == 0:
        for b in range(-2, 3):
            mc.setBlock("glass", Vec3(start_x + width, y0 + 1, start_z + depth // 2 + b))

# Крыша и антенна
roof_y = start_y + floors * floor_height
for dx in range(width):
    for dz in range(depth):
        mc.setBlock(accent_block, Vec3(start_x + dx, roof_y, start_z + dz))

# Антенна
for a in range(5):
    mc.setBlock("iron bars", Vec3(start_x + width // 2, roof_y + a, start_z + depth // 2))
