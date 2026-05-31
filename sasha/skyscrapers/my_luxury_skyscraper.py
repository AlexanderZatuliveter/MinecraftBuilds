import random
from typing import Literal
from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('192.168.1.66')
mcw = MinecraftWrap(mc)

start = Vec3(-920, 66, -900)

# Увеличенные параметры здания
floors = 35  # Больше этажей
floor_height = 6  # Выше потолки
width = 25  # Шире
depth = 20  # Глубже

# Роскошные материалы
wall_block = mc.Block("quartz block")  # Кварц вместо бетона
glass_block = mc.Block("blue stained glass pane")  # Синее стекло
floor_block = mc.Block("polished blackstone")  # Полированный чернокамень
pillar_block = mc.Block("gold block")  # Золотые колонны!
roof_block = mc.Block("diamond block")  # Алмазная крыша!
antenna_block = mc.Block("netherite block")  # Незеритовые антенны
atrium_block = mc.Block("sea lantern")  # Морские фонари
railing_block = mc.Block("dark oak fence")
accent_block = mc.Block("emerald block")  # Изумрудные акценты


def luxury_roof(pos: Vec3, block: Block, accent: Block):
    roof_shift = floors * floor_height
    # Основная крыша
    for dx in range(-2, width + 3):
        for dz in range(-2, depth + 3):
            mcw.set_block(block, pos + Vec3(dx, roof_shift, dz))

    # Декоративные изумрудные полосы на крыше
    for dx in range(0, width, 5):
        for dz in range(depth):
            mcw.set_block(accent, pos + Vec3(dx, roof_shift + 1, dz))

    # Роскошная надстройка в центре
    center_x, center_z = width // 2, depth // 2
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            for dy in range(1, 4):
                mcw.set_block(accent, pos + Vec3(center_x + dx, roof_shift + dy, center_z + dz))


def luxury_antennas(pos: Vec3, block: Block):
    roof_shift = floors * floor_height
    # Больше и выше антенн
    for i in range(5):
        dx = width // 5 * i + 3
        dz = depth // 2 + (i % 2) * 2
        height = 8 + i * 3
        for a in range(height):
            mcw.set_block(block, pos + Vec3(dx, roof_shift + 4 + a, dz))
            # Добавляем боковые элементы
            if a % 3 == 0 and a > 0:
                mcw.set_block(mc.Block("gold block"), pos + Vec3(dx + 1, roof_shift + 4 + a, dz))
                mcw.set_block(mc.Block("gold block"), pos + Vec3(dx - 1, roof_shift + 4 + a, dz))


def luxury_table_with_lanterns(pos: Vec3):
    # Золотой стол с дорогими фонарями
    mcw.set_block(mc.Block("gold block"), pos + Vec3(0, 0, 0))
    mcw.set_block(mc.Block("gold block"), pos + Vec3(-1, 0, 0))
    mcw.set_block(mc.Block("gold block"), pos + Vec3(0, 0, -1))
    mcw.set_block(mc.Block("gold block"), pos + Vec3(-1, 0, -1))
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(-1, 1, -1))


def luxury_storage(pos: Vec3, wood_type: str):
    # Колонна из незерита
    log_positions = [Vec3(0, 1, 0), Vec3(0, 2, 0), Vec3(0, 3, 0), Vec3(0, 4, 0)]
    for log_pos in log_positions:
        mcw.set_block(mc.Block("netherite block"), log_pos + pos)
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 5, 0))

    # Больше сундуков в роскошном стиле
    chests_properties: list[tuple[Vec3, str]] = []
    for y in range(1, 5):
        chests_properties.extend([
            (Vec3(1, y, 0), "north"), (Vec3(2, y, 0), "north"), (Vec3(3, y, 0), "north"),
            (Vec3(0, y, -1), "east"), (Vec3(0, y, -2), "east"), (Vec3(0, y, -3), "east"),
            (Vec3(0, y, -4), "east"), (Vec3(-1, y, 0), "west"), (Vec3(-2, y, 0), "west")
        ])

    for p, direction in chests_properties:
        mcw.set_block(mc.Block("ender chest").withData({"facing": direction}), p + pos)


