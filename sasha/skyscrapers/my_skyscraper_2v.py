from typing import Literal
from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('localhost')
mcw = MinecraftWrap(mc)

start = Vec3(450, 62, 425)

width = 15
room_depth = 14
depth = room_depth * 2 + 5
floor_height = 5
floors = 3

wall_block = mc.Block("light gray concrete")
roof_block = mc.Block("gray concrete")
floor_block = mc.Block("stone bricks")
window_block = mc.Block("glass pane")
ladder_block = mc.Block("stone brick stairs")
railings_block = mc.Block("oak fence")
lantern_block = mc.Block("lantern")


def lighting(pos: Vec3):
    mcw.set_block(lantern_block.withData({"hanging": True}), pos + Vec3(3, floor_height - 1, 3))
    mcw.set_block(lantern_block.withData({"hanging": True}), pos + Vec3(3, floor_height - 1, room_depth - 4))
    mcw.set_block(lantern_block.withData({"hanging": True}), pos + Vec3(width - 4, floor_height - 1, 3))
    mcw.set_block(lantern_block.withData({"hanging": True}), pos + Vec3(width - 4, floor_height - 1, room_depth - 4))
    mcw.set_block(lantern_block.withData({"hanging": True}), pos + Vec3(width // 2, floor_height - 1, room_depth // 2))
    mcw.set_block(lantern_block.withData({"hanging": True}), pos +
                  Vec3(width // 2, floor_height - 1, room_depth // 2 - 1))


def library(pos: Vec3, room_side: Literal["left", "right"], enter_pos: Literal["near", "far"]):
    lighting(pos)

    def table(pos: Vec3):
        for dz in range(3):
            mcw.set_block(mc.Block("oak stairs").withData({"facing": "east"}), pos + Vec3(0, 0, dz))
            mcw.set_block(mc.Block("oak fence"), pos + Vec3(-1, 0, dz))
            mcw.set_block(mc.Block("oak pressure plate"), pos + Vec3(-1, 1, dz))
            mcw.set_block(mc.Block("oak stairs").withData({"facing": "west"}), pos + Vec3(-2, 0, dz))

    if enter_pos == "near":
        x1 = width - 3
        x2 = width - 8
    if enter_pos == "far":
        x1 = width - 6
        x2 = width - 11

    if room_side == "left":

        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(2, 1, 3), pos + Vec3(2, 3, 5))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(5, 1, 3), pos + Vec3(5, 3, 5))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(9, 1, 3), pos + Vec3(9, 3, 5))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(12, 1, 3), pos + Vec3(12, 3, 5))

        table(pos + Vec3(x1, 1, room_depth - 6))
        table(pos + Vec3(x2, 1, room_depth - 6))

    if room_side == "right":

        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(2, 1, room_depth - 4), pos + Vec3(2, 3, room_depth - 6))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(5, 1, room_depth - 4), pos + Vec3(5, 3, room_depth - 6))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(9, 1, room_depth - 4), pos + Vec3(9, 3, room_depth - 6))
        mcw.set_block_cube(mc.Block("bookshelf"), pos + Vec3(12, 1, room_depth - 4), pos + Vec3(12, 3, room_depth - 6))

        table(pos + Vec3(x1, 1, 3))
        table(pos + Vec3(x2, 1, 3))


