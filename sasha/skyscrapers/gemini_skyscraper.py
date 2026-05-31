import random
from typing import Literal
from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('192.168.1.88')
mcw = MinecraftWrap(mc)

start = Vec3(-1200, 67, -800)

floors = 20
floor_height = 5
width = 19
depth = 15

# Upgraded color palette for a high-tech modern look
wall_block = mc.Block("cyan_terracotta")
glass_block = mc.Block("black_stained_glass_pane")
floor_block = mc.Block("smooth_stone")
pillar_block = mc.Block("stripped_dark_oak_log")
roof_block = mc.Block("stone_bricks")
antenna_block = mc.Block("iron_bars")
atrium_block = mc.Block("sea_lantern")
railing_block = mc.Block("dark_oak_fence")
accent_block = mc.Block("quartz_block")


def roof_with_helipad(pos: Vec3, block: Block):
    roof_shift = floors * floor_height

    # Base roof layer
    for dx in range(-1, width + 2):
        for dz in range(-1, depth + 2):
            mcw.set_block(block, pos + Vec3(dx, roof_shift, dz))

    # Helipad markings and structure
    helipad_y = roof_shift + 1
    cx = width // 2
    cz = depth // 2

    for dx in range(-4, 5):
        for dz in range(-4, 5):
            mcw.set_block(mc.Block("gray_concrete"), pos + Vec3(cx + dx, helipad_y, cz + dz))

    # Letter H for helipad
    for dz in range(-2, 3):
        mcw.set_block(accent_block, pos + Vec3(cx - 2, helipad_y, cz + dz))
        mcw.set_block(accent_block, pos + Vec3(cx + 2, helipad_y, cz + dz))
    for dx in range(-1, 2):
        mcw.set_block(accent_block, pos + Vec3(cx + dx, helipad_y, cz))


def modern_spire(pos: Vec3):
    roof_shift = floors * floor_height + 1

    # Place a tall modern spire on the side
    cx = width // 2 - 6
    cz = depth // 2

    for dy in range(12):
        mcw.set_block(mc.Block("iron_block"), pos + Vec3(cx, roof_shift + dy, cz))

    mcw.set_block(mc.Block("redstone_block"), pos + Vec3(cx, roof_shift + 12, cz))
    mcw.set_block(
        mc.Block("lightning_rod").withData({"facing": "up"}),
        pos + Vec3(cx, roof_shift + 13, cz)
    )


def table_with_lanterns(pos: Vec3):
    mcw.set_block(mc.Block("crafting table"), pos + Vec3(0, 0, 0))
    mcw.set_block(mc.Block("crafting table"), pos + Vec3(-1, 0, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(-1, 1, 0))


def storage(pos: Vec3, wood_type: str):
    log_positions = [Vec3(0, 1, 0), Vec3(0, 2, 0), Vec3(0, 3, 0)]
    for log_pos in log_positions:
        mcw.set_block(mc.Block(f"{wood_type} log"), log_pos + pos)
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 4, 0))

    chests_properties: list[tuple[Vec3, str]] = []

    for y in range(1, 4):
        chests_properties.extend([
            (Vec3(1, y, 0), "north"),
            (Vec3(2, y, 0), "north"),
            (Vec3(0, y, -1), "east"),
            (Vec3(0, y, -2), "east"),
            (Vec3(0, y, -3), "east")
        ])

    for p, direction in chests_properties:
        mcw.set_block(mc.Block("chest").withData({"facing": direction}), p + pos)


def atrium_and_pillars(pos: Vec3, light_block: Block, pillar_block: Block, floor_h: int):
    lighting_positions = []
    for dx in [-1, 0, 1]:
        for dz in [-1, 0, 1]:
            lighting_positions.append(Vec3(dx, 0, dz))

    for p in lighting_positions:
        mcw.set_block(light_block, p + pos)

    pillar_positions = []
    for y in range(1, floor_h):
        pillar_positions.extend([
            Vec3(-3, y, -3), Vec3(3, y, 3),
            Vec3(3, y, -3), Vec3(-3, y, 3)
        ])

    for p in pillar_positions:
        mcw.set_block(pillar_block, p + pos)


def sofa_with_table(wood_type: str, pos: Vec3):
    mcw.set_block(mc.Block(f"{wood_type} fence"), pos)
    mcw.set_block(mc.Block(f"{wood_type} pressure plate"), pos + Vec3(0, 1, 0))
    mcw.set_block(mc.Block(f"{wood_type} log"), pos + Vec3(2, 0, 2))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(2, 1, 2))

    stairs_properties = [
        (Vec3(0, 0, 2), "south"), (Vec3(1, 0, 2), "south"),
        (Vec3(2, 0, 1), "east"), (Vec3(2, 0, 0), "east")
    ]
    for p, direction in stairs_properties:
        mcw.set_block(
            mc.Block(f"{wood_type} stairs").withData({"facing": direction}),
            p + pos
        )


