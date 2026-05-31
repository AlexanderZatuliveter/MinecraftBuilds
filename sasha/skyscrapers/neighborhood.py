from common.minecraft_wrap import MinecraftWrap
from pathlib import Path
import sys

from mcpq import Block, Minecraft, Vec3

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


mc = Minecraft("192.168.1.66")
mcw = MinecraftWrap(mc)

# The skyscraper already exists at this anchor; this script builds the district around it.
tower_start = Vec3(-1, 70, -718)

road_block = mc.Block("stone bricks")
sidewalk_block = mc.Block("smooth stone")
plaza_block = mc.Block("polished andesite")
accent_block = mc.Block("light gray concrete")

lamp_pole_block = mc.Block("dark oak fence")
lamp_top_block = mc.Block("lantern").withData({"hanging": True})


def fill_rect(block: Block | str, pos1: Vec3, pos2: Vec3):
    mcw.set_block_cube(block, pos1, pos2)


def build_path_line(block: Block | str, start: Vec3, end: Vec3):
    if start.x == end.x:
        x = start.x
        z1 = min(start.z, end.z)
        z2 = max(start.z, end.z)
        fill_rect(block, Vec3(x, start.y, z1), Vec3(x, start.y, z2))
    elif start.z == end.z:
        z = start.z
        x1 = min(start.x, end.x)
        x2 = max(start.x, end.x)
        fill_rect(block, Vec3(x1, start.y, z), Vec3(x2, start.y, z))
    else:
        raise ValueError("Path lines must be straight")


def build_street_lamp(pos: Vec3):
    mcw.set_block(lamp_pole_block, pos + Vec3(0, 1, 0))
    mcw.set_block(lamp_pole_block, pos + Vec3(0, 2, 0))
    mcw.set_block(lamp_pole_block, pos + Vec3(0, 3, 0))
    mcw.set_block(lamp_top_block, pos + Vec3(0, 4, 0))


def build_balcony(pos: Vec3, width: int, facing: str):
    if facing in ("north", "south"):
        for dx in range(width):
            mcw.set_block(sidewalk_block, pos + Vec3(dx, 0, 0))
            mcw.set_block(lamp_pole_block, pos + Vec3(dx, 1, 0))
    else:
        for dz in range(width):
            mcw.set_block(sidewalk_block, pos + Vec3(0, 0, dz))
            mcw.set_block(lamp_pole_block, pos + Vec3(0, 1, dz))


def build_flat_roof(pos: Vec3, width: int, depth: int, roof_y: int):
    fill_rect(plaza_block, pos + Vec3(-1, roof_y, -1), pos + Vec3(width, roof_y, depth))
    fill_rect(accent_block, pos + Vec3(0, roof_y + 1, 0), pos + Vec3(width - 1, roof_y + 1, depth - 1))


