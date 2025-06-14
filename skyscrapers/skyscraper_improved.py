from mcpq import Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('192.168.1.77')
mcw = MinecraftWrap(mc)

start = Vec3(-417, 64, -602)

floors = 5
floor_height = 5
width = 19
depth = 15

wall_block = "white concrete"
glass_block = "light blue stained glass pane"
floor_block = "stone"
pillar_block = "gray concrete"
roof_block = "black concrete"
antenna_block = "iron bars"
atrium_block = "glowstone"


def roof(start: Vec3, block: str):
    roof_shift = floors * floor_height
    for dx in range(-1, width + 2):
        for dz in range(-1, depth + 2):
            mcw.set_block(block, start + Vec3(dx, roof_shift, dz))


def antennas(start: Vec3, block: str):
    roof_shift = floors * floor_height
    for i in range(3):
        dx = width // 3 * i + 2
        dz = depth // 2
        for a in range(5 + i * 2):
            mcw.set_block(block, start + Vec3(dx, roof_shift + 1 + a, dz))


def storage(pos: Vec3, wood_type: str):
    log_positions = [
        Vec3(0, 1, 0),
        Vec3(0, 2, 0),
        Vec3(0, 3, 0)
    ]

    for log_pos in log_positions:
        mcw.set_block(f"{wood_type} log", log_pos)

    mcw.set_block(f"lantern", pos + Vec3(0, 4, 0))

    chests = []
    for y in range(1, 4):
        mcw.set_block(mc.Block("chest").withData({"facing": "north"}), Vec3(1, y, 0))
        mcw.set_block(mc.Block("chest").withData({"facing": "north"}), Vec3(2, y, 0))
        mcw.set_block(mc.Block("chest").withData({"facing": "east"}), Vec3(0, y, -1))
        mcw.set_block(mc.Block("chest").withData({"facing": "east"}), Vec3(0, y, -2))
        mcw.set_block(mc.Block("chest").withData({"facing": "east"}), Vec3(0, y, -3))


def atrium_and_pillars(pos: Vec3, lighting_block: str, pillar_block: str, floor_height: int):

    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            mcw.set_block(lighting_block, pos + Vec3(dx, 0, dz))

    pillar_positions = []
    for y in range(1, floor_height):
        pillar_positions.append(pos + Vec3(-3, y, -3))
        pillar_positions.append(pos + Vec3(3, y, 3))
        pillar_positions.append(pos + Vec3(3, y, -3))
        pillar_positions.append(pos + Vec3(-3, y, 3))

    mc.setBlockList(pillar_block, pillar_positions)


def sofa_with_table(wood_type: str, pos: Vec3):
    mc.setBlock(f"{wood_type} fence", pos)
    mc.setBlock(f"{wood_type} pressure plate", pos + Vec3(0, 1, 0))
    stairs_properties = [
        (Vec3(0, 0, 2), "south"),
        (Vec3(1, 0, 2), "south"),
        (Vec3(2, 0, 1), "east"),
        (Vec3(2, 0, 0), "east")
    ]

    for (p, direction) in stairs_properties:
        block = mc.Block(f"{wood_type} stairs").withData({"facing": direction})
        mc.setBlock(block, p + pos)

    mc.setBlock(f"{wood_type} log", pos + Vec3(2, 0, 2))
    mc.setBlock(f"lantern", pos + Vec3(2, 1, 2))


def bookshelves_and_lanterns(pos: Vec3):
    bookshelves_positions = []
    for y in range(0, 3):
        bookshelves_positions.append(Vec3(0, y, 0))
        bookshelves_positions.append(Vec3(-1, y, 0))
        bookshelves_positions.append(Vec3(-2, y, 0))
        bookshelves_positions.append(Vec3(0, y, 1))
        bookshelves_positions.append(Vec3(0, y, 2))

    mc.setBlockList("bookshelf", [p + pos for p in bookshelves_positions])

    lantern_positions = [
        Vec3(0, 3, 0),
        Vec3(-2, 3, 0),
        Vec3(0, 3, 2),
    ]
    mc.setBlockList("lantern", [p + pos for p in lantern_positions])


def floor(start: Vec3, floor: int, floor_height: int, floor_block: str, pillar_block: str):
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
                        mc.setBlock(glass_block, pos)
                    else:
                        mc.setBlock(wall_block, pos)
                else:
                    # mc.setBlock("air", pos)
                    mc.setBlock(floor_block, floor_start + Vec3(dx, 0, dz))

    atrium_and_pillars(
        floor_start + Vec3(width // 2, 0, depth // 2), atrium_block, pillar_block, floor_height)

    # Мебель
    mc.setBed(floor_start + Vec3(4, 1, 3), "north")
    mc.setBed(floor_start + Vec3(3, 1, 3), "north")
    mc.setBlock("crafting table", floor_start + Vec3(2, 1, 2))
    mc.setBlock(f"lantern", floor_start + Vec3(2, 2, 2))

    storage(floor_start + Vec3(2, 0, depth - 3), "oak")
    sofa_with_table("oak", floor_start + Vec3(width - 5, 1, depth - 5))
    bookshelves_and_lanterns(floor_start + Vec3(width - 3, 1, 2))


# -----------------------------------------------------------------------------------------


mc.postToChat("Стройка небоскреба...")

# Строим этажи
for f in range(floors):
    floor(start, f, floor_height, floor_block, pillar_block)

# Крыша
roof(start, roof_block)

# Антенны
antennas(start, antenna_block)

mc.postToChat("Стройка небоскреба завершена!")