def bookshelves_and_lanterns(pos: Vec3):
    bookshelves_positions = []
    for y in range(0, 3):
        bookshelves_positions.extend([
            Vec3(0, y, 0), Vec3(-1, y, 0), Vec3(-2, y, 0),
            Vec3(0, y, 1), Vec3(0, y, 2)
        ])

    for p in bookshelves_positions:
        mcw.set_block(mc.Block("bookshelf"), p + pos)

    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 3, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(-2, 3, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(0, 3, 2))


def street_lamp(pos: Vec3, fence_material: str, facing: str):
    for dy in range(2, 5):
        mcw.set_block(f"{fence_material} fence", pos + Vec3(0, dy, 0))
    if facing == "south":
        mcw.set_block(f"{fence_material} fence", pos + Vec3(0, 4, 1))
        mcw.set_block(f"{fence_material} fence", pos + Vec3(-1, 4, 0))
        mcw.set_block(mc.Block("lantern").withData({"hanging": True}), pos + Vec3(0, 3, 1))
        mcw.set_block(mc.Block("lantern").withData({"hanging": True}), pos + Vec3(-1, 3, 0))
    elif facing == "north":
        mcw.set_block(f"{fence_material} fence", pos + Vec3(0, 4, -1))
        mcw.set_block(f"{fence_material} fence", pos + Vec3(-1, 4, 0))
        mcw.set_block(mc.Block("lantern").withData({"hanging": True}), pos + Vec3(0, 3, -1))
        mcw.set_block(mc.Block("lantern").withData({"hanging": True}), pos + Vec3(-1, 3, 0))


def ladder(pos: Vec3, floor: int, floor_height: int, max_floor: int):
    def even_floor():
        # Platform 1
        mcw.set_block_cube("quartz block", pos + Vec3(1, 0, -1), pos + Vec3(3, 0, -4))
        for dx in range(1, 5):
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(dx, 0, 0)
            )

        # Stairs
        stairs_y = 1
        for dz in range(5, 10):
            mcw.set_block("quartz stairs", pos + Vec3(1, stairs_y, -dz))
            mcw.set_block("quartz stairs", pos + Vec3(2, stairs_y, -dz))
            mcw.set_block(mc.Block(railing_block), pos + Vec3(3, stairs_y, -dz + 1))
            mcw.set_block(
                mc.Block("quartz stairs").withData({"facing": "south", "half": "top"}),
                pos + Vec3(3, stairs_y, -dz)
            )
            stairs_y += 1

        # Platform 2
        mcw.set_block_cube(
            "quartz block",
            pos + Vec3(1, floor_height, -10),
            pos + Vec3(3, floor_height, -13)
        )
        for dx in range(1, 4):
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(dx, floor_height, -14)
            )

    def odd_floor():
        # Platform 1
        mcw.set_block_cube("quartz block", pos + Vec3(6, 0, -10), pos + Vec3(4, 0, -13))

        for dx in range(1, 7):
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(dx, 0, -14)
            )
            mcw.set_block(mc.Block(railing_block), pos + Vec3(dx, 1, -14))
        for dz in range(10, 14):
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(6, 0, -dz)
            )
            mcw.set_block(mc.Block(railing_block), pos + Vec3(6, 1, -dz))

        street_lamp(pos + Vec3(6, 0, -14), fence_material="pale oak", facing="south")

        # Stairs
        stairs_y = 5
        for dz in range(5, 10):
            mcw.set_block(
                mc.Block("quartz stairs").withData({"facing": "south"}),
                pos + Vec3(4, stairs_y, -dz)
            )
            mcw.set_block(
                mc.Block("quartz stairs").withData({"facing": "south"}),
                pos + Vec3(5, stairs_y, -dz)
            )
            mcw.set_block(
                mc.Block("quartz stairs").withData({"facing": "north", "half": "top"}),
                pos + Vec3(6, stairs_y, -dz)
            )
            mcw.set_block(
                mc.Block("quartz stairs").withData({"facing": "north", "half": "top"}),
                pos + Vec3(3, stairs_y, -dz)
            )
            mcw.set_block(railing_block, pos + Vec3(6, stairs_y + 1, -dz))
            mcw.set_block(railing_block, pos + Vec3(3, stairs_y, -dz - 1))
            stairs_y -= 1

        # Platform 2
        mcw.set_block_cube(
            "quartz block",
            pos + Vec3(4, floor_height, -1),
            pos + Vec3(5, floor_height, -4)
        )

        for dx in range(1, 7):
            if dx >= 5:
                mcw.set_block(
                    mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(dx, floor_height, 0)
                )
            mcw.set_block(mc.Block(railing_block), pos + Vec3(dx, floor_height + 1, 0))
        for dz in range(1, 5):
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(6, floor_height, -dz)
            )
            mcw.set_block(mc.Block(railing_block), pos + Vec3(6, floor_height + 1, -dz))

        street_lamp(pos + Vec3(6, floor_height, 0), fence_material="pale oak", facing="north")

    if floor == 0:
        mcw.set_block_cube("quartz block", pos + Vec3(4, 0, 0), pos + Vec3(6, 0, -4))
        for dx in range(4, 7):
            mcw.set_block(railing_block, pos + Vec3(dx, 1, -4))
        for dz in range(0, 4):
            mcw.set_block(railing_block, pos + Vec3(6, 1, -dz))

        street_lamp(pos + Vec3(6, 0, 0), fence_material="pale oak", facing="north")

    elif floor == max_floor:
        if max_floor % 2 == 0:
            mcw.set_block(railing_block, pos + Vec3(3, floor_height + 1, -9))
            mcw.set_block(railing_block, pos + Vec3(4, floor_height + 1, -9))
            mcw.set_block(
                mc.Block("quartz slab").withData({"type": "top"}),
                pos + Vec3(4, floor_height, -9)
            )
            for dz in range(10, 15):
                mcw.set_block(
                    mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(4, floor_height, -dz)
                )
                mcw.set_block(railing_block, pos + Vec3(4, floor_height + 1, -dz))
            for dx in range(1, 4):
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, -14))
            street_lamp(
                pos + Vec3(4, floor_height, -14),
                fence_material="pale oak",
                facing="south"
            )
        else:
            mcw.set_block_cube(
                "quartz block",
                pos + Vec3(1, floor_height, -1),
                pos + Vec3(3, floor_height, -5)
            )
            for dx in range(1, 4):
                mcw.set_block(
                    mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(dx, floor_height, 0)
                )
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, 0))
                mcw.set_block(railing_block, pos + Vec3(dx, floor_height + 1, -5))

    if floor % 2 != 0:
        odd_floor()
    else:
        even_floor()