def build_townhouse(pos: Vec3, facing: str = "south"):
    width = 11
    depth = 9
    height = 9
    floor_block = mc.Block("smooth stone")
    wall_block = mc.Block("white concrete")
    window_block = mc.Block("light blue stained glass pane")
    trim_block = mc.Block("light gray concrete")
    roof_block = mc.Block("stone bricks")
    stair_block = mc.Block("stone brick stairs")

    fill_rect(floor_block, pos, pos + Vec3(width - 1, 0, depth - 1))

    for y in range(1, height):
        for dx in range(width):
            for dz in range(depth):
                edge = dx in (0, width - 1) or dz in (0, depth - 1)
                if not edge:
                    continue
                p = pos + Vec3(dx, y, dz)
                is_window_row = 2 <= y <= 5 and (
                    (dz in (0, depth - 1) and 2 <= dx <= width - 3 and dx % 2 == 0)
                    or (dx in (0, width - 1) and 2 <= dz <= depth - 3 and dz % 2 == 0)
                )
                mcw.set_block(window_block if is_window_row else wall_block, p)

        if y in (3, 6):
            fill_rect(trim_block, pos + Vec3(0, y, 0), pos + Vec3(width - 1, y, depth - 1))

    fill_rect(roof_block, pos + Vec3(0, height, 0), pos + Vec3(width - 1, height, depth - 1))
    for dx in range(width):
        mcw.set_block(stair_block.withData({"facing": "south", "half": "top"}), pos + Vec3(dx, height + 1, 0))
        mcw.set_block(stair_block.withData({"facing": "north", "half": "top"}), pos + Vec3(dx, height + 1, depth - 1))

    door_x = width // 2
    if facing == "south":
        fill_rect(plaza_block, pos + Vec3(door_x - 1, 1, depth), pos + Vec3(door_x + 1, 1, depth + 1))
        mcw.set_block(mc.Block("oak door").withData({"facing": "south"}), pos + Vec3(door_x, 1, depth - 1))
        build_street_lamp(pos + Vec3(door_x - 3, 0, depth + 1))
    elif facing == "north":
        fill_rect(plaza_block, pos + Vec3(door_x - 1, 1, -2), pos + Vec3(door_x + 1, 1, -1))
        mcw.set_block(mc.Block("oak door").withData({"facing": "north"}), pos + Vec3(door_x, 1, 0))
        build_street_lamp(pos + Vec3(door_x + 3, 0, -2))
    elif facing == "east":
        fill_rect(plaza_block, pos + Vec3(width, 1, door_x - 1), pos + Vec3(width + 1, 1, door_x + 1))
        mcw.set_block(mc.Block("oak door").withData({"facing": "east"}), pos + Vec3(width - 1, 1, door_x))
        build_street_lamp(pos + Vec3(width + 1, 0, door_x - 3))
    else:
        fill_rect(plaza_block, pos + Vec3(-2, 1, door_x - 1), pos + Vec3(-1, 1, door_x + 1))
        mcw.set_block(mc.Block("oak door").withData({"facing": "west"}), pos + Vec3(0, 1, door_x))
        build_street_lamp(pos + Vec3(-2, 0, door_x + 3))


