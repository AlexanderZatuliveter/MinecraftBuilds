from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('localhost')
mcw = MinecraftWrap(mc)

start = Vec3(350, 62, 150)

width = 14
depth = 25
floor_height = 4
floors = 3

wall_block = mc.Block("light gray concrete")
floor_block = mc.Block("stone bricks")
window_block = mc.Block("glass pane")


def floor(pos: Vec3, floor: int, floor_height: int):
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
                is_floor = y == 0 and dx not in (0, width - 1) and dz not in (0, depth - 1)

                is_dividing_wall = dz in (depth // 2 - 3, depth // 2 + 3) or \
                    (dz in (depth // 2 - 2, depth // 2 + 2) and dx in (0, width - 1))
                is_outside_wall = (dx in (0, width - 1) or dz in (0, depth - 1)) and y in (0, floor_height) \
                    or (dx in (0, width - 1) and dz in [z for z in range(depth // 2 - 2, depth // 2 + 3)] and y == 4)
                is_wall = is_outside_wall or is_dividing_wall or is_column

                if is_wall:
                    mcw.set_block(wall_block, pos)
                elif is_floor:
                    mcw.set_block(floor_block, pos)
                elif is_window:
                    mcw.set_block(window_block, pos)


# -----------------------------------------------------------------------------------------

mc.postToChat("Стройка небоскреба №2...")

for f in range(floors):
    floor(start, f, floor_height)

mcw.draw()
mc.postToChat("Стройка небоскреба завершена!")
