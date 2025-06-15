from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('192.168.1.77')
mcw = MinecraftWrap(mc)

start = Vec3(-220, 67, -65)

floors = 5
floor_height = 5
width = 19
depth = 15

wall_block = mc.Block("white concrete")
glass_block = mc.Block("light blue stained glass pane")
floor_block = mc.Block("stone")
pillar_block = mc.Block("gray concrete")
roof_block = mc.Block("black concrete")
antenna_block = mc.Block("iron bars")
atrium_block = mc.Block("glowstone")


def roof(pos: Vec3, block: Block):
    roof_shift = floors * floor_height
    for dx in range(-1, width + 2):
        for dz in range(-1, depth + 2):
            mcw.set_block(block, pos + Vec3(dx, roof_shift, dz))


def antennas(pos: Vec3, block: Block):
    roof_shift = floors * floor_height
    for i in range(3):
        dx = width // 3 * i + 2
        dz = depth // 2
        for a in range(5 + i * 2):
            mcw.set_block(block, pos + Vec3(dx, roof_shift + 1 + a, dz))


def table_with_lanterns(pos: Vec3):
    mcw.set_block(mc.Block("crafting table"), pos + Vec3(0, 0, 0))
    mcw.set_block(mc.Block("crafting table"), pos + Vec3(-1, 0, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(-1, 1, 0))


def storage(pos: Vec3, wood_type: str):
    log_positions = [
        Vec3(0, 1, 0),
        Vec3(0, 2, 0),
        Vec3(0, 3, 0)
    ]
    for log_pos in log_positions:
        mcw.set_block(mc.Block(f"{wood_type} log"), log_pos + pos)
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 4, 0))

    chests_properties: list[tuple[Vec3, str]] = []

    for y in range(1, 4):
        chests_properties.extend(
            [(Vec3(1, y, 0), "north"),
             (Vec3(2, y, 0), "north"),
             (Vec3(0, y, -1), "east"),
             (Vec3(0, y, -2), "east"),
             (Vec3(0, y, -3), "east")]
        )

    for p, direction in chests_properties:
        mcw.set_block(mc.Block("chest").withData({"facing": direction}), p + pos)


def atrium_and_pillars(pos: Vec3, lighting_block: Block, pillar_block: Block, floor_height: int):

    lighting_positions = []
    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            lighting_positions.append(Vec3(dx, 0, dz))

    for p in lighting_positions:
        mcw.set_block(lighting_block, p + pos)

    pillar_positions = []
    for y in range(1, floor_height):
        pillar_positions.extend(
            [Vec3(-3, y, -3),
             Vec3(3, y, 3),
             Vec3(3, y, -3),
             Vec3(-3, y, 3)]
        )

    for p in pillar_positions:
        mcw.set_block(pillar_block, p + pos)


def sofa_with_table(wood_type: str, pos: Vec3):
    mcw.set_block(mc.Block(f"{wood_type} fence"), pos)
    mcw.set_block(mc.Block(f"{wood_type} pressure plate"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block(f"{wood_type} log"), pos + Vec3(2, 0, 2))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(2, 1, 2))

    stairs_properties = [
        (Vec3(0, 0, 2), "south"),
        (Vec3(1, 0, 2), "south"),
        (Vec3(2, 0, 1), "east"),
        (Vec3(2, 0, 0), "east")
    ]
    for p, direction in stairs_properties:
        mcw.set_block(mc.Block(f"{wood_type} stairs").withData({"facing": direction}), p + pos)


def bookshelves_and_lanterns(pos: Vec3):
    bookshelves_positions = []
    for y in range(0, 3):
        bookshelves_positions.extend(
            [Vec3(0, y, 0),
             Vec3(-1, y, 0),
             Vec3(-2, y, 0),
             Vec3(0, y, 1),
             Vec3(0, y, 2)]
        )

    for p in bookshelves_positions:
        mcw.set_block(mc.Block("bookshelf"), p + pos)

    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 3, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(-2, 3, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 3, 2))


def floor(pos: Vec3, floor: int, floor_height: int, floor_block: Block, pillar_block: Block):
    floor_shift = Vec3(0, floor * floor_height, 0)
    floor_start = start + floor_shift
    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                pos = floor_start + Vec3(dx, y, dz)

                # Внешний каркас
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)

                if is_edge:
                    if 1 <= y <= 3:
                        # Панорамные окна
                        mcw.set_block(glass_block, pos)
                    else:
                        mcw.set_block(wall_block, pos)
                else:
                    mcw.set_block(floor_block, floor_start + Vec3(dx, 0, dz))

    atrium_and_pillars(
        floor_start + Vec3(width // 2, 0, depth // 2), atrium_block, pillar_block, floor_height)

    # Мебель

    # Кровать и верстак
    mc.setBed(floor_start + Vec3(4, 1, 3), "north")
    mc.setBed(floor_start + Vec3(3, 1, 3), "north")
    mcw.set_block(mc.Block("crafting table"), floor_start + Vec3(2, 1, 2))
    mcw.set_block(mc.Block("lantern"), floor_start + Vec3(2, 2, 2))

    # Другое
    storage(floor_start + Vec3(2, 0, depth - 3), "oak")

    if floor % 2 == 0:
        bookshelves_and_lanterns(floor_start + Vec3(width - 3, 1, 2))
        table_with_lanterns(floor_start + Vec3(width - 4, 1, depth - 2))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, depth - 3))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, depth - 3))
    else:
        sofa_with_table(mc.Block("oak"), floor_start + Vec3(width - 5, 1, depth - 5))
        table_with_lanterns(floor_start + Vec3(width - 4, 1, 1))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, 3))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, 3))


# -----------------------------------------------------------------------------------------


mc.postToChat("Стройка небоскреба...")

# Строим этажи
for f in range(floors):
    floor(start, f, floor_height, floor_block, pillar_block)

# Крыша
roof(start, roof_block)

# Антенны
antennas(start, antenna_block)

mcw.draw()
mc.postToChat("Стройка небоскреба завершена!")