def luxury_atrium_and_pillars(pos: Vec3, lighting_block: Block, pillar_block: Block, floor_height: int):
    # Больший атриум с морскими фонарями
    lighting_positions = []
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            lighting_positions.append(Vec3(dx, 0, dz))

    for p in lighting_positions:
        mcw.set_block(lighting_block, p + pos)

    # Золотые колонны по углам
    pillar_positions = []
    for y in range(1, floor_height):
        pillar_positions.extend([
            Vec3(-4, y, -4), Vec3(4, y, 4), Vec3(4, y, -4), Vec3(-4, y, 4),
            Vec3(-4, y, 0), Vec3(4, y, 0), Vec3(0, y, -4), Vec3(0, y, 4)  # Дополнительные колонны
        ])

    for p in pillar_positions:
        mcw.set_block(pillar_block, p + pos)


def luxury_sofa_with_table(wood_type: str, pos: Vec3):
    # Роскошная мебель из темного дуба и золота
    mcw.set_block(mc.Block("gold block"), pos)
    mcw.set_block(mc.Block("red carpet"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block("emerald block"), pos + Vec3(2, 0, 2))
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(2, 1, 2))

    stairs_properties = [
        (Vec3(0, 0, 2), "south"), (Vec3(1, 0, 2), "south"), (Vec3(2, 0, 2), "south"),
        (Vec3(2, 0, 1), "east"), (Vec3(2, 0, 0), "east"), (Vec3(3, 0, 0), "east")
    ]
    for p, direction in stairs_properties:
        mcw.set_block(mc.Block("dark oak stairs").withData({"facing": direction}), p + pos)


def luxury_bookshelves_and_lanterns(pos: Vec3):
    # Библиотека с зачарованными столами
    bookshelves_positions = []
    for y in range(0, 4):
        bookshelves_positions.extend([
            Vec3(0, y, 0), Vec3(-1, y, 0), Vec3(-2, y, 0), Vec3(-3, y, 0),
            Vec3(0, y, 1), Vec3(0, y, 2), Vec3(0, y, 3)
        ])

    for p in bookshelves_positions:
        mcw.set_block(mc.Block("bookshelf"), p + pos)

    # Зачарованные столы
    mcw.set_block(mc.Block("enchanting table"), pos + Vec3(-1, 1, 1))
    mcw.set_block(mc.Block("enchanting table"), pos + Vec3(-1, 1, 2))

    # Роскошное освещение
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 4, 0))
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(-3, 4, 0))
    mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 4, 3))


def luxury_street_lamp(pos: Vec3, fence_material: str, facing: str):
    # Золотые уличные фонари
    for dy in range(2, 6):
        mcw.set_block(mc.Block("gold block"), pos + Vec3(0, dy, 0))

    if facing == "south":
        mcw.set_block(mc.Block("gold block"), pos + Vec3(0, 5, 1))
        mcw.set_block(mc.Block("gold block"), pos + Vec3(-1, 5, 0))
        mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 4, 1))
        mcw.set_block(mc.Block("sea lantern"), pos + Vec3(-1, 4, 0))
    elif facing == "north":
        mcw.set_block(mc.Block("gold block"), pos + Vec3(0, 5, -1))
        mcw.set_block(mc.Block("gold block"), pos + Vec3(-1, 5, 0))
        mcw.set_block(mc.Block("sea lantern"), pos + Vec3(0, 4, -1))
        mcw.set_block(mc.Block("sea lantern"), pos + Vec3(-1, 4, 0))


