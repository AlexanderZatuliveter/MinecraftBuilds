from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('localhost')
mcw = MinecraftWrap(mc)

start = Vec3(425, 62, 200)

width = 14
depth = 33
floor_height = 4
floors = 3

wall_block = mc.Block("light gray concrete")
roof_block = mc.Block("gray concrete")
floor_block = mc.Block("stone bricks")
window_block = mc.Block("glass pane")
ladder_block = mc.Block("stone brick stairs")
railings_block = mc.Block("oak fence")


def ladder(pos: Vec3, floor: int, floor_height: int):

    if floor % 2 == 0:
        dx = 5
        dy = 1
        mcw.set_block(railings_block, pos + Vec3(dx - 1, dy, depth // 2))
        for _ in range(floor_height):
            mcw.set_block(ladder_block.withData({"half": "top", "facing": "west"}), pos + Vec3(dx, dy, depth // 2))
            mcw.set_block(railings_block, pos + Vec3(dx, dy + 1, depth // 2))
            for dz in range(1, 3):
                p = pos + Vec3(dx, dy, depth // 2 + dz)
                mcw.set_block(ladder_block.withData({"facing": "east"}), p)
            dx += 1
            dy += 1
        pos1 = pos + Vec3(9, floor_height, depth // 2 + 2)
        pos2 = pos + Vec3(12, floor_height, depth // 2 - 2)
        mcw.set_block_cube(floor_block, pos1, pos2)
    else:
        dx = 8
        dy = 1
        mcw.set_block(railings_block, pos + Vec3(dx + 1, dy, depth // 2))
        for _ in range(floor_height):
            mcw.set_block(ladder_block.withData({"half": "top", "facing": "east"}), pos + Vec3(dx, dy, depth // 2))
            mcw.set_block(railings_block, pos + Vec3(dx, dy + 1, depth // 2))
            for dz in range(1, 3):
                p = pos + Vec3(dx, dy, depth // 2 - dz)
                mcw.set_block(ladder_block.withData({"facing": "west"}), p)
            dx -= 1
            dy += 1
        pos1 = pos + Vec3(1, floor_height, depth // 2 + 2)
        pos2 = pos + Vec3(4, floor_height, depth // 2 - 2)
        mcw.set_block_cube(floor_block, pos1, pos2)


def roof(pos: Vec3):
    roof_shift = floors * floor_height

    def antennas(pos: Vec3, block: Block):
        for i in range(3):
            dx = width // 2
            dz = depth // 4 * i + 2
            for a in range(5 + i * 2):
                mcw.set_block(block, pos + Vec3(dx, roof_shift + 1 + a, dz + 4))

    mcw.set_block_cube(roof_block, pos + Vec3(-1, roof_shift, -1), pos + Vec3(width, roof_shift, depth))
    antennas(pos, mc.Block("iron bars"))


def floor(start: Vec3, floor: int, floor_height: int):
    floor_shift = Vec3(0, floor * floor_height, 0)
    floor_start = start + floor_shift
    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                pos = floor_start + Vec3(dx, y, dz)

                is_enter = dx in (0, width - 1) and \
                    dz in [z for z in range(depth // 2 - 3, depth // 2 + 4)] and 1 <= y <= 3

                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_column = dx in (0, width - 1) and dz in (0, depth - 1)
                is_window = is_edge and y not in (0, floor_height) and not is_enter and not is_column
                is_floor = y == 0 and dx not in (0, width - 1) and dz not in (0, depth - 1) \
                    and (pos.y == start.y or dz not in [z for z in range(depth // 2 - 2, depth // 2 + 3)])

                if floor % 2 == 0:
                    is_dividing_wall = dz in (depth // 2 - 3, depth // 2 + 3) and dx not in (2, 3)
                else:
                    is_dividing_wall = dz in (depth // 2 - 3, depth // 2 + 3) and dx not in (10, 11)
                is_outside_wall = (dx in (0, width - 1) or dz in (0, depth - 1)) and y in (0, floor_height) \
                    or (dx in (0, width - 1) and dz in [z for z in range(depth // 2 - 2, depth // 2 + 3)] and y == 4)
                is_wall = is_outside_wall or is_dividing_wall or is_column

                if is_wall:
                    mcw.set_block(wall_block, pos)

                if is_floor:
                    mcw.set_block(floor_block, pos)

                if is_window:
                    if dx in (0, width - 1):
                        mcw.set_block(window_block.withData({"south": True, "north": True}), pos)
                    elif dz in (0, depth - 1):
                        mcw.set_block(window_block.withData({"east": True, "west": True}), pos)

                if is_enter and dz not in (depth // 2 - 3, depth // 2 + 3):
                    if floor == 0 and dx == 0:
                        if dz == depth // 2 - 2 and y == 3:
                            mcw.set_block(mc.Block("stone brick stairs").withData(
                                {"facing": "north", "half": "top"}), pos)
                        elif dz == depth // 2 + 2 and y == 3:
                            mcw.set_block(mc.Block("stone brick stairs").withData(
                                {"facing": "south", "half": "top"}), pos)
                    else:
                        mcw.set_block(window_block.withData({"south": True, "north": True}), pos)

    if floor != floors - 1:
        ladder(floor_start, floor, floor_height)

# -----------------------------------------------------------------------------------------


mc.postToChat("Стройка небоскреба №2...")

for f in range(floors):
    floor(start, f, floor_height)

roof(start)


mcw.draw()
mc.postToChat("Стройка небоскреба завершена!")