def bedroom(pos: Vec3, room_side: Literal["left", "right"], enter_pos: Literal["near", "far"]):
    lighting(pos)

    def set_bed(pos: Vec3, color: Literal["blue", "red"], direction: Literal["south", "north"]):
        if direction == "south":
            mc.setBed(pos, direction, color)
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "east", "half": "bottom", "open": True}), pos + Vec3(1, 0, 0))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "east", "half": "bottom", "open": True}), pos + Vec3(1, 0, 1))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "south", "half": "bottom", "open": True}), pos + Vec3(0, 0, 2))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "south", "half": "bottom", "open": True}), pos + Vec3(-1, 0, 2))
            mcw.set_block(mc.Block("ladder").withData({"facing": "north"}), pos + Vec3(-1, 0, 1))
        else:
            mc.setBed(pos, direction, color)
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "east", "half": "bottom", "open": True}), pos + Vec3(1, 0, -1))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "east", "half": "bottom", "open": True}), pos + Vec3(1, 0, 0))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "north", "half": "bottom", "open": True}), pos + Vec3(0, 0, -2))
            mcw.set_block(mc.Block("spruce trapdoor").withData(
                {"facing": "north", "half": "bottom", "open": True}), pos + Vec3(-1, 0, -2))
            mcw.set_block(mc.Block("ladder").withData({"facing": "south"}), pos + Vec3(-1, 0, -1))

    if enter_pos == "near":
        x1 = width - 4
        x2 = width - 13
        x3 = width - 4
        x4 = width - 9
    else:
        x1 = width - 3
        x2 = width - 12
        x3 = width - 7
        x4 = width - 12

    for dy in range(1, 3):
        if room_side == "right":
            for dx in range(x1, x2, -4):
                set_bed(pos + Vec3(dx, dy, room_depth - 5), direction="south", color="red")
            for dx in range(x3, x4, -4):
                set_bed(pos + Vec3(dx, dy, 3), direction="south", color="blue")
        else:
            for dx in range(x1, x2, -4):
                set_bed(pos + Vec3(dx, dy, 4), direction="north", color="red")
            for dx in range(x3, x4, -4):
                set_bed(pos + Vec3(dx, dy, room_depth - 4), direction="north", color="blue")


def storage(pos: Vec3, enter_pos: Literal["near", "far"]):

    # In this function the room_side is not important.

    lighting(pos)

    if enter_pos == "near":
        pattern = ["right_chest", "left_chest", "log"]
        direction = "west"
        x1, x2 = 5, 12
    else:
        pattern = ["left_chest", "right_chest", "log"]
        direction = "east"
        x1, x2 = 3, 10

    for dx in range(x1, x2, 3):
        for dy in range(1, 4):
            for i, dz in enumerate(range(3, 11)):
                block_type = pattern[i % 3]

                if block_type == "log":
                    mcw.set_block(mc.Block("oak log").withData({"axis": "y"}), pos + Vec3(dx, dy, dz))
                elif block_type == "right_chest":
                    mcw.set_block(mc.Block("chest").withData(
                        {"facing": direction, "type": "right"}), pos + Vec3(dx, dy, dz))
                elif block_type == "left_chest":
                    mcw.set_block(mc.Block("chest").withData(
                        {"facing": direction, "type": "left"}), pos + Vec3(dx, dy, dz))


