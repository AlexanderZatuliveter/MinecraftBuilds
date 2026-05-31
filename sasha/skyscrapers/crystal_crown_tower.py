"""
Crystal Crown Tower — архитектурный небоскрёб с атриумом, офисами,
пентхаусом, бассейном на крыше, обсерваторией и детализированным лобби.
Объединяет интерьеры Luxury Tower и атриум my_skyscraper.
"""

from common.minecraft_wrap import MinecraftWrap
import random
from pathlib import Path
import sys

from mcpq import Block, Minecraft, Vec3

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


mc = Minecraft("192.168.1.88")
mcw = MinecraftWrap(mc)

start = Vec3(-1200, 67, -750)

# ── размеры ──
floors = 22
floor_height = 5
width = 23
depth = 19

# ── палитра ──
wall_block = mc.Block("smooth quartz")
accent_wall = mc.Block("cyan terracotta")
dark_accent = mc.Block("deepslate tiles")
glass_block = mc.Block("light blue stained glass pane")
dark_glass = mc.Block("gray stained glass pane")
floor_block = mc.Block("polished deepslate")
floor_marble = mc.Block("quartz block")
ceiling_block = mc.Block("smooth stone")
pillar_block = mc.Block("cut copper")
pillar_gold = mc.Block("gold block")
roof_block = mc.Block("black concrete")
roof_slab = mc.Block("blackstone slab")
antenna_block = mc.Block("lightning rod")
railing_block = mc.Block("iron bars")
railing_wood = mc.Block("dark oak fence")
carpet_light = mc.Block("light blue carpet")
carpet_dark = mc.Block("cyan carpet")
carpet_gold = mc.Block("yellow carpet")
lantern_hang = mc.Block("sea lantern")
lantern_floor = mc.Block("sea lantern")
soul_lantern = mc.Block("soul lantern").withData({"hanging": True})
atrium_block = mc.Block("sea lantern")
pool_block = mc.Block("prismarine bricks")
water_block = mc.Block("water")
leaf_block = mc.Block("azalea leaves").withData({"persistent": True})
log_block = mc.Block("dark oak log")
grass_block = mc.Block("grass block")
plaza_block = mc.Block("polished diorite")
path_block = mc.Block("smooth stone")
hedge_block = mc.Block("spruce leaves").withData({"persistent": True})
light_strip = mc.Block("glowstone")
end_rod = mc.Block("end rod")


# ═══════════════════════  ВСПОМОГАТЕЛЬНЫЕ  ═══════════════════════

def fill(block, p1: Vec3, p2: Vec3):
    mcw.set_block_cube(block, p1, p2)


def place(block, pos: Vec3):
    mcw.set_block(block, pos)


def item_frame(pos: Vec3, facing: str = "south"):
    """Рамка на стене — entity, не блок (mcpq: spawnEntity)."""
    facings = {
        "north": Vec3().north(),
        "south": Vec3().south(),
        "east": Vec3().east(),
        "west": Vec3().west(),
    }
    frame = mc.spawnEntity("item_frame", pos)
    frame.teleport(facing=facings[facing])


# ═══════════════════════  ДЕКОР / МЕБЕЛЬ  ═══════════════════════

def grand_chandelier(center: Vec3, size: int = 2):
    """Большая люстра size×size из цепей и морских фонарей."""
    for dx in range(-size, size + 1):
        for dz in range(-size, size + 1):
            place(mc.Block("chain"), center + Vec3(dx, 0, dz))
            if abs(dx) + abs(dz) <= size:
                place(lantern_hang, center + Vec3(dx, -1, dz))
                if abs(dx) + abs(dz) <= size - 1:
                    place(lantern_hang, center + Vec3(dx, -2, dz))


def wall_lamp(pos: Vec3):
    place(mc.Block("dark oak fence"), pos)
    place(lantern_floor, pos + Vec3(0, 1, 0))


def floor_lamp(pos: Vec3):
    place(mc.Block("dark oak fence"), pos)
    place(mc.Block("dark oak fence"), pos + Vec3(0, 1, 0))
    place(lantern_floor, pos + Vec3(0, 2, 0))