def luxury_ladder(pos: Vec3, floor: int, floor_height: int, max_floor: int):
    def even_floor():
        # Роскошная платформа из кварца и золота
        mcw.set_block_cube("quartz block", pos + Vec3(1, 0, -1), pos + Vec3(4, 0, -5))
        for dx in range(1, 6):
            mcw.set_block(mc.Block("gold block"), pos + Vec3(dx, 0, 0))

        # Лестница из кварца
        stairs_y = 1
        for dz in range(6, 12):
            mcw.set_block(mc.Block("quartz stairs"), pos + Vec3(1, stairs_y, -dz))
            mcw.set_block(mc.Block("quartz stairs"), pos + Vec3(2, stairs_y, -dz))
            mcw.set_block(mc.Block("quartz stairs"), pos + Vec3(3, stairs_y, -dz))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(4, stairs_y, -dz + 1))
            mcw.set_block(mc.Block("quartz stairs").withData(
                {"facing": "south", "half": "top"}), pos + Vec3(4, stairs_y, -dz))
            stairs_y += 1

        # Верхняя платформа
        mcw.set_block_cube("quartz block", pos + Vec3(1, floor_height, -12), pos + Vec3(4, floor_height, -16))
        for dx in range(1, 5):
            mcw.set_block(mc.Block("gold block"), pos + Vec3(dx, floor_height, -17))

    def odd_floor():
        # Аналогично, но с другой стороны и роскошнее
        mcw.set_block_cube("quartz block", pos + Vec3(7, 0, -12), pos + Vec3(5, 0, -16))

        for dx in range(1, 8):
            mcw.set_block(mc.Block("gold block"), pos + Vec3(dx, 0, -17))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(dx, 1, -17))
        for dz in range(12, 17):
            mcw.set_block(mc.Block("gold block"), pos + Vec3(7, 0, -dz))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(7, 1, -dz))

        luxury_street_lamp(pos + Vec3(7, 0, -17), fence_material="dark oak", facing="south")

        # Лестница
        stairs_y = 6
        for dz in range(6, 12):
            mcw.set_block(mc.Block("quartz stairs").withData({"facing": "south"}), pos + Vec3(5, stairs_y, -dz))
            mcw.set_block(mc.Block("quartz stairs").withData({"facing": "south"}), pos + Vec3(6, stairs_y, -dz))
            mcw.set_block(mc.Block("quartz stairs").withData(
                {"facing": "north", "half": "top"}), pos + Vec3(7, stairs_y, -dz))
            mcw.set_block(mc.Block("quartz stairs").withData(
                {"facing": "north", "half": "top"}), pos + Vec3(4, stairs_y, -dz))
            mcw.set_block(railing_block, pos + Vec3(7, stairs_y + 1, -dz))
            mcw.set_block(railing_block, pos + Vec3(4, stairs_y, -dz - 1))
            stairs_y -= 1

        # Верхняя платформа
        mcw.set_block_cube("quartz block", pos + Vec3(5, floor_height, -1), pos + Vec3(6, floor_height, -5))

        for dx in range(1, 8):
            if dx >= 6:
                mcw.set_block(mc.Block("gold block"), pos + Vec3(dx, floor_height, 0))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(dx, floor_height + 1, 0))
        for dz in range(1, 6):
            mcw.set_block(mc.Block("gold block"), pos + Vec3(7, floor_height, -dz))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(7, floor_height + 1, -dz))

        luxury_street_lamp(pos + Vec3(7, floor_height, 0), fence_material="dark oak", facing="north")

    # Базовая платформа
    if floor == 0:
        mcw.set_block_cube("quartz block", pos + Vec3(5, 0, 0), pos + Vec3(7, 0, -5))
        for dx in range(5, 8):
            mcw.set_block(railing_block, pos + Vec3(dx, 1, -5))
        for dz in range(0, 5):
            mcw.set_block(railing_block, pos + Vec3(7, 1, -dz))
        luxury_street_lamp(pos + Vec3(7, 0, 0), fence_material="dark oak", facing="north")

    elif floor == max_floor:
        if max_floor % 2 == 0:
            mcw.set_block(railing_block, pos + Vec3(4, floor_height + 1, -11))
            mcw.set_block(railing_block, pos + Vec3(5, floor_height + 1, -11))
            mcw.set_block(mc.Block("gold block"), pos + Vec3(5, floor_height, -11))
            for dz in range(12, 18):
                mcw.set_block(mc.Block("gold block"), pos + Vec3(5, floor_height, -dz))
                mcw.set_block(railing_block, pos + Vec3(5, floor_height + 1, -dz))
            for dx in range(1, 5):
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, -17))
            luxury_street_lamp(pos + Vec3(5, floor_height, -17), fence_material="dark oak", facing="south")
        else:
            mcw.set_block_cube("quartz block", pos + Vec3(1, floor_height, -1), pos + Vec3(4, floor_height, -6))
            for dx in range(1, 5):
                mcw.set_block(mc.Block("gold block"), pos + Vec3(dx, floor_height, 0))
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, 0))
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, -6))

    if floor % 2 != 0:
        odd_floor()
    else:
        even_floor()


