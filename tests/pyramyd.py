from mcpq import Minecraft, Vec3
import random

mc = Minecraft('192.168.1.77')
mc.postToChat("🔺 Создание Великой Четырёхгранной Пирамиды началось!")

# Начальные координаты и размеры
origin_x = 50
origin_y = 70
origin_z = -150
size = 61  # нечетное для центра
height = size // 2

# === Строим внешнюю оболочку пирамиды ===
for level in range(height):
    for x in range(size - level * 2):
        for z in range(size - level * 2):
            bx = origin_x + level + x
            by = origin_y + level
            bz = origin_z + level + z
            mc.setBlock("sandstone", Vec3(bx, by, bz))

# === Внутренняя очистка для этажей и лабиринта ===
for level in range(1, height - 1):
    for x in range(size - level * 2 - 2):
        for z in range(size - level * 2 - 2):
            bx = origin_x + level + 1 + x
            by = origin_y + level
            bz = origin_z + level + 1 + z
            mc.setBlock("air", Vec3(bx, by, bz))

# === Внутренняя лестница в центр ===
center_x = origin_x + size // 2
center_z = origin_z + size // 2
for i in range(height - 1):
    mc.setBlock("stone_brick_stairs", Vec3(center_x, origin_y + i, center_z), {"facing": "north"})

# === Комнаты на разных уровнях ===
def build_room(x, y, z, w=7, h=4, d=7):
    for dx in range(w):
        for dy in range(h):
            for dz in range(d):
                px = x + dx
                py = y + dy
                pz = z + dz
                if dx in [0, w - 1] or dy in [0, h - 1] or dz in [0, d - 1]:
                    mc.setBlock("cut_sandstone", Vec3(px, py, pz))
                else:
                    mc.setBlock("air", Vec3(px, py, pz))
    mc.setBlock("chest", Vec3(x + w//2, y + 1, z + d//2))

levels_with_rooms = [origin_y + 5, origin_y + 10, origin_y + 15]
for y in levels_with_rooms:
    rx = center_x - 3
    rz = center_z - 3
    build_room(rx, y, rz)

# === Лабиринт у основания ===
def build_labyrinth(x0, y, z0, w, d):
    for x in range(w):
        for z in range(d):
            wall = random.choice([True, False, False])
            for dy in range(3):
                block = "smooth_sandstone" if wall else "air"
                mc.setBlock(block, Vec3(x0 + x, y + dy, z0 + z))

build_labyrinth(origin_x + 2, origin_y + 1, origin_z + 2, size - 4, size - 4)

# === Вход ===
for dx in range(3):
    for dy in range(4):
        mc.setBlock("air", Vec3(origin_x + size // 2 + dx - 1, origin_y + dy, origin_z + size - 1))

mc.postToChat("✅ Полная Пирамида построена: 4 грани, комнаты, лестница, лабиринт.")