def workroom(pos: Vec3, room_side: Literal["left", "right"], enter_pos: Literal["near", "far"]):
    lighting(pos)

    def furnace_angle(pos: Vec3, direction: Literal["south-east", "north-east", "south-west", "north-west"]):
        mcw.set_block_cube(mc.Block("oak log"), pos + Vec3(0, 1, 0), pos + Vec3(0, 3, 0))
        if direction == "south-east":
            mcw.set_block_cube(mc.Block("furnace").withData(
                {"facing": "south"}), pos + Vec3(1, 1, 0), pos + Vec3(3, 3, 0))
            mcw.set_block_cube(mc.Block("blast furnace").withData(
                {"facing": "east"}), pos + Vec3(0, 1, 1), pos + Vec3(0, 3, 3))
        elif direction == "north-east":
            mcw.set_block_cube(mc.Block("blast furnace").withData(
                {"facing": "north"}), pos + Vec3(1, 1, 0), pos + Vec3(3, 3, 0))
            mcw.set_block_cube(mc.Block("furnace").withData(
                {"facing": "east"}), pos + Vec3(0, 1, -1), pos + Vec3(0, 3, -3))
        elif direction == "south-west":
            mcw.set_block_cube(mc.Block("blast furnace").withData(
                {"facing": "south"}), pos + Vec3(-1, 1, 0), pos + Vec3(-3, 3, 0))
            mcw.set_block_cube(mc.Block("furnace").withData(
                {"facing": "west"}), pos + Vec3(0, 1, 1), pos + Vec3(0, 3, 3))
        elif direction == "north-west":
            mcw.set_block_cube(mc.Block("furnace").withData(
                {"facing": "north"}), pos + Vec3(-1, 1, 0), pos + Vec3(-3, 3, 0))
            mcw.set_block_cube(mc.Block("blast furnace").withData(
                {"facing": "west"}), pos + Vec3(0, 1, -1), pos + Vec3(0, 3, -3))

    # Carpet

    light_carpet = mc.Block("light gray carpet")
    dark_carpet = mc.Block("gray carpet")

    for dx in range(3, width - 3):
        for dz in range(3, room_depth - 3):
            is_dark_carpet = (
                dx in (3, width - 4, (width - 1) // 2) or
                dz in (3, room_depth - 4)
            )

            block_pos = pos + Vec3(dx, 1, dz)

            if is_dark_carpet:
                mcw.set_block(dark_carpet, block_pos)
            else:
                mcw.set_block(light_carpet, block_pos)

    if enter_pos == "near" and room_side == "left":
        furnace_angle(pos + Vec3(2, 0, 2), "south-east")
        furnace_angle(pos + Vec3(width - 3, 0, 2), "south-west")
        furnace_angle(pos + Vec3(width - 3, 0, room_depth - 3), "north-west")
    elif enter_pos == "near" and room_side == "right":
        furnace_angle(pos + Vec3(width - 3, 0, room_depth - 3), "north-west")
        furnace_angle(pos + Vec3(width - 3, 0, 2), "south-west")
        furnace_angle(pos + Vec3(2, 0, room_depth - 3), "north-east")
    elif enter_pos == "far" and room_side == "left":
        furnace_angle(pos + Vec3(2, 0, 2), "south-east")
        furnace_angle(pos + Vec3(width - 3, 0, 2), "south-west")
        furnace_angle(pos + Vec3(2, 0, room_depth - 3), "north-east")
    elif enter_pos == "far" and room_side == "right":
        furnace_angle(pos + Vec3(2, 0, 2), "south-east")
        furnace_angle(pos + Vec3(2, 0, room_depth - 3), "north-east")
        furnace_angle(pos + Vec3(width - 3, 0, room_depth - 3), "north-west")

    for dz in range(room_depth // 2 - 1, room_depth // 2 + 1):
        mcw.set_block(mc.Block("anvil"), pos + Vec3(5, 1, dz))
        mcw.set_block(mc.Block("stonecutter"), pos + Vec3(6, 1, dz))
        mcw.set_block(mc.Block("grindstone").withData({"face": "floor"}), pos + Vec3(7, 1, dz))
        mcw.set_block(mc.Block("stonecutter"), pos + Vec3(8, 1, dz))
        mcw.set_block(mc.Block("anvil"), pos + Vec3(9, 1, dz))


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
        pos1 = pos + Vec3(10, floor_height, depth // 2 + 2)
        pos2 = pos + Vec3(13, floor_height, depth // 2 - 2)
        mcw.set_block_cube(floor_block, pos1, pos2)
    else:
        dx = 9
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
            dz = depth // 3.25 * i + 2
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
                is_window = is_edge and y not in (0, floor_height - 1, floor_height) and not is_enter and not is_column
                is_floor = y == 0 and dx not in (0, width - 1) and dz not in (0, depth - 1) \
                    and (pos.y == start.y or dz not in [z for z in range(depth // 2 - 2, depth // 2 + 3)])

                if floor % 2 == 0:
                    is_dividing_wall = dz in (depth // 2 - 3, depth // 2 + 3) and dx not in (2, 3) \
                        or (dz in (depth // 2 - 3, depth // 2 + 3) and dx in (2, 3) and y == 4)
                else:
                    is_dividing_wall = dz in (depth // 2 - 3, depth // 2 + 3) and dx not in (11, 12) \
                        or (dz in (depth // 2 - 3, depth // 2 + 3) and dx in (11, 12) and y == 4)

                is_outside_wall = (dx in (0, width - 1) or dz in (0, depth - 1)) and y in (0, floor_height - 1, floor_height) \
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

# library(start + Vec3(0, 0, 0), room_side="left", enter_pos="near")
# library(start + Vec3(0, 0, 19), room_side="right", enter_pos="near")
# bedroom(start + Vec3(0, floor_height, 0), room_side="left", enter_pos="far")
# bedroom(start + Vec3(0, floor_height, 19), room_side="right", enter_pos="far")
# storage(start + Vec3(0, floor_height * 2, 0), enter_pos="near")
# storage(start + Vec3(0, floor_height * 2, 19), enter_pos="near")

workroom(start, room_side="left", enter_pos="near")
workroom(start + Vec3(0, 0, 19), room_side="right", enter_pos="near")
workroom(start + Vec3(0, floor_height, 0), room_side="left", enter_pos="far")
workroom(start + Vec3(0, floor_height, 19), room_side="right", enter_pos="far")

mcw.draw()
mc.postToChat("Стройка небоскреба завершена!")
