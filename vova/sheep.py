from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')
mc.postToChat("Овца обновлена!")

# Начальные координаты (нижний левый угол передней левой ноги)
start_x = -1320
start_y = 64
start_z = 489

# Цвета
WOOL_WHITE = "white_wool"
WOOL_PINK = "pink_wool"
WOOL_BROWN = "brown_wool"
WOOL_BLACK = "black_wool"

# === Размеры
body_length = 32
body_height = 16
body_width = 16

leg_size = 7
leg_height = 12

head_width = 14
head_height = 14
head_length = 14

# === Тело
for x in range(body_length):
    for y in range(body_height):
        for z in range(body_width):
            mc.setBlock(WOOL_WHITE, Vec3(start_x + x, start_y + leg_height + y, start_z + z))

# === Ноги (4 ноги — верхние 2 слоя 7x7, остальные 5x5)
leg_offsets = [
    (+2, 0),                                 # передняя левая
    (+2, body_width - leg_size),            # передняя правая
    (body_length - leg_size - 1, 0),           # задняя левая
    (body_length - leg_size - 1, body_width - leg_size)  # задняя правая
]

for dx, dz in leg_offsets:
    for y in range(leg_height):
        # Верхние два слоя — 7x7, остальные — 5x5
        layer_size = 7 if y >= leg_height - 2 else 5
        offset = (leg_size - layer_size) // 2  # Центрируем 5x5 внутри 7x7

        for x in range(layer_size):
            for z in range(layer_size):
                block_type = WOOL_BROWN if y < 2 else WOOL_WHITE
                mc.setBlock(
                    block_type,
                    Vec3(start_x + dx + offset + x, start_y + y, start_z + dz + offset + z)
                )

# === Голова
head_x = start_x - head_length + 8
head_y = start_y + body_height + 4
head_z = start_z + (body_width // 2) - (head_width // 2)

for x in range(head_length):
    for y in range(head_height):
        for z in range(head_width):
            bx = head_x + x
            by = head_y + y
            bz = head_z + z

            # Морда — перед головы
            if x == 0 and 1 <= z <= 4 and 1 <= y <= 4:
                mc.setBlock(WOOL_PINK, Vec3(bx, by, bz))
            # Глаза
            elif x == 1 and (z == 1 or z == 4) and 2 <= y <= 3:
                mc.setBlock(WOOL_BLACK, Vec3(bx, by, bz))
            else:
                mc.setBlock(WOOL_WHITE, Vec3(bx, by, bz))

# === Лицо (морда) — 12x12, выступает на 2 блока вперёд
face_length = 2
face_size = 12

face_x = head_x - face_length
face_y = head_y + 1
face_z = head_z + 1

for x in range(face_length):
    for y in range(face_size):
        for z in range(face_size):
            bx = face_x + x
            by = face_y + y
            bz = face_z + z

            # === РОТ — розовый 4x4 внизу центра
            if x == 0 and 4 <= z <= 7 and 0 <= y <= 3:
                mc.setBlock(WOOL_PINK, Vec3(bx, by, bz))

            # === ГЛАЗА
            # Черные 2x2, 4 блока ниже верха
            elif x == 0 and 6 <= y <= 7 and z in (0, 1, 10, 11):
                mc.setBlock(WOOL_BLACK, Vec3(bx, by, bz))
            # Белые рядом с ними
            elif x == 0 and 6 <= y <= 7 and z in (2, 3, 8, 9):
                mc.setBlock(WOOL_WHITE, Vec3(bx, by, bz))

            # === ВЕРХНЯЯ БЕЛАЯ ПОЛОСА
            elif y in (10, 11):
                mc.setBlock(WOOL_WHITE, Vec3(bx, by, bz))

            # === НИЖНИЕ БЕЛЫЕ УГЛЫ (симметричные)
            elif y <= 3 and z in (0, 1, 10, 11):
                mc.setBlock(WOOL_WHITE, Vec3(bx, by, bz))

            # === ВСЁ ОСТАЛЬНОЕ — КОРИЧНЕВОЕ
            else:
                mc.setBlock(WOOL_BROWN, Vec3(bx, by, bz))