def sofa(pos: Vec3, length: int, facing: str, wood: str = "dark_oak"):
    dx_dir = 1 if facing in ("north", "south") else 0
    dz_dir = 0 if facing in ("north", "south") else 1
    place(mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_left"}), pos)
    end = pos + Vec3(dx_dir * (length + 1), 0, dz_dir * (length + 1))
    place(mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_right"}), end)
    for i in range(1, length + 1):
        place(mc.Block(f"{wood} stairs").withData({"facing": facing}),
              pos + Vec3(dx_dir * i, 0, dz_dir * i))


def dining_table(pos: Vec3, length: int, direction: str = "x"):
    for i in range(length):
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        place(mc.Block("dark oak fence"), pos + offset)
        place(mc.Block("dark oak pressure plate"), pos + offset + Vec3(0, 1, 0))


def kitchen_counter(pos: Vec3, length: int, facing: str):
    blocks = ["furnace", "smoker", "blast_furnace", "crafting_table", "smoker", "brewing_stand"]
    for i in range(length):
        b = blocks[i % len(blocks)]
        if b == "crafting_table":
            place(mc.Block("crafting table"), pos + Vec3(i, 0, 0))
        elif b == "brewing_stand":
            place(mc.Block("brewing stand"), pos + Vec3(i, 0, 0))
        else:
            place(mc.Block(b).withData({"facing": facing}), pos + Vec3(i, 0, 0))
    for i in range(length):
        place(mc.Block("barrel").withData({"facing": "down"}), pos + Vec3(i, 2, 0))


def bed_set(pos: Vec3, direction: str, color: str):
    mc.setBed(pos, direction, color)
    place(mc.Block("oak trapdoor").withData({"facing": "west", "half": "bottom", "open": True}),
          pos + Vec3(1, 0, 0))
    place(mc.Block("oak trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
          pos + Vec3(-1, 0, 0))
    place(lantern_floor, pos + Vec3(1, 1, 0))
    place(lantern_floor, pos + Vec3(-1, 1, 0))


def bookshelf_wall(pos: Vec3, w: int, h: int):
    for dx in range(w):
        for dy in range(h):
            place(mc.Block("bookshelf"), pos + Vec3(dx, dy, 0))
    place(lantern_floor, pos + Vec3(0, h, 0))
    place(lantern_floor, pos + Vec3(w - 1, h, 0))


def flower_row(pos: Vec3, length: int, direction: str = "x"):
    flowers = ["potted_poppy", "potted_dandelion", "potted_blue_orchid",
               "potted_allium", "potted_azure_bluet", "potted_red_tulip",
               "potted_oxeye_daisy", "potted_cornflower", "potted_lily_of_the_valley",
               "potted_fern", "potted_bamboo"]
    for i in range(length):
        f = random.choice(flowers)
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        place(mc.Block(f), pos + offset)


def tree(pos: Vec3, trunk_h: int = 5):
    for dy in range(trunk_h):
        place(log_block, pos + Vec3(0, dy, 0))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in range(trunk_h, trunk_h + 3):
                if abs(dx) + abs(dz) <= 3 - (dy - trunk_h):
                    place(leaf_block, pos + Vec3(dx, dy, dz))


def fountain(center: Vec3, radius: int = 2):
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if abs(dx) == radius or abs(dz) == radius:
                place(pool_block, center + Vec3(dx, 0, dz))
            else:
                place(pool_block, center + Vec3(dx, -1, dz))
                place(water_block, center + Vec3(dx, 0, dz))
    for dy in range(1, 5):
        place(mc.Block("quartz pillar"), center + Vec3(0, dy, 0))
    place(water_block, center + Vec3(0, 5, 0))
    for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        place(lantern_floor, center + Vec3(dx, 1, dz))


def parking_car(pos: Vec3, color: str):
    fill(mc.Block(f"{color} concrete"), pos, pos + Vec3(1, 0, 3))
    for dz in (1, 2):
        place(mc.Block("glass"), pos + Vec3(0, 1, dz))
        place(mc.Block("glass"), pos + Vec3(1, 1, dz))
    fill(mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 0), pos + Vec3(1, 1, 0))
    fill(mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 3), pos + Vec3(1, 1, 3))
    for wx, wz in [(-1, 0), (-1, 3), (2, 0), (2, 3)]:
        place(mc.Block("stone button").withData({"facing": "west" if wx < 0 else "east", "face": "floor"}),
              pos + Vec3(wx, 0, wz))


def elevator_doors(pos: Vec3, facing: str = "south"):
    for dy in range(1, 4):
        place(mc.Block("iron_door").withData({"facing": facing, "half": "lower" if dy == 1 else "upper"}),
              pos + Vec3(0, dy, 0))
        place(mc.Block("iron_door").withData({"facing": facing, "half": "lower" if dy == 1 else "upper"}),
              pos + Vec3(1, dy, 0))
    place(mc.Block("stone button").withData({"facing": facing}), pos + Vec3(-1, 2, 0))


def office_desk(pos: Vec3, facing: str):
    place(mc.Block("spruce stairs").withData({"facing": facing}), pos)
    place(mc.Block("dark oak pressure plate"), pos + Vec3(0, 1, 0))
    place(mc.Block("flower pot"), pos + Vec3(1, 1, 0))


def gym_equipment(pos: Vec3):
    place(mc.Block("anvil"), pos)
    place(mc.Block("grindstone"), pos + Vec3(2, 0, 0))
    place(mc.Block("iron block"), pos + Vec3(4, 0, 0))
    place(mc.Block("iron block"), pos + Vec3(4, 1, 0))
    place(mc.Block("iron trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
          pos + Vec3(4, 2, 0))


def atrium_lighting(center: Vec3, radius: int = 2):
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if abs(dx) + abs(dz) <= radius + 1:
                place(atrium_block, center + Vec3(dx, 0, dz))


def facade_pillars(fp: Vec3):
    """Угловые колонны и вертикальные медные полосы."""
    corners = [(0, 0), (width - 1, 0), (0, depth - 1), (width - 1, depth - 1)]
    for cx, cz in corners:
        for dy in range(1, floor_height):
            place(pillar_block, fp + Vec3(cx, dy, cz))
    for dx in (3, width // 2, width - 4):
        for dy in range(1, floor_height - 1):
            place(accent_wall, fp + Vec3(dx, dy, 0))
            place(accent_wall, fp + Vec3(dx, dy, depth - 1))


def ceiling_y(pos: Vec3) -> Vec3:
    return pos + Vec3(0, floor_height - 1, 0)


def wall_sconce(pos: Vec3):
    """Бра: медная плита + end rod."""
    place(accent_wall, pos)
    place(end_rod, pos + Vec3(0, 1, 0))


def strip_lights(pos: Vec3, length: int, direction: str = "x"):
    for i in range(length):
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        place(light_strip, pos + offset)


def recessed_ceiling(pos: Vec3):
    """Точечный светильник в потолке."""
    place(lantern_floor, pos)
    place(mc.Block("chain"), pos + Vec3(0, 1, 0))


def lighting_grid(pos: Vec3, step_x: int = 5, step_z: int = 4,
                  skip_atrium: bool = True, skip_stairs: bool = True):
    """Равномерная сетка потолочного света по этажу."""
    mid_x = width // 2
    mid_z = depth // 2
    stair_x = width - 5
    for dx in range(3, width - 3, step_x):
        for dz in range(3, depth - 3, step_z):
            if skip_atrium and abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                continue
            if skip_stairs and dx >= stair_x - 1:
                continue
            recessed_ceiling(ceiling_y(pos) + Vec3(dx, 0, dz))


def corridor_lights(pos: Vec3, path: list[tuple[int, int]]):
    for dx, dz in path:
        recessed_ceiling(ceiling_y(pos) + Vec3(dx, 0, dz))
        wall_sconce(pos + Vec3(dx, 2, dz))


def room_divider(pos: Vec3, length: int, direction: str = "x", door_at: int | None = None):
    """Перегородка с дверным проёмом."""
    for i in range(length):
        if door_at is not None and i in (door_at, door_at + 1):
            continue
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        for dy in range(1, floor_height - 1):
            place(accent_wall, pos + offset + Vec3(0, dy, 0))


def bathroom(pos: Vec3):
    """Ванная: плитка, душ, раковина, зеркало."""
    fill(dark_accent, pos, pos + Vec3(3, 0, 3))
    place(mc.Block("cauldron"), pos + Vec3(1, 1, 1))
    place(mc.Block("cauldron"), pos + Vec3(2, 1, 1))
    fill(mc.Block("glass pane"), pos + Vec3(0, 2, 1), pos + Vec3(0, 3, 2))
    place(mc.Block("iron trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
          pos + Vec3(3, 1, 2))
    place(lantern_floor, pos + Vec3(2, 3, 2))
    place(carpet_light, pos + Vec3(1, 1, 3))
    place(carpet_light, pos + Vec3(2, 1, 3))


def fireplace(pos: Vec3):
    """Камин с облицовкой и подсветкой."""
    for dx in (-1, 0, 1):
        for dy in range(1, 5):
            place(mc.Block("bricks"), pos + Vec3(dx, dy, 0))
    place(mc.Block("campfire").withData({"lit": True}), pos + Vec3(0, 1, 0))
    place(soul_lantern, pos + Vec3(0, 4, 0))


def tv_wall(pos: Vec3, w: int = 3, h: int = 2):
    fill(mc.Block("black concrete"), pos, pos + Vec3(w - 1, h - 1, 0))
    place(end_rod, pos + Vec3(w // 2, h, 0))
    place(mc.Block("oak trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
          pos + Vec3(0, -1, 0))
    place(mc.Block("oak trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
          pos + Vec3(w - 1, -1, 0))


def grand_piano(pos: Vec3):
    """Рояль из чёрно-белой шерсти."""
    fill(mc.Block("black wool"), pos, pos + Vec3(2, 0, 1))
    fill(mc.Block("white wool"), pos + Vec3(0, 1, 0), pos + Vec3(2, 1, 0))
    place(mc.Block("note block"), pos + Vec3(1, 1, 1))
    place(lantern_floor, pos + Vec3(1, 2, 0))


def jacuzzi(pos: Vec3):
    """Джакузи из призмарина с подсветкой."""
    fill(pool_block, pos, pos + Vec3(3, 0, 3))
    fill(water_block, pos + Vec3(1, 1, 1), pos + Vec3(2, 1, 2))
    for dx, dz in ((0, 0), (3, 0), (0, 3), (3, 3)):
        place(lantern_floor, pos + Vec3(dx, 1, dz))
    place(end_rod, pos + Vec3(1, 3, 1))


def meeting_table(pos: Vec3, length: int):
    fill(floor_marble, pos, pos + Vec3(length - 1, 0, 2))
    for i in range(length):
        place(mc.Block("dark oak fence"), pos + Vec3(i, 1, -1))
        place(mc.Block("dark oak fence"), pos + Vec3(i, 1, 3))
        place(mc.Block("spruce stairs").withData({"facing": "north"}), pos + Vec3(i, 1, 0))
        place(mc.Block("spruce stairs").withData({"facing": "south"}), pos + Vec3(i, 1, 2))
    grand_chandelier(ceiling_y(pos) + Vec3(length // 2, 0, 1), 1)


def cubicle(pos: Vec3, w: int, d: int):
    """Офисная кабинка с рабочим местом."""
    for dx in range(w):
        place(railing_wood, pos + Vec3(dx, 1, 0))
        place(railing_wood, pos + Vec3(dx, 1, d - 1))
    for dz in range(1, d - 1):
        place(railing_wood, pos + Vec3(0, 1, dz))
    office_desk(pos + Vec3(1, 1, 1), "south")
    recessed_ceiling(ceiling_y(pos) + Vec3(w // 2, 0, d // 2))


def aquarium(pos: Vec3, w: int, h: int):
    """Акварium: стекло + вода + кораллы."""
    for dx in range(w):
        for dy in range(h):
            place(glass_block, pos + Vec3(dx, dy, 0))
            place(glass_block, pos + Vec3(dx, dy, 2))
    for dy in range(1, h):
        place(glass_block, pos + Vec3(0, dy, 1))
        place(glass_block, pos + Vec3(w - 1, dy, 1))
    fill(water_block, pos + Vec3(1, 1, 1), pos + Vec3(w - 2, h - 2, 1))
    place(mc.Block("brain coral"), pos + Vec3(1, 1, 1))
    place(mc.Block("tube coral"), pos + Vec3(w - 2, 1, 1))
    place(lantern_floor, pos + Vec3(w // 2, h, 1))


# ═══════════════════════  ЛОББИ  ═══════════════════════

def build_lobby(pos: Vec3):
    """Двухсветное лобби: ресепшен, лифты, галерея, зона отдыха."""
    mid_x = width // 2
    mid_z = depth // 2

    # мраморный пол — шахматный узор
    for dx in range(1, width - 1):
        for dz in range(1, depth - 1):
            b = floor_marble if (dx + dz) % 2 == 0 else floor_block
            place(b, pos + Vec3(dx, 1, dz))

    # красная дорожка к входу
    for dz in range(1, depth - 1):
        place(carpet_gold, pos + Vec3(mid_x, 1, dz))
        place(carpet_gold, pos + Vec3(mid_x - 1, 1, dz))

    # ресепшен
    for dx in range(mid_x - 3, mid_x + 4):
        place(mc.Block("polished andesite"), pos + Vec3(dx, 1, mid_z))
        place(mc.Block("dark oak pressure plate"), pos + Vec3(dx, 2, mid_z))
    for dx in range(mid_x - 2, mid_x + 3, 2):
        place(mc.Block("spruce stairs").withData({"facing": "south"}),
              pos + Vec3(dx, 1, mid_z + 1))

    # лифты
    elevator_doors(pos + Vec3(2, 1, mid_z - 1), "east")
    elevator_doors(pos + Vec3(width - 4, 1, mid_z - 1), "west")

    # зоны отдыха
    sofa(pos + Vec3(3, 1, 3), 4, "east", "spruce")
    sofa(pos + Vec3(width - 5, 1, 3), 4, "west", "spruce")
    dining_table(pos + Vec3(3, 1, depth - 5), 3, "x")
    dining_table(pos + Vec3(width - 6, 1, depth - 5), 3, "x")

    # галерея — картины (разноцветные шерсть + рамки)
    art_colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime"]
    for i, dx in enumerate(range(5, width - 5, 3)):
        color = art_colors[i % len(art_colors)]
        place(mc.Block(f"{color} wool"), pos + Vec3(dx, 2, 1))
        item_frame(pos + Vec3(dx, 2, 0), "south")

    # цветы
    flower_row(pos + Vec3(2, 1, 2), 4, "x")
    flower_row(pos + Vec3(width - 6, 1, 2), 4, "x")
    flower_row(pos + Vec3(2, 1, depth - 3), 4, "x")
    flower_row(pos + Vec3(width - 6, 1, depth - 3), 4, "x")

    # освещение
    grand_chandelier(pos + Vec3(mid_x, floor_height - 1, mid_z // 2), 2)
    grand_chandelier(pos + Vec3(mid_x, floor_height - 1, mid_z + mid_z // 2), 2)
    floor_lamp(pos + Vec3(1, 1, 1))
    floor_lamp(pos + Vec3(width - 2, 1, 1))
    floor_lamp(pos + Vec3(1, 1, depth - 2))
    floor_lamp(pos + Vec3(width - 2, 1, depth - 2))

    # атриум в центре лобби
    atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)

    # акварium у боковых стен
    aquarium(pos + Vec3(1, 2, depth - 5), 4, 3)
    aquarium(pos + Vec3(width - 5, 2, depth - 5), 4, 3)

    # стойка ресепшен — детали
    place(mc.Block("bell"), pos + Vec3(mid_x, 2, mid_z))
    place(mc.Block("flower pot"), pos + Vec3(mid_x - 3, 2, mid_z))
    place(mc.Block("flower pot"), pos + Vec3(mid_x + 3, 2, mid_z))


# ═══════════════════════  ЖИЛОЙ ЭТАЖ  ═══════════════════════

def build_living_floor(pos: Vec3, floor_num: int):
    mid_x = width // 2
    mid_z = depth // 2
    stair_x = width - 6  # граница: мебель только при dx < stair_x

    for dx in range(2, stair_x):
        for dz in range(2, depth - 2):
            if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                continue
            c = carpet_dark if (dx + dz + floor_num) % 4 == 0 else carpet_light
            place(c, pos + Vec3(dx, 1, dz))

    # ── спальня (северо-запад) ──
    bed_colors = ["red", "blue", "cyan", "lime", "pink", "purple", "orange", "magenta", "light_blue"]
    color = random.choice(bed_colors)
    bed_set(pos + Vec3(3, 1, 3), "north", color)
    place(mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, 1, 2))
    place(mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, 1, 3))
    place(mc.Block("flower pot"), pos + Vec3(5, 1, 3))
    floor_lamp(pos + Vec3(2, 1, 5))
    small_chandelier(ceiling_y(pos) + Vec3(4, 0, 4))

    # ── кухня-столовая (центр) ──
    kitchen_counter(pos + Vec3(mid_x + 1, 1, 2), 5, "north")
    dining_table(pos + Vec3(mid_x + 2, 1, mid_z - 2), 4, "x")
    for i in range(4):
        place(mc.Block("spruce stairs").withData({"facing": "north"}),
              pos + Vec3(mid_x + 2 + i, 1, mid_z - 1))
        place(mc.Block("spruce stairs").withData({"facing": "south"}),
              pos + Vec3(mid_x + 2 + i, 1, mid_z - 3))
    place(mc.Block("cauldron"), pos + Vec3(mid_x + 1, 1, 3))
    small_chandelier(ceiling_y(pos) + Vec3(mid_x + 3, 0, mid_z - 2))

    # ── гостиная (южная половина) ──
    sofa(pos + Vec3(3, 1, mid_z + 2), 4, "east", "dark_oak")
    dining_table(pos + Vec3(6, 1, mid_z + 4), 2, "x")
    fireplace(pos + Vec3(3, 1, depth - 4))
    tv_wall(pos + Vec3(mid_x + 1, 2, mid_z + 3), 3, 2)
    sofa(pos + Vec3(mid_x + 4, 1, mid_z + 4), 2, "west", "spruce")
    flower_row(pos + Vec3(11, 1, depth - 2), 4, "x")
    grand_chandelier(ceiling_y(pos) + Vec3(6, 0, mid_z + 4), 1)

    for dx in range(3, stair_x, 5):
        place(mc.Block("potted_fern"), pos + Vec3(dx, 1, 1))
        place(mc.Block("potted_bamboo"), pos + Vec3(dx, 1, depth - 2))

    atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 1)
    lighting_grid(pos, step_x=6, step_z=5)


def small_chandelier(center: Vec3):
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            place(mc.Block("chain"), center + Vec3(dx, 0, dz))
            if abs(dx) + abs(dz) <= 1:
                place(lantern_hang, center + Vec3(dx, -1, dz))


# ═══════════════════════  ОФИСНЫЙ ЭТАЖ  ═══════════════════════

def build_office_floor(pos: Vec3, floor_num: int):
    mid_x = width // 2
    mid_z = depth // 2
    stair_x = width - 6

    for dx in range(2, stair_x):
        for dz in range(2, depth - 2):
            if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                continue
            place(carpet_light if (dx + dz) % 3 == 0 else carpet_dark, pos + Vec3(dx, 1, dz))

    # open-space — рабочие столы
    for row in range(2):
        for col in range(3):
            office_desk(pos + Vec3(3 + col * 4, 1, 3 + row * 3), "north")

    # переговорная зона (без перегородок)
    meeting_table(pos + Vec3(3, 1, depth - 6), 5)
    place(mc.Block("lectern"), pos + Vec3(2, 1, depth - 5))

    # кофе-уголок
    dining_table(pos + Vec3(mid_x + 2, 1, mid_z - 2), 3, "x")
    place(mc.Block("brewing stand"), pos + Vec3(mid_x + 1, 1, mid_z - 2))
    place(mc.Block("cake"), pos + Vec3(mid_x + 1, 1, mid_z - 3))

    flower_row(pos + Vec3(2, 1, 2), 4, "x")

    atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 1)
    lighting_grid(pos, step_x=5, step_z=4)
    for dx in (3, stair_x - 2):
        floor_lamp(pos + Vec3(dx, 1, mid_z + 1))
    grand_chandelier(ceiling_y(pos) + Vec3(mid_x - 3, 0, depth - 5), 1)


# ═══════════════════════  СПОРТИВНЫЙ ЭТАЖ  ═══════════════════════

def build_gym_floor(pos: Vec3):
    mid_x = width // 2
    mid_z = depth // 2
    stair_x = width - 6

    fill(floor_block, pos + Vec3(2, 1, 2), pos + Vec3(stair_x - 1, 1, depth - 3))

    gym_equipment(pos + Vec3(3, 1, 3))
    gym_equipment(pos + Vec3(3, 1, depth - 5))
    gym_equipment(pos + Vec3(8, 1, 3))

    # беговая дорожка
    for dx in range(4, stair_x - 2, 2):
        place(carpet_dark, pos + Vec3(dx, 1, depth - 4))
        place(carpet_dark, pos + Vec3(dx, 1, depth - 3))

    # йога-зона
    for dx in range(mid_x - 1, mid_x + 3):
        for dz in range(mid_z - 1, mid_z + 3):
            if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                continue
            place(carpet_light, pos + Vec3(dx, 1, dz))
    place(mc.Block("flower pot"), pos + Vec3(mid_x + 2, 1, mid_z + 2))

    # мини-бассейн
    fill(pool_block, pos + Vec3(stair_x - 6, 0, 2), pos + Vec3(stair_x - 1, 0, 7))
    fill(water_block, pos + Vec3(stair_x - 5, 0, 3), pos + Vec3(stair_x - 2, 0, 6))
    for dx in range(stair_x - 5, stair_x - 1):
        place(lantern_floor, pos + Vec3(dx, 1, 2))

    sofa(pos + Vec3(2, 1, depth - 5), 3, "east", "spruce")
    atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)
    grand_chandelier(ceiling_y(pos) + Vec3(mid_x - 4, 0, 4), 1)
    lighting_grid(pos, step_x=6, step_z=5)


# ═══════════════════════  ПЕНТХАУС  ═══════════════════════

def build_penthouse(pos: Vec3):
    mid_x = width // 2
    mid_z = depth // 2
    stair_x = width - 6

    for dx in range(1, width - 1):
        for dz in range(1, depth - 1):
            if dx >= stair_x:
                place(floor_marble, pos + Vec3(dx, 1, dz))
            else:
                place(floor_marble if (dx + dz) % 2 == 0 else carpet_gold, pos + Vec3(dx, 1, dz))

    # master bedroom — без перегородок
    bed_set(pos + Vec3(3, 1, 3), "north", "purple")
    bed_set(pos + Vec3(6, 1, 3), "north", "purple")
    jacuzzi(pos + Vec3(3, 1, 8))
    place(mc.Block("ender chest").withData({"facing": "south"}), pos + Vec3(2, 1, 2))
    place(mc.Block("ender chest").withData({"facing": "south"}), pos + Vec3(2, 1, 3))

    # гостиная (центр-юг)
    sofa(pos + Vec3(3, 1, mid_z + 2), 4, "east", "dark_oak")
    sofa(pos + Vec3(8, 1, mid_z + 2), 4, "east", "dark_oak")
    grand_piano(pos + Vec3(mid_x - 1, 1, mid_z + 5))
    fireplace(pos + Vec3(8, 1, depth - 3))
    tv_wall(pos + Vec3(mid_x + 1, 2, mid_z + 3), 4, 2)
    dining_table(pos + Vec3(mid_x - 2, 1, mid_z), 6, "x")

    # кухня и бар (правая половина)
    kitchen_counter(pos + Vec3(stair_x - 6, 1, 2), 5, "north")
    fill(mc.Block("gold block"), pos + Vec3(2, 1, depth - 5), pos + Vec3(4, 1, depth - 4))
    place(mc.Block("brewing stand"), pos + Vec3(3, 2, depth - 5))

    flower_row(pos + Vec3(2, 1, mid_z - 1), 6, "x")
    aquarium(pos + Vec3(stair_x - 4, 2, depth - 5), 3, 3)

    # роскошное освещение
    grand_chandelier(ceiling_y(pos) + Vec3(mid_x - 2, 0, mid_z), 2)
    grand_chandelier(ceiling_y(pos) + Vec3(5, 0, 5), 1)
    atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)
    lighting_grid(pos, step_x=6, step_z=6)


# ═══════════════════════  ЛЕСТНИЦА  ═══════════════════════

def build_stairs(pos: Vec3, floor_num: int):
    sx = width - 4
    if floor_num % 2 == 0:
        dy = 1
        for dz in range(3, 3 + floor_height):
            place(mc.Block("quartz stairs").withData({"facing": "south"}),
                  pos + Vec3(sx, dy, dz))
            place(mc.Block("quartz stairs").withData({"facing": "south"}),
                  pos + Vec3(sx - 1, dy, dz))
            place(railing_wood, pos + Vec3(sx + 1, dy, dz))
            place(railing_wood, pos + Vec3(sx - 2, dy + 1, dz))
            place(end_rod, pos + Vec3(sx - 2, dy + 2, dz))
            place(lantern_floor, pos + Vec3(sx + 1, dy + 2, dz))
            dy += 1
        fill(mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, 3 + floor_height),
             pos + Vec3(sx, floor_height, 3 + floor_height + 2))
    else:
        dy = 1
        for dz in range(depth - 4, depth - 4 - floor_height, -1):
            place(mc.Block("quartz stairs").withData({"facing": "north"}),
                  pos + Vec3(sx, dy, dz))
            place(mc.Block("quartz stairs").withData({"facing": "north"}),
                  pos + Vec3(sx - 1, dy, dz))
            place(railing_wood, pos + Vec3(sx + 1, dy, dz))
            place(railing_wood, pos + Vec3(sx - 2, dy + 1, dz))
            place(end_rod, pos + Vec3(sx - 2, dy + 2, dz))
            place(lantern_floor, pos + Vec3(sx + 1, dy + 2, dz))
            dy += 1
        fill(mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, depth - 4 - floor_height - 2),
             pos + Vec3(sx, floor_height, depth - 4 - floor_height))


# ═══════════════════════  КАРКАС ЭТАЖА  ═══════════════════════

def build_floor_shell(floor_num: int):
    floor_shift = Vec3(0, floor_num * floor_height, 0)
    fp = start + floor_shift

    stair_opening = set()
    if floor_num > 0:
        sx = width - 4
        prev = floor_num - 1
        if prev % 2 == 0:
            for dx in range(sx - 1, sx + 1):
                for dz in range(3, 3 + floor_height + 3):
                    stair_opening.add((dx, dz))
        else:
            for dx in range(sx - 1, sx + 1):
                for dz in range(depth - 4 - floor_height - 2, depth - 3):
                    stair_opening.add((dx, dz))

    is_penthouse = floor_num >= floors - 2

    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                p = fp + Vec3(dx, y, dz)
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_corner = dx in (0, width - 1) and dz in (0, depth - 1)

                if y == 0 and not is_edge:
                    if (dx, dz) in stair_opening:
                        continue
                    place(floor_block, p)

                if is_edge:
                    if is_corner:
                        place(pillar_gold if is_penthouse else pillar_block, p)
                    elif y == 0 or y == floor_height - 1:
                        place(dark_accent, p)
                    elif 1 <= y <= floor_height - 2:
                        if floor_num == 0:
                            if (dx in (0, width - 1) and dz % 2 == 0) or \
                               (dz in (0, depth - 1) and dx % 2 == 0):
                                place(glass_block, p)
                            else:
                                place(wall_block, p)
                        elif is_penthouse:
                            if 2 <= dx <= width - 3 and dz in (0, depth - 1):
                                place(dark_glass, p)
                            elif 2 <= dz <= depth - 3 and dx in (0, width - 1):
                                place(dark_glass, p)
                            else:
                                place(accent_wall, p)
                        else:
                            if (dx in (0, width - 1) and 2 <= dz <= depth - 3) or \
                               (dz in (0, depth - 1) and 2 <= dx <= width - 3):
                                place(glass_block, p)
                            else:
                                place(wall_block, p)

    if floor_num == 0:
        door_x = width // 2
        for dy in range(1, 4):
            place(mc.Block("air"), fp + Vec3(door_x, dy, 0))
            place(mc.Block("air"), fp + Vec3(door_x - 1, dy, 0))
            place(mc.Block("air"), fp + Vec3(door_x + 1, dy, 0))
        place(mc.Block("stone brick stairs").withData({"facing": "east", "half": "top"}),
              fp + Vec3(door_x - 1, 3, 0))
        place(mc.Block("stone brick stairs").withData({"facing": "west", "half": "top"}),
              fp + Vec3(door_x + 1, 3, 0))
        place(pillar_gold, fp + Vec3(door_x - 2, 1, 0))
        place(pillar_gold, fp + Vec3(door_x + 2, 1, 0))

    facade_pillars(fp)


# ═══════════════════════  БАЛКОНЫ  ═══════════════════════

def build_balconies(floor_num: int):
    if floor_num < 2 or floor_num % 3 != 0:
        return
    fp = start + Vec3(0, floor_num * floor_height, 0)

    for side_z, dz_range in ((-1, range(-2, 0)), (depth, range(depth, depth + 2))):
        for dx in range(4, width - 4):
            for dz in dz_range:
                place(mc.Block("smooth quartz slab"), fp + Vec3(dx, 0, dz))
            place(railing_block, fp + Vec3(dx, 1, dz_range[-1]))
        for dz in dz_range:
            place(railing_block, fp + Vec3(3, 1, dz))
            place(railing_block, fp + Vec3(width - 4, 1, dz))
        flower_row(fp + Vec3(5, 1, side_z if side_z < 0 else depth), min(6, width - 10), "x")
        place(end_rod, fp + Vec3(4, 1, side_z if side_z < 0 else depth))
        place(end_rod, fp + Vec3(width - 5, 1, side_z if side_z < 0 else depth))


# ═══════════════════════  КРЫША  ═══════════════════════

def build_roof():
    ry = floors * floor_height
    rp = start + Vec3(0, ry, 0)
    mid_x = width // 2
    mid_z = depth // 2

    fill(roof_block, rp + Vec3(-2, 0, -2), rp + Vec3(width + 1, 0, depth + 1))

    # ступенчатая корона
    for tier, shrink in enumerate([0, 2, 4]):
        y = tier
        fill(accent_wall, rp + Vec3(shrink, y, shrink),
             rp + Vec3(width - 1 - shrink, y, depth - 1 - shrink))

    # infinity-бассейн
    px, pz = 2, 2
    fill(pool_block, rp + Vec3(px, 1, pz), rp + Vec3(px + 8, 1, pz + 5))
    fill(mc.Block("air"), rp + Vec3(px + 1, 1, pz + 1), rp + Vec3(px + 7, 1, pz + 4))
    fill(pool_block, rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 7, 0, pz + 4))
    fill(water_block, rp + Vec3(px + 1, 1, pz + 1), rp + Vec3(px + 7, 1, pz + 4))
    for i in range(4):
        place(mc.Block("spruce stairs").withData({"facing": "north", "half": "bottom"}),
              rp + Vec3(px + 1 + i * 2, 2, pz + 6))

    # сад
    for dx in range(12, width - 2):
        for dz in range(2, 7):
            place(grass_block, rp + Vec3(dx, 1, dz))
    tree(rp + Vec3(16, 2, 4), 4)
    flower_row(rp + Vec3(12, 2, 2), 6, "x")

    # бар на крыше
    kitchen_counter(rp + Vec3(2, 2, depth - 6), 5, "north")
    sofa(rp + Vec3(2, 2, depth - 4), 3, "east", "spruce")
    dining_table(rp + Vec3(2, 2, depth - 8), 3, "x")
    grand_chandelier(rp + Vec3(5, 4, depth - 5), 1)
    floor_lamp(rp + Vec3(2, 2, depth - 3))
    floor_lamp(rp + Vec3(8, 2, depth - 3))
    strip_lights(rp + Vec3(2, 4, depth - 7), 6, "x")

    # подсветка бассейна
    for dx in range(px, px + 9):
        place(lantern_floor, rp + Vec3(dx, 1, pz - 1))
        place(lantern_floor, rp + Vec3(dx, 1, pz + 6))
    for dz in range(pz, pz + 6):
        place(end_rod, rp + Vec3(px - 1, 2, dz))
        place(end_rod, rp + Vec3(px + 9, 2, dz))

    # обсерватория
    for dx in range(mid_x - 2, mid_x + 3):
        for dz in range(mid_z - 2, mid_z + 3):
            place(glass_block, rp + Vec3(dx, 2, dz))
            place(glass_block, rp + Vec3(dx, 3, dz))
    place(light_strip, rp + Vec3(mid_x, 1, mid_z))
    grand_chandelier(rp + Vec3(mid_x, 4, mid_z), 1)
    for dx in range(mid_x - 2, mid_x + 3):
        place(end_rod, rp + Vec3(dx, 1, mid_z - 3))
        place(end_rod, rp + Vec3(dx, 1, mid_z + 3))
    for dz in range(mid_z - 2, mid_z + 3):
        place(end_rod, rp + Vec3(mid_x - 3, 1, dz))
        place(end_rod, rp + Vec3(mid_x + 3, 1, dz))
    for dx in range(mid_x - 2, mid_x + 3):
        place(railing_block, rp + Vec3(dx, 2, mid_z - 3))
        place(railing_block, rp + Vec3(dx, 2, mid_z + 3))
    for dz in range(mid_z - 2, mid_z + 3):
        place(railing_block, rp + Vec3(mid_x - 3, 2, dz))
        place(railing_block, rp + Vec3(mid_x + 3, 2, dz))

    # ограждение
    for dx in range(-2, width + 2):
        place(railing_block, rp + Vec3(dx, 2, -2))
        place(railing_block, rp + Vec3(dx, 2, depth + 1))
    for dz in range(-2, depth + 2):
        place(railing_block, rp + Vec3(-2, 2, dz))
        place(railing_block, rp + Vec3(width + 1, 2, dz))

    # антенны и маяк
    for i, dx in enumerate([3, mid_x, width - 4]):
        h = 8 + i * 3
        for a in range(h):
            place(antenna_block, rp + Vec3(dx, 3 + a, mid_z))
    place(mc.Block("beacon"), rp + Vec3(mid_x, 3 + 12, mid_z))

    # вертолётная площадка
    fill(mc.Block("yellow concrete"), rp + Vec3(mid_x - 4, 2, mid_z - 4),
         rp + Vec3(mid_x + 4, 2, mid_z + 4))
    fill(roof_block, rp + Vec3(mid_x - 3, 2, mid_z - 3),
         rp + Vec3(mid_x + 3, 2, mid_z + 3))
    for dx, dz in [
        (mid_x - 2, mid_z - 1), (mid_x - 2, mid_z), (mid_x - 2, mid_z + 1),
        (mid_x - 1, mid_z), (mid_x + 1, mid_z),
        (mid_x + 2, mid_z - 1), (mid_x + 2, mid_z), (mid_x + 2, mid_z + 1),
    ]:
        place(mc.Block("white concrete"), rp + Vec3(dx, 2, dz))


# ═══════════════════════  ОКРУЖЕНИЕ  ═══════════════════════

def build_surroundings():
    ground_y = start.y
    bx = start.x
    bz = start.z

    fill(plaza_block, Vec3(bx - 5, ground_y, bz - 14), Vec3(bx + width + 4, ground_y, bz - 1))
    fill(path_block, Vec3(bx + width // 2 - 1, ground_y, bz - 14),
         Vec3(bx + width // 2 + 1, ground_y, bz - 1))

    fountain(Vec3(bx + width // 2, ground_y + 1, bz - 8), radius=3)

    tree(Vec3(bx - 2, ground_y + 1, bz - 12), 6)
    tree(Vec3(bx + width + 1, ground_y + 1, bz - 12), 6)
    tree(Vec3(bx - 2, ground_y + 1, bz - 4), 5)
    tree(Vec3(bx + width + 1, ground_y + 1, bz - 4), 5)

    for dx in range(-5, width + 5):
        place(hedge_block, Vec3(bx + dx, ground_y + 1, bz - 14))
        place(hedge_block, Vec3(bx + dx, ground_y + 2, bz - 14))
    for dz in range(-14, 0):
        place(hedge_block, Vec3(bx - 5, ground_y + 1, bz + dz))
        place(hedge_block, Vec3(bx + width + 4, ground_y + 1, bz + dz))

    for z_off in (-5, -10):
        for side_x, facing in ((2, "east"), (width - 3, "west")):
            place(mc.Block("spruce stairs").withData({"facing": facing}),
                  Vec3(bx + side_x, ground_y + 1, bz + z_off))
            place(mc.Block("spruce stairs").withData({"facing": facing}),
                  Vec3(bx + side_x, ground_y + 1, bz + z_off + 1))

    lamp_positions = [
        Vec3(bx - 3, ground_y, bz - 3),
        Vec3(bx + width + 2, ground_y, bz - 3),
        Vec3(bx - 3, ground_y, bz - 12),
        Vec3(bx + width + 2, ground_y, bz - 12),
        Vec3(bx + width // 2 - 5, ground_y, bz - 14),
        Vec3(bx + width // 2 + 5, ground_y, bz - 14),
    ]
    for lp in lamp_positions:
        for dy in range(1, 5):
            place(mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
        place(lantern_hang, lp + Vec3(0, 4, 0))
        place(end_rod, lp + Vec3(1, 3, 0))
        place(end_rod, lp + Vec3(-1, 3, 0))

    # кафе-терраса
    fill(mc.Block("spruce planks"), Vec3(bx - 4, ground_y, bz - 3),
         Vec3(bx - 1, ground_y, bz + 3))
    for dx in range(-4, 0):
        for dz in range(-3, 4, 3):
            dining_table(Vec3(bx + dx, ground_y + 1, bz + dz), 2, "x")
    tree(Vec3(bx - 3, ground_y + 1, bz), 3)

    # парковка
    fill(mc.Block("gray concrete"), Vec3(bx, ground_y, bz + depth + 1),
         Vec3(bx + width - 1, ground_y, bz + depth + 12))
    for dx in range(0, width, 4):
        fill(mc.Block("white concrete"), Vec3(bx + dx, ground_y, bz + depth + 4),
             Vec3(bx + dx, ground_y, bz + depth + 9))
    car_colors = ["red", "blue", "yellow", "lime", "cyan", "light_gray", "orange", "purple"]
    for i, dx in enumerate(range(1, min(width - 3, 20), 4)):
        parking_car(Vec3(bx + dx, ground_y + 1, bz + depth + 5), car_colors[i % len(car_colors)])


# ═══════════════════════  ГЛАВНАЯ СБОРКА  ═══════════════════════

mc.postToChat("Стройка Crystal Crown Tower...")

for f in range(floors):
    build_floor_shell(f)
    mc.postToChat(f"  каркас этажа {f + 1}/{floors}")

build_lobby(start)

for f in range(1, floors):
    fp = start + Vec3(0, f * floor_height, 0)
    if f >= floors - 2:
        build_penthouse(fp)
    elif f % 5 == 0:
        build_gym_floor(fp)
    elif f % 2 == 0:
        build_office_floor(fp, f)
    else:
        build_living_floor(fp, f)
    build_stairs(fp, f)

for f in range(floors):
    build_balconies(f)

build_roof()
build_surroundings()

mc.postToChat("Отрисовка...")
mcw.draw()
mc.postToChat("Crystal Crown Tower завершена!")
