from mcpq import Minecraft, Vec3
import random

mc = Minecraft('192.168.1.77')
mc.postToChat("Генерация Удивительного Мира начинается!")

start_x = 100
start_y = 80
start_z = -100

# Создание летающих островов
def create_floating_island(cx, cy, cz, radius):
    for x in range(-radius, radius):
        for y in range(-radius // 2, radius // 2):
            for z in range(-radius, radius):
                if x**2 + (2*y)**2 + z**2 < radius**2:
                    mc.setBlock("grass_block", Vec3(cx + x, cy + y, cz + z))

# Посадка простого дерева
def plant_tree(x, y, z):
    for dy in range(5):
        mc.setBlock("oak_log", Vec3(x, y + dy, z))
    for dx in range(-2, 3):
        for dy in range(4, 7):
            for dz in range(-2, 3):
                if dx**2 + dz**2 < 5:
                    mc.setBlock("oak_leaves", Vec3(x + dx, y + dy, z + dz))

# Стеклянный мост
def build_glass_bridge(x1, z1, x2, z2, y):
    for i in range(abs(x2 - x1) + 1):
        for j in range(-1, 2):
            for k in range(-1, 2):
                mc.setBlock("glass", Vec3(x1 + i, y + j, z1 + k))

# Водопад
def create_waterfall(x, y, z, height):
    for dy in range(height):
        mc.setBlock("water", Vec3(x, y - dy, z))

# Генерация мира
for i in range(5):
    ix = start_x + i * 30
    iz = start_z + random.randint(0, 50)
    iy = start_y + random.randint(5, 15)
    create_floating_island(ix, iy, iz, radius=7)
    plant_tree(ix, iy + 3, iz)
    create_waterfall(ix + 3, iy, iz + 3, height=15)

build_glass_bridge(start_x, start_z, start_x + 120, start_z + 10, start_y + 5)

mc.postToChat("Удивительный Мир построен!")