def build_cottage(pos: Vec3, facing: str = "north"):
    width = 11
    depth = 9
    height = 6
    floor_block = mc.Block("oak planks")
    wall_block = mc.Block("spruce planks")
    window_block = mc.Block("light blue stained glass pane")
    roof_block = mc.Block("dark oak planks")
    trim_block = mc.Block("spruce stairs")

    fill_rect(floor_block, pos, pos + Vec3(width - 1, 0, depth - 1))

    for y in range(1, height):
        for dx in range(width):
            for dz in range(depth):
                edge = dx in (0, width - 1) or dz in (0, depth - 1)
                if not edge:
                    continue
                p = pos + Vec3(dx, y, dz)
                is_window_row = 2 <= y <= 4 and (
                    (dz in (0, depth - 1) and 2 <= dx <= width - 3 and dx % 2 == 1)
                    or (dx in (0, width - 1) and 2 <= dz <= depth - 3 and dz % 2 == 1)
                )
                mcw.set_block(window_block if is_window_row else wall_block, p)

    roof_layers = 3
    for layer in range(roof_layers):
        fill_rect(
            roof_block,
            pos + Vec3(layer, height + layer, layer),
            pos + Vec3(width - 1 - layer, height + layer, depth - 1 - layer),
        )

    fill_rect(
        trim_block,
        pos +
        Vec3(
            0,
            height +
            roof_layers,
            0),
        pos +
        Vec3(
            width -
            1,
            height +
            roof_layers,
            depth -
            1))
    mcw.set_block(mc.Block("cobblestone wall"), pos + Vec3(2, 2, 0))
    mcw.set_block(mc.Block("cobblestone wall"), pos + Vec3(width - 3, 2, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(2, 3, 0))
    mcw.set_block(mc.Block("lantern"), pos + Vec3(width - 3, 3, 0))

    if facing == "north":
        mcw.set_block(mc.Block("oak door").withData({"facing": "north"}), pos + Vec3(width // 2, 1, 0))
        fill_rect(sidewalk_block, pos + Vec3(width // 2 - 1, 1, -2), pos + Vec3(width // 2 + 1, 1, -1))
    elif facing == "south":
        mcw.set_block(mc.Block("oak door").withData({"facing": "south"}), pos + Vec3(width // 2, 1, depth - 1))
        fill_rect(sidewalk_block, pos + Vec3(width // 2 - 1, 1, depth), pos + Vec3(width // 2 + 1, 1, depth + 1))
    elif facing == "east":
        mcw.set_block(mc.Block("oak door").withData({"facing": "east"}), pos + Vec3(width - 1, 1, depth // 2))
        fill_rect(sidewalk_block, pos + Vec3(width, 1, depth // 2 - 1), pos + Vec3(width + 1, 1, depth // 2 + 1))
    else:
        mcw.set_block(mc.Block("oak door").withData({"facing": "west"}), pos + Vec3(0, 1, depth // 2))
        fill_rect(sidewalk_block, pos + Vec3(-2, 1, depth // 2 - 1), pos + Vec3(-1, 1, depth // 2 + 1))


def build_villa(pos: Vec3, facing: str = "west"):
    width = 13
    depth = 11
    height = 9
    floor_block = mc.Block("cherry planks")
    wall_block = mc.Block("smooth sandstone")
    window_block = mc.Block("pink stained glass pane")
    trim_block = mc.Block("cut sandstone")
    roof_block = mc.Block("white concrete")
    roof_cap = mc.Block("quartz slab").withData({"type": "top"})

    fill_rect(floor_block, pos, pos + Vec3(width - 1, 0, depth - 1))

    for y in range(1, height):
        for dx in range(width):
            for dz in range(depth):
                edge = dx in (0, width - 1) or dz in (0, depth - 1)
                if not edge:
                    continue
                p = pos + Vec3(dx, y, dz)
                is_window_row = 2 <= y <= 5 and (
                    (dz in (0, depth - 1) and 2 <= dx <= width - 3 and dx % 3 != 0)
                    or (dx in (0, width - 1) and 2 <= dz <= depth - 3 and dz % 3 != 0)
                )
                mcw.set_block(window_block if is_window_row else wall_block, p)

        if y == 3:
            fill_rect(trim_block, pos + Vec3(0, y, 0), pos + Vec3(width - 1, y, depth - 1))

    fill_rect(roof_block, pos + Vec3(1, height, 1), pos + Vec3(width - 2, height, depth - 2))
    fill_rect(roof_cap, pos + Vec3(0, height + 1, 0), pos + Vec3(width - 1, height + 1, depth - 1))

    for x in (2, width - 3):
        mcw.set_block(mc.Block("quartz pillar"), pos + Vec3(x, 1, 0))
        mcw.set_block(mc.Block("quartz pillar"), pos + Vec3(x, 1, depth - 1))
        mcw.set_block(mc.Block("lantern"), pos + Vec3(x, 4, 0))
        mcw.set_block(mc.Block("lantern"), pos + Vec3(x, 4, depth - 1))

    build_balcony(pos + Vec3(2, 6, depth), width - 4, "south")
    build_balcony(pos + Vec3(2, 6, -1), width - 4, "north")

    if facing == "west":
        mcw.set_block(mc.Block("oak door").withData({"facing": "west"}), pos + Vec3(0, 1, depth // 2))
        fill_rect(sidewalk_block, pos + Vec3(-2, 1, depth // 2 - 1), pos + Vec3(-1, 1, depth // 2 + 1))
        build_street_lamp(pos + Vec3(-3, 0, depth // 2 + 3))
    elif facing == "east":
        mcw.set_block(mc.Block("oak door").withData({"facing": "east"}), pos + Vec3(width - 1, 1, depth // 2))
        fill_rect(sidewalk_block, pos + Vec3(width, 1, depth // 2 - 1), pos + Vec3(width + 1, 1, depth // 2 + 1))
        build_street_lamp(pos + Vec3(width + 1, 0, depth // 2 - 3))
    elif facing == "north":
        mcw.set_block(mc.Block("oak door").withData({"facing": "north"}), pos + Vec3(width // 2, 1, 0))
        fill_rect(sidewalk_block, pos + Vec3(width // 2 - 1, 1, -2), pos + Vec3(width // 2 + 1, 1, -1))
        build_street_lamp(pos + Vec3(width // 2 + 3, 0, -3))
    else:
        mcw.set_block(mc.Block("oak door").withData({"facing": "south"}), pos + Vec3(width // 2, 1, depth - 1))
        fill_rect(sidewalk_block, pos + Vec3(width // 2 - 1, 1, depth), pos + Vec3(width // 2 + 1, 1, depth + 1))
        build_street_lamp(pos + Vec3(width // 2 - 3, 0, depth + 2))


def build_plaza(anchor: Vec3):
    fill_rect(plaza_block, anchor, anchor + Vec3(15, 0, 13))
    fill_rect(sidewalk_block, anchor + Vec3(2, 0, 2), anchor + Vec3(13, 0, 11))
    fill_rect(accent_block, anchor + Vec3(6, 0, 5), anchor + Vec3(9, 0, 8))
    for dx in (1, 14):
        for dz in (1, 12):
            build_street_lamp(anchor + Vec3(dx, 0, dz))
    fill_rect(mc.Block("spruce stairs").withData({"facing": "north"}), anchor + Vec3(5, 1, 5), anchor + Vec3(10, 1, 5))
    fill_rect(mc.Block("spruce stairs").withData({"facing": "south"}), anchor + Vec3(5, 1, 8), anchor + Vec3(10, 1, 8))


def build_district():
    mc.postToChat("Строю район вокруг небоскреба...")

    north_road_z = tower_start.z - 26
    south_road_z = tower_start.z + 20
    west_road_x = tower_start.x - 26
    east_road_x = tower_start.x + 22

    fill_rect(
        road_block,
        Vec3(
            west_road_x,
            tower_start.y,
            north_road_z),
        Vec3(
            east_road_x +
            18,
            tower_start.y,
            north_road_z +
            2))
    fill_rect(
        road_block,
        Vec3(
            west_road_x,
            tower_start.y,
            south_road_z),
        Vec3(
            east_road_x +
            18,
            tower_start.y,
            south_road_z +
            2))
    fill_rect(
        road_block,
        Vec3(
            west_road_x,
            tower_start.y,
            north_road_z),
        Vec3(
            west_road_x +
            2,
            tower_start.y,
            south_road_z +
            2))
    fill_rect(
        road_block,
        Vec3(
            east_road_x + 15,
            tower_start.y,
            north_road_z),
        Vec3(
            east_road_x + 17,
            tower_start.y,
            south_road_z + 2))

    build_path_line(
        sidewalk_block,
        Vec3(
            tower_start.x + 9,
            tower_start.y,
            tower_start.z - 4),
        Vec3(
            tower_start.x + 9,
            tower_start.y,
            north_road_z + 1))
    build_path_line(
        sidewalk_block,
        Vec3(
            tower_start.x + 9,
            tower_start.y,
            tower_start.z + 18),
        Vec3(
            tower_start.x + 9,
            tower_start.y,
            south_road_z))

    build_plaza(Vec3(east_road_x + 4, tower_start.y, tower_start.z - 10))

    build_townhouse(Vec3(tower_start.x - 37, tower_start.y, tower_start.z - 42), facing="south")
    build_cottage(Vec3(tower_start.x + 23, tower_start.y, tower_start.z - 42), facing="south")
    build_villa(Vec3(tower_start.x - 37, tower_start.y, tower_start.z + 38), facing="east")

    for x in range(tower_start.x - 30, tower_start.x + 26, 8):
        build_street_lamp(Vec3(x, tower_start.y, north_road_z + 1))
        build_street_lamp(Vec3(x, tower_start.y, south_road_z + 1))

    mcw.draw()
    mc.postToChat("Район вокруг небоскреба завершен!")


if __name__ == "__main__":
    build_district()