def luxury_floor(pos: Vec3, floor: int, floor_height: int, floor_block: Block, pillar_block: Block):
    floor_shift = Vec3(0, floor * floor_height, 0)
    floor_start = start + floor_shift

    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                pos = floor_start + Vec3(dx, y, dz)

                # Внешний каркас с роскошными материалами
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_corner = (dx in (0, width - 1)) and (dz in (0, depth - 1))

                if is_edge:
                    if 1 <= y <= 4:  # Выше окна
                        if is_corner or dx % 3 == 0 or dz % 3 == 0:
                            # Золотые рамы окон
                            mcw.set_block(mc.Block("gold block"), pos)
                        else:
                            # Синие панорамные окна
                            mcw.set_block(glass_block, pos)
                    else:
                        if is_corner:
                            mcw.set_block(accent_block, pos)  # Изумрудные углы
                        else:
                            mcw.set_block(wall_block, pos)
                else:
                    if y == 0:
                        # Роскошный пол
                        if (dx + dz) % 2 == 0:
                            mcw.set_block(floor_block, floor_start + Vec3(dx, 0, dz))
                        else:
                            mcw.set_block(mc.Block("polished blackstone bricks"), floor_start + Vec3(dx, 0, dz))

    # Лестница (только если не последний этаж)
    if floor != floors - 1:
        luxury_ladder(floor_start + Vec3(width - 1, 0, depth - 1), floor, floor_height, floors - 2)

    # Роскошный атриум
    luxury_atrium_and_pillars(
        floor_start + Vec3(width // 2, 0, depth // 2), atrium_block, pillar_block, floor_height)

    # Роскошная мебель и декор

    # VIP кровати и мебель
    bed_colors: list[Literal["red", "orange", "yellow", "lime", "green", "cyan", "light_blue", "blue", "purple", "magenta", "pink"]] = [
        "red", "orange", "yellow", "lime", "green", "cyan", "light_blue", "blue", "purple", "magenta", "pink"]
    rand_color = random.choice(bed_colors)

    # Двуспальная кровать
    mc.setBed(floor_start + Vec3(5, 1, 4), "north", rand_color)
    mc.setBed(floor_start + Vec3(4, 1, 4), "north", rand_color)
    mc.setBed(floor_start + Vec3(6, 1, 4), "north", rand_color)
    mc.setBed(floor_start + Vec3(3, 1, 4), "north", rand_color)

    # Золотой верстак
    mcw.set_block(mc.Block("smithing table"), floor_start + Vec3(3, 1, 3))
    mcw.set_block(mc.Block("sea lantern"), floor_start + Vec3(3, 2, 3))

    # Роскошное хранилище
    luxury_storage(floor_start + Vec3(3, 0, depth - 4), "dark oak")

    # Различная мебель на четных и нечетных этажах
    if floor % 2 == 0:
        luxury_bookshelves_and_lanterns(floor_start + Vec3(width - 4, 1, 3))
        luxury_table_with_lanterns(floor_start + Vec3(width - 5, 1, depth - 3))
        # Больше места для прохода
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, depth - 4))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, depth - 4))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 3, depth - 4))
    else:
        luxury_sofa_with_table("dark oak", floor_start + Vec3(width - 6, 1, depth - 6))
        luxury_table_with_lanterns(floor_start + Vec3(width - 5, 1, 2))
        # Больше места для прохода
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, 3))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, 3))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 3, 3))

    # Дополнительные роскошные элементы на каждом этаже
    if floor % 5 == 0:  # Каждый 5-й этаж - особенно роскошный
        # Золотые колонны по периметру
        for dx in range(2, width - 2, 3):
            mcw.set_block(mc.Block("gold block"), floor_start + Vec3(dx, 1, 2))
            mcw.set_block(mc.Block("gold block"), floor_start + Vec3(dx, 1, depth - 3))
        for dz in range(2, depth - 2, 3):
            mcw.set_block(mc.Block("gold block"), floor_start + Vec3(2, 1, dz))
            mcw.set_block(mc.Block("gold block"), floor_start + Vec3(width - 3, 1, dz))


# -----------------------------------------------------------------------------------------

mc.postToChat("Строительство роскошного небоскреба начинается...")

# Строим все этажи
for f in range(floors):
    luxury_floor(start, f, floor_height, floor_block, pillar_block)
    if f % 5 == 0:
        mc.postToChat(f"Построено {f + 1} этажей из {floors}...")

# Роскошная крыша
luxury_roof(start, roof_block, accent_block)

# Элитные антенны
luxury_antennas(start, antenna_block)

mcw.draw()
mc.postToChat("Роскошный небоскреб завершен! 35 этажей элитной недвижимости!")
