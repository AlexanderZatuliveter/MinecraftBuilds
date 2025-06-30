from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('localhost')
mcw = MinecraftWrap(mc)

start = Vec3(501, 63, 169)

width = 14
depth = 27
floor_height = 5
floors = 1

wall_block = mc.Block("cherry planks")
window_block = mc.Block("pink stained glass pane")
floor_block = mc.Block("cherry wood")
column_block = mc.Block("cherry wood")


def floor(pos: Vec3, floor: int, floor_height: int):
    floor_shift = Vec3(0, floor * floor_height, 0)
    floor_start = start + floor_shift
    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                pos = floor_start + Vec3(dx, y, dz)
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)

                if y == 0 and not is_edge:
                    mcw.set_block(floor_block, pos)
                if is_edge:
                    if y in (0, floor_height):
                        mcw.set_block(wall_block, pos)
                    else:
                        mcw.set_block(window_block, pos)
                if dx in (0, width - 1) and dz in (0, depth - 1):
                    mcw.set_block(column_block, pos)
                    
    if floor == 0:
        mcw.set_block(mc.Block("stone bricks stairs").withData({"facing": "south"}), pos)


# -----------------------------------------------------------------------------------------

mc.postToChat("Стройка дома Кати...")

for f in range(floors):
    floor(start, f, floor_height)

mcw.draw()
mc.postToChat("Стройка дома завершена!")