def build_floor(pos: Vec3, f_idx: int, f_height: int, f_block: Block, p_block: Block):
    floor_shift = Vec3(0, f_idx * f_height, 0)
    floor_start = start + floor_shift

    for y in range(f_height):
        for dx in range(width):
            for dz in range(depth):
                current_pos = floor_start + Vec3(dx, y, dz)

                # Outer framework logic
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_corner = dx in (0, width - 1) and dz in (0, depth - 1)

                if is_edge:
                    if is_corner:
                        # Structural quartz corners for a monolithic design
                        mcw.set_block(accent_block, current_pos)
                    elif 1 <= y <= 3:
                        # Panoramic tinted windows
                        mcw.set_block(glass_block, current_pos)
                    else:
                        mcw.set_block(wall_block, current_pos)
                else:
                    # Inner floor casting
                    mcw.set_block(f_block, floor_start + Vec3(dx, 0, dz))

    if f_idx != floors - 1:
        ladder(floor_start + Vec3(width - 1, 0, depth - 1), f_idx, f_height, floors - 2)

    atrium_and_pillars(
        floor_start + Vec3(width // 2, 0, depth // 2), atrium_block, p_block, f_height
    )

    # Furniture setup
    bed_colors: list[Literal[
        "red", "orange", "yellow", "lime", "green", "cyan",
        "light_blue", "blue", "purple", "magenta", "pink"
    ]] = [
        "red", "orange", "yellow", "lime", "green", "cyan",
        "light_blue", "blue", "purple", "magenta", "pink"
    ]
    rand_color = random.choice(bed_colors)

    mc.setBed(floor_start + Vec3(4, 1, 3), "north", rand_color)
    mc.setBed(floor_start + Vec3(3, 1, 3), "north", rand_color)
    mcw.set_block(mc.Block("crafting table"), floor_start + Vec3(2, 1, 2))
    mcw.set_block(mc.Block("lantern"), floor_start + Vec3(2, 2, 2))

    # Storage and alternating floor layouts
    storage(floor_start + Vec3(2, 0, depth - 3), "oak")

    if f_idx % 2 == 0:
        bookshelves_and_lanterns(floor_start + Vec3(width - 3, 1, 2))
        table_with_lanterns(floor_start + Vec3(width - 4, 1, depth - 2))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, depth - 3))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, depth - 3))
    else:
        sofa_with_table(mc.Block("oak"), floor_start + Vec3(width - 5, 1, depth - 5))
        table_with_lanterns(floor_start + Vec3(width - 4, 1, 1))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 1, 2))
        mcw.set_block(mc.Block("air"), floor_start + Vec3(width - 1, 2, 2))


# -----------------------------------------------------------------------------------------

mc.postToChat("Building advanced skyscraper...")

# Constructing floors
for f in range(floors):
    build_floor(start, f, floor_height, floor_block, pillar_block)

# Constructing upgraded roof and spire
roof_with_helipad(start, roof_block)
modern_spire(start)

mcw.draw()
mc.postToChat("Skyscraper construction completed successfully!")
