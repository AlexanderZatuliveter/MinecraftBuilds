"""
Luxury Tower — современная башня с террасами, бассейном на крыше,
лобби, кухнями, спальнями, библиотеками, садом и фонтаном у входа.
"""

import random
from pathlib import Path
import sys

from mcpq import Block, Minecraft, Vec3

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft("192.168.1.88")
mcw = MinecraftWrap(mc)

start = Vec3(-1000, 67, -700)

# ── размеры ──
floors = 18
floor_height = 5
width = 21       # X
depth = 17       # Z

# ── палитра блоков ──
wall_block       = mc.Block("white concrete")
accent_wall      = mc.Block("light gray concrete")
glass_block      = mc.Block("light blue stained glass pane")
dark_glass       = mc.Block("gray stained glass pane")
floor_block      = mc.Block("polished andesite")
ceiling_block    = mc.Block("smooth stone")
pillar_block     = mc.Block("quartz pillar")
roof_block       = mc.Block("black concrete")
roof_slab        = mc.Block("blackstone slab")
antenna_block    = mc.Block("iron bars")
railing_block    = mc.Block("dark oak fence")
carpet_light     = mc.Block("light gray carpet")
carpet_dark      = mc.Block("gray carpet")
carpet_red       = mc.Block("red carpet")
lantern_hang     = mc.Block("lantern").withData({"hanging": True})
lantern_floor    = mc.Block("lantern")
soul_lantern     = mc.Block("soul lantern").withData({"hanging": True})
pool_block       = mc.Block("prismarine bricks")
water_block      = mc.Block("water")
leaf_block       = mc.Block("oak leaves").withData({"persistent": True})
log_block        = mc.Block("oak log")
grass_block      = mc.Block("grass block")
flower_pot_block = mc.Block("potted poppy")
path_block       = mc.Block("smooth stone")
hedge_block      = mc.Block("spruce leaves").withData({"persistent": True})
plaza_block      = mc.Block("polished diorite")
bench_block      = mc.Block("spruce stairs")


# ═══════════════════════  ВСПОМОГАТЕЛЬНЫЕ  ═══════════════════════

def fill(block, p1: Vec3, p2: Vec3):
    mcw.set_block_cube(block, p1, p2)


def place(block, pos: Vec3):
    mcw.set_block(block, pos)


# ═══════════════════════  ДЕКОР / МЕБЕЛЬ  ═══════════════════════

def chandelier(center: Vec3):
    """Люстра 3×3 из цепей и фонарей."""
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            place(mc.Block("chain"), center + Vec3(dx, 0, dz))
            if abs(dx) + abs(dz) <= 1:
                place(lantern_hang, center + Vec3(dx, -1, dz))


def wall_lamp(pos: Vec3, facing: str):
    """Настенный светильник — забор + фонарь."""
    place(mc.Block("dark oak fence"), pos)
    place(lantern_floor, pos + Vec3(0, 1, 0))


def floor_lamp(pos: Vec3):
    """Напольный светильник — столбик с фонарём."""
    place(mc.Block("dark oak fence"), pos)
    place(mc.Block("dark oak fence"), pos + Vec3(0, 1, 0))
    place(lantern_floor, pos + Vec3(0, 2, 0))


def sofa(pos: Vec3, length: int, facing: str, wood: str = "spruce"):
    """Диван из ступенек с подлокотниками."""
    dx_dir = 1 if facing in ("north", "south") else 0
    dz_dir = 0 if facing in ("north", "south") else 1
    # подлокотники
    place(mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_left"}), pos)
    end = pos + Vec3(dx_dir * (length + 1), 0, dz_dir * (length + 1))
    place(mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_right"}), end)
    for i in range(1, length + 1):
        place(mc.Block(f"{wood} stairs").withData({"facing": facing}),
              pos + Vec3(dx_dir * i, 0, dz_dir * i))


def dining_table(pos: Vec3, length: int, direction: str = "x"):
    """Обеденный стол: заборы + нажимные плиты."""
    for i in range(length):
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        place(mc.Block("dark oak fence"), pos + offset)
        place(mc.Block("dark oak pressure plate"), pos + offset + Vec3(0, 1, 0))


def kitchen_counter(pos: Vec3, length: int, facing: str):
    """Кухонный гарнитур: печки, коптильня, варочные стойки."""
    blocks = ["furnace", "smoker", "blast_furnace", "crafting_table", "smoker"]
    for i in range(length):
        b = blocks[i % len(blocks)]
        if b == "crafting_table":
            place(mc.Block("crafting table"), pos + Vec3(i, 0, 0))
        else:
            place(mc.Block(b).withData({"facing": facing}), pos + Vec3(i, 0, 0))
    # навесные шкафы — бочки
    for i in range(length):
        place(mc.Block("barrel").withData({"facing": "down"}), pos + Vec3(i, 2, 0))


def bed_set(pos: Vec3, direction: str, color: str):
    """Кровать + тумбочки."""
    mc.setBed(pos, direction, color)
    if direction == "north":
        place(mc.Block("oak trapdoor").withData({"facing": "west", "half": "bottom", "open": True}),
              pos + Vec3(1, 0, 0))
        place(mc.Block("oak trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
              pos + Vec3(-1, 0, 0))
        place(lantern_floor, pos + Vec3(1, 1, 0))
        place(lantern_floor, pos + Vec3(-1, 1, 0))
    elif direction == "south":
        place(mc.Block("oak trapdoor").withData({"facing": "west", "half": "bottom", "open": True}),
              pos + Vec3(1, 0, 0))
        place(mc.Block("oak trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
              pos + Vec3(-1, 0, 0))
        place(lantern_floor, pos + Vec3(1, 1, 0))
        place(lantern_floor, pos + Vec3(-1, 1, 0))


def bookshelf_wall(pos: Vec3, w: int, h: int):
    """Стена книжных полок w × h."""
    for dx in range(w):
        for dy in range(h):
            place(mc.Block("bookshelf"), pos + Vec3(dx, dy, 0))
    place(lantern_floor, pos + Vec3(0, h, 0))
    place(lantern_floor, pos + Vec3(w - 1, h, 0))


def flower_row(pos: Vec3, length: int, direction: str = "x"):
    """Ряд цветочных горшков."""
    flowers = ["potted_poppy", "potted_dandelion", "potted_blue_orchid",
               "potted_allium", "potted_azure_bluet", "potted_red_tulip",
               "potted_oxeye_daisy", "potted_cornflower", "potted_lily_of_the_valley"]
    for i in range(length):
        f = random.choice(flowers)
        offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
        place(mc.Block(f), pos + offset)


def tree(pos: Vec3, trunk_h: int = 5):
    """Декоративное дерево."""
    for dy in range(trunk_h):
        place(log_block, pos + Vec3(0, dy, 0))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in range(trunk_h, trunk_h + 3):
                if abs(dx) + abs(dz) <= 3 - (dy - trunk_h):
                    place(leaf_block, pos + Vec3(dx, dy, dz))


def fountain(center: Vec3):
    """Фонтан 5×5 с водой."""
    # бассейн
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 or abs(dz) == 2:
                place(pool_block, center + Vec3(dx, 0, dz))
            else:
                place(pool_block, center + Vec3(dx, -1, dz))
                place(water_block, center + Vec3(dx, 0, dz))
    # столб
    for dy in range(1, 4):
        place(mc.Block("quartz pillar"), center + Vec3(0, dy, 0))
    place(water_block, center + Vec3(0, 4, 0))


def parking_car(pos: Vec3, color: str):
    """Имитация машины из бетона и стекла."""
    # корпус
    fill(mc.Block(f"{color} concrete"), pos, pos + Vec3(1, 0, 3))
    # стёкла
    place(mc.Block("glass"), pos + Vec3(0, 1, 1))
    place(mc.Block("glass"), pos + Vec3(1, 1, 1))
    place(mc.Block("glass"), pos + Vec3(0, 1, 2))
    place(mc.Block("glass"), pos + Vec3(1, 1, 2))
    # крыша
    fill(mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 0), pos + Vec3(1, 1, 0))
    fill(mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 3), pos + Vec3(1, 1, 3))
    # колёса — кнопки
    place(mc.Block("stone button").withData({"facing": "west", "face": "floor"}), pos + Vec3(-1, 0, 0))
    place(mc.Block("stone button").withData({"facing": "west", "face": "floor"}), pos + Vec3(-1, 0, 3))
    place(mc.Block("stone button").withData({"facing": "east", "face": "floor"}), pos + Vec3(2, 0, 0))
    place(mc.Block("stone button").withData({"facing": "east", "face": "floor"}), pos + Vec3(2, 0, 3))


# ═══════════════════════  ЛОББИ (1-й этаж)  ═══════════════════════

def build_lobby(pos: Vec3):
    """Просторное лобби с ресепшеном, диванами, цветами."""
    # ресепшен — длинная стойка
    for dx in range(4, 10):
        place(mc.Block("polished andesite"), pos + Vec3(dx, 1, depth // 2))
        place(mc.Block("dark oak pressure plate"), pos + Vec3(dx, 2, depth // 2))
    # стулья за стойкой
    for dx in range(4, 10, 2):
        place(mc.Block("spruce stairs").withData({"facing": "south"}),
              pos + Vec3(dx, 1, depth // 2 + 1))

    # зона отдыха слева
    sofa(pos + Vec3(2, 1, 3), 3, "east", "dark_oak")
    dining_table(pos + Vec3(2, 1, 7), 2, "z")

    # зона отдыха справа
    sofa(pos + Vec3(width - 4, 1, 3), 3, "west", "dark_oak")
    dining_table(pos + Vec3(width - 3, 1, 7), 2, "z")

    # цветы по углам
    flower_row(pos + Vec3(2, 1, 2), 3, "x")
    flower_row(pos + Vec3(width - 5, 1, 2), 3, "x")
    flower_row(pos + Vec3(2, 1, depth - 3), 3, "x")
    flower_row(pos + Vec3(width - 5, 1, depth - 3), 3, "x")

    # ковровая дорожка ко входу
    for dz in range(1, depth - 1):
        place(carpet_red, pos + Vec3(width // 2, 1, dz))
        place(carpet_red, pos + Vec3(width // 2 - 1, 1, dz))

    # люстры
    chandelier(pos + Vec3(width // 4, floor_height - 1, depth // 3))
    chandelier(pos + Vec3(3 * width // 4, floor_height - 1, depth // 3))
    chandelier(pos + Vec3(width // 2, floor_height - 1, 2 * depth // 3))

    # напольные лампы у входа
    floor_lamp(pos + Vec3(1, 1, 1))
    floor_lamp(pos + Vec3(width - 2, 1, 1))
    floor_lamp(pos + Vec3(1, 1, depth - 2))
    floor_lamp(pos + Vec3(width - 2, 1, depth - 2))


# ═══════════════════════  ЖИЛОЙ ЭТАЖ  ═══════════════════════

def build_living_floor(pos: Vec3, floor_num: int):
    """Жилой этаж: спальня, гостиная, кухня, ванная."""

    # ── ковёр ──
    for dx in range(2, width - 2):
        for dz in range(2, depth - 2):
            c = carpet_dark if (dx + dz) % 5 == 0 else carpet_light
            place(c, pos + Vec3(dx, 1, dz))

    # ── разделительные стены (внутренние) ──
    mid_x = width // 2
    mid_z = depth // 2
    # стена по X (делит на 2 зоны по Z)
    for dx in range(2, width - 2):
        for dy in range(1, floor_height - 1):
            if dx in (mid_x - 1, mid_x, mid_x + 1):
                continue  # проход
            place(accent_wall, pos + Vec3(dx, dy, mid_z))
    # стена по Z в верхней половине (делит на 2 комнаты)
    for dz in range(2, mid_z):
        for dy in range(1, floor_height - 1):
            if dz in (mid_z // 2 - 1, mid_z // 2, mid_z // 2 + 1):
                continue
            place(accent_wall, pos + Vec3(mid_x, dy, dz))

    # ── Зона A: спальня (левая верхняя четверть) ──
    bed_colors = ["red", "blue", "cyan", "lime", "pink", "purple", "orange", "magenta"]
    color = random.choice(bed_colors)
    bed_set(pos + Vec3(4, 1, 3), "north", color)
    # шкаф (сундуки)
    for dy in range(1, 4):
        place(mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, dy, 2))
        place(mc.Block("chest").withData({"facing": "south"}), pos + Vec3(3, dy, 2))
    # зеркало (стеклянная панель)
    place(mc.Block("glass pane"), pos + Vec3(6, 2, 2))
    place(mc.Block("glass pane"), pos + Vec3(6, 3, 2))
    # прикроватные лампы
    floor_lamp(pos + Vec3(2, 1, 5))
    place(lantern_hang, pos + Vec3(4, floor_height - 1, 3))

    # ── Зона B: кухня (правая верхняя четверть) ──
    kitchen_counter(pos + Vec3(mid_x + 2, 1, 2), 5, "north")
    # обеденный стол
    dining_table(pos + Vec3(mid_x + 3, 1, mid_z - 3), 3, "x")
    # стулья
    for i in range(3):
        place(mc.Block("spruce stairs").withData({"facing": "north"}),
              pos + Vec3(mid_x + 3 + i, 1, mid_z - 2))
        place(mc.Block("spruce stairs").withData({"facing": "south"}),
              pos + Vec3(mid_x + 3 + i, 1, mid_z - 4))
    # холодильник (железный блок + дверь)
    place(mc.Block("iron block"), pos + Vec3(width - 3, 1, 2))
    place(mc.Block("iron block"), pos + Vec3(width - 3, 2, 2))
    place(mc.Block("iron_door").withData({"facing": "south", "half": "lower"}), pos + Vec3(width - 3, 1, 3))
    # раковина (котёл)
    place(mc.Block("cauldron"), pos + Vec3(mid_x + 2, 1, 3))
    # свет
    chandelier(pos + Vec3(mid_x + 5, floor_height - 1, mid_z // 2))

    # ── Зона C: гостиная (нижняя половина) ──
    sofa(pos + Vec3(3, 1, mid_z + 3), 4, "east", "dark_oak")
    sofa(pos + Vec3(3, 1, mid_z + 6), 4, "east", "dark_oak")
    # кофейный столик
    dining_table(pos + Vec3(5, 1, mid_z + 5), 2, "x")
    # камин
    place(mc.Block("campfire").withData({"lit": True}), pos + Vec3(3, 1, depth - 3))
    place(mc.Block("bricks"), pos + Vec3(2, 1, depth - 3))
    place(mc.Block("bricks"), pos + Vec3(4, 1, depth - 3))
    for dy in range(2, 4):
        place(mc.Block("bricks"), pos + Vec3(2, dy, depth - 3))
        place(mc.Block("bricks"), pos + Vec3(4, dy, depth - 3))
        place(mc.Block("bricks"), pos + Vec3(3, dy, depth - 3))
    place(mc.Block("bricks"), pos + Vec3(2, 4, depth - 3))
    place(mc.Block("bricks"), pos + Vec3(3, 4, depth - 3))
    place(mc.Block("bricks"), pos + Vec3(4, 4, depth - 3))
    # ТВ (чёрный бетон)
    fill(mc.Block("black concrete"), pos + Vec3(width - 3, 2, mid_z + 3),
         pos + Vec3(width - 3, 3, mid_z + 5))
    # диван перед ТВ
    sofa(pos + Vec3(width - 6, 1, mid_z + 3), 2, "east", "spruce")
    # цветы
    flower_row(pos + Vec3(width - 3, 1, depth - 4), 3, "z")
    # книжная полка
    bookshelf_wall(pos + Vec3(mid_x + 1, 1, depth - 2), 4, 3)
    # свет гостиной
    chandelier(pos + Vec3(width // 4, floor_height - 1, mid_z + depth // 4))
    chandelier(pos + Vec3(3 * width // 4, floor_height - 1, mid_z + depth // 4))
    floor_lamp(pos + Vec3(2, 1, mid_z + 2))
    floor_lamp(pos + Vec3(width - 2, 1, mid_z + 2))

    # ── Цветочные горшки на подоконниках ──
    for dx in range(3, width - 3, 4):
        place(mc.Block("potted_fern"), pos + Vec3(dx, 1, 1))
        place(mc.Block("potted_fern"), pos + Vec3(dx, 1, depth - 2))


# ═══════════════════════  ЛЕСТНИЦА  ═══════════════════════

def build_stairs(pos: Vec3, floor_num: int):
    """Лестница в правой части здания — зигзаг."""
    sx = width - 3
    if floor_num % 2 == 0:
        # лестница вверх по Z
        dy = 1
        for dz in range(3, 3 + floor_height):
            place(mc.Block("quartz stairs").withData({"facing": "south"}),
                  pos + Vec3(sx, dy, dz))
            place(mc.Block("quartz stairs").withData({"facing": "south"}),
                  pos + Vec3(sx - 1, dy, dz))
            place(railing_block, pos + Vec3(sx + 1, dy, dz))
            place(railing_block, pos + Vec3(sx - 2, dy + 1, dz))
            dy += 1
        # площадка
        fill(mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, 3 + floor_height),
             pos + Vec3(sx, floor_height, 3 + floor_height + 2))
    else:
        # лестница вниз по Z (обратно)
        dy = 1
        for dz in range(depth - 4, depth - 4 - floor_height, -1):
            place(mc.Block("quartz stairs").withData({"facing": "north"}),
                  pos + Vec3(sx, dy, dz))
            place(mc.Block("quartz stairs").withData({"facing": "north"}),
                  pos + Vec3(sx - 1, dy, dz))
            place(railing_block, pos + Vec3(sx + 1, dy, dz))
            place(railing_block, pos + Vec3(sx - 2, dy + 1, dz))
            dy += 1
        fill(mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, depth - 4 - floor_height - 2),
             pos + Vec3(sx, floor_height, depth - 4 - floor_height))


# ═══════════════════════  ЭТАЖ (каркас)  ═══════════════════════

def build_floor_shell(floor_num: int):
    """Стены, пол, потолок и окна одного этажа."""
    floor_shift = Vec3(0, floor_num * floor_height, 0)
    fp = start + floor_shift   # floor pos

    for y in range(floor_height):
        for dx in range(width):
            for dz in range(depth):
                p = fp + Vec3(dx, y, dz)
                is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                is_corner = dx in (0, width - 1) and dz in (0, depth - 1)

                # пол
                if y == 0 and not is_edge:
                    place(floor_block, p)

                # каркас стен
                if is_edge:
                    if is_corner:
                        place(pillar_block, p)
                    elif y == 0 or y == floor_height - 1:
                        place(accent_wall, p)
                    elif 1 <= y <= floor_height - 2:
                        # окна с чередованием
                        if floor_num == 0:
                            # лобби — двойная высота, большие окна
                            if (dx in (0, width - 1) and dz % 2 == 0) or \
                               (dz in (0, depth - 1) and dx % 2 == 0):
                                place(glass_block, p)
                            else:
                                place(wall_block, p)
                        else:
                            if (dx in (0, width - 1) and 2 <= dz <= depth - 3) or \
                               (dz in (0, depth - 1) and 2 <= dx <= width - 3):
                                place(glass_block, p)
                            else:
                                place(wall_block, p)

    # вход (пустые блоки) — первый этаж, центральная дверь по южной стене
    if floor_num == 0:
        door_x = width // 2
        for dy in range(1, 4):
            place(mc.Block("air"), fp + Vec3(door_x, dy, 0))
            place(mc.Block("air"), fp + Vec3(door_x - 1, dy, 0))
            place(mc.Block("air"), fp + Vec3(door_x + 1, dy, 0))
        # арка
        place(mc.Block("stone brick stairs").withData({"facing": "east", "half": "top"}),
              fp + Vec3(door_x - 1, 3, 0))
        place(mc.Block("stone brick stairs").withData({"facing": "west", "half": "top"}),
              fp + Vec3(door_x + 1, 3, 0))


# ═══════════════════════  БАЛКОНЫ  ═══════════════════════

def build_balconies(floor_num: int):
    """Балконы с ограждением через этаж."""
    if floor_num < 2 or floor_num % 2 != 0:
        return
    fp = start + Vec3(0, floor_num * floor_height, 0)

    # южный балкон
    for dx in range(3, width - 3):
        place(mc.Block("smooth stone slab"), fp + Vec3(dx, 0, -1))
        place(mc.Block("smooth stone slab"), fp + Vec3(dx, 0, -2))
        place(railing_block, fp + Vec3(dx, 1, -2))
    # торцы
    for dz in (-1, -2):
        place(railing_block, fp + Vec3(2, 1, dz))
        place(railing_block, fp + Vec3(width - 3, 1, dz))
    # цветы на балконе
    flower_row(fp + Vec3(4, 1, -1), min(5, width - 8), "x")

    # северный балкон
    for dx in range(3, width - 3):
        place(mc.Block("smooth stone slab"), fp + Vec3(dx, 0, depth))
        place(mc.Block("smooth stone slab"), fp + Vec3(dx, 0, depth + 1))
        place(railing_block, fp + Vec3(dx, 1, depth + 1))
    for dz in (depth, depth + 1):
        place(railing_block, fp + Vec3(2, 1, dz))
        place(railing_block, fp + Vec3(width - 3, 1, dz))


# ═══════════════════════  КРЫША  ═══════════════════════

def build_roof():
    """Крыша с бассейном, садом, лежаками и антеннами."""
    ry = floors * floor_height
    rp = start + Vec3(0, ry, 0)

    # основание крыши
    fill(roof_block, rp + Vec3(-1, 0, -1), rp + Vec3(width, 0, depth))

    # ── бассейн 7×5 ──
    px, pz = 2, 2
    fill(pool_block, rp + Vec3(px, 0, pz), rp + Vec3(px + 6, 0, pz + 4))
    fill(mc.Block("air"), rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 5, 0, pz + 3))
    fill(pool_block, rp + Vec3(px + 1, -1, pz + 1), rp + Vec3(px + 5, -1, pz + 3))
    fill(water_block, rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 5, 0, pz + 3))

    # лежаки у бассейна
    for i in range(3):
        place(mc.Block("spruce stairs").withData({"facing": "north", "half": "bottom"}),
              rp + Vec3(px + 1 + i * 2, 1, pz + 5))

    # ── сад на крыше ──
    for dx in range(12, width - 2):
        for dz in range(2, 6):
            place(grass_block, rp + Vec3(dx, 0, dz))
    tree(rp + Vec3(15, 1, 4), 4)
    flower_row(rp + Vec3(12, 1, 2), 5, "x")
    flower_row(rp + Vec3(12, 1, 5), 5, "x")

    # ── зона отдыха ──
    sofa(rp + Vec3(3, 1, depth - 4), 3, "east", "spruce")
    dining_table(rp + Vec3(3, 1, depth - 6), 3, "x")
    floor_lamp(rp + Vec3(2, 1, depth - 3))
    floor_lamp(rp + Vec3(7, 1, depth - 3))

    # ── ограждение крыши ──
    for dx in range(-1, width + 1):
        place(railing_block, rp + Vec3(dx, 1, -1))
        place(railing_block, rp + Vec3(dx, 1, depth))
    for dz in range(-1, depth + 1):
        place(railing_block, rp + Vec3(-1, 1, dz))
        place(railing_block, rp + Vec3(width, 1, dz))

    # ── антенны ──
    for i, dx in enumerate([4, width // 2, width - 5]):
        h = 7 + i * 2
        for a in range(h):
            place(antenna_block, rp + Vec3(dx, 2 + a, depth // 2))
    # красный маячок
    place(mc.Block("redstone lamp"), rp + Vec3(width // 2, 2 + 9, depth // 2))

    # ── вертолётная площадка ──
    fill(mc.Block("yellow concrete"), rp + Vec3(width // 2 - 3, 1, depth // 2 - 3),
         rp + Vec3(width // 2 + 3, 1, depth // 2 + 3))
    fill(roof_block, rp + Vec3(width // 2 - 2, 1, depth // 2 - 2),
         rp + Vec3(width // 2 + 2, 1, depth // 2 + 2))
    # H
    place(mc.Block("white concrete"), rp + Vec3(width // 2 - 1, 1, depth // 2 - 1))
    place(mc.Block("white concrete"), rp + Vec3(width // 2 - 1, 1, depth // 2))
    place(mc.Block("white concrete"), rp + Vec3(width // 2 - 1, 1, depth // 2 + 1))
    place(mc.Block("white concrete"), rp + Vec3(width // 2, 1, depth // 2))
    place(mc.Block("white concrete"), rp + Vec3(width // 2 + 1, 1, depth // 2 - 1))
    place(mc.Block("white concrete"), rp + Vec3(width // 2 + 1, 1, depth // 2))
    place(mc.Block("white concrete"), rp + Vec3(width // 2 + 1, 1, depth // 2 + 1))


# ═══════════════════════  ОКРУЖЕНИЕ  ═══════════════════════

def build_surroundings():
    """Площадь перед зданием: дорожки, фонтан, деревья, скамейки, парковка, фонари."""
    ground_y = start.y
    bx = start.x  # base x
    bz = start.z  # base z

    # ── площадь перед входом ──
    fill(plaza_block, Vec3(bx - 3, ground_y, bz - 12), Vec3(bx + width + 2, ground_y, bz - 1))

    # дорожка от входа
    fill(path_block, Vec3(bx + width // 2 - 1, ground_y, bz - 12),
         Vec3(bx + width // 2 + 1, ground_y, bz - 1))

    # ── фонтан ──
    fountain(Vec3(bx + width // 2, ground_y + 1, bz - 7))

    # ── деревья по бокам ──
    tree(Vec3(bx - 1, ground_y + 1, bz - 10), 5)
    tree(Vec3(bx + width, ground_y + 1, bz - 10), 5)
    tree(Vec3(bx - 1, ground_y + 1, bz - 4), 4)
    tree(Vec3(bx + width, ground_y + 1, bz - 4), 4)

    # ── живая изгородь ──
    for dx in range(-3, width + 3):
        place(hedge_block, Vec3(bx + dx, ground_y + 1, bz - 12))
        place(hedge_block, Vec3(bx + dx, ground_y + 2, bz - 12))
    for dz in range(-12, 0):
        place(hedge_block, Vec3(bx - 3, ground_y + 1, bz + dz))
        place(hedge_block, Vec3(bx + width + 2, ground_y + 1, bz + dz))

    # ── скамейки ──
    for z_off in (-4, -9):
        place(mc.Block("spruce stairs").withData({"facing": "east"}),
              Vec3(bx + 2, ground_y + 1, bz + z_off))
        place(mc.Block("spruce stairs").withData({"facing": "east"}),
              Vec3(bx + 2, ground_y + 1, bz + z_off + 1))
        place(mc.Block("spruce stairs").withData({"facing": "west"}),
              Vec3(bx + width - 3, ground_y + 1, bz + z_off))
        place(mc.Block("spruce stairs").withData({"facing": "west"}),
              Vec3(bx + width - 3, ground_y + 1, bz + z_off + 1))

    # ── уличные фонари ──
    lamp_positions = [
        Vec3(bx - 2, ground_y, bz - 2),
        Vec3(bx + width + 1, ground_y, bz - 2),
        Vec3(bx - 2, ground_y, bz - 11),
        Vec3(bx + width + 1, ground_y, bz - 11),
        Vec3(bx + width // 2 - 4, ground_y, bz - 12),
        Vec3(bx + width // 2 + 4, ground_y, bz - 12),
    ]
    for lp in lamp_positions:
        for dy in range(1, 5):
            place(mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
        place(lantern_hang, lp + Vec3(0, 4, 0))
        place(mc.Block("dark oak fence"), lp + Vec3(1, 4, 0))
        place(lantern_hang, lp + Vec3(1, 3, 0))
        place(mc.Block("dark oak fence"), lp + Vec3(-1, 4, 0))
        place(lantern_hang, lp + Vec3(-1, 3, 0))

    # ── парковка (за зданием) ──
    fill(mc.Block("gray concrete"), Vec3(bx, ground_y, bz + depth + 1),
         Vec3(bx + width - 1, ground_y, bz + depth + 10))
    # разметка
    for dx in range(0, width, 4):
        fill(mc.Block("white concrete"), Vec3(bx + dx, ground_y, bz + depth + 3),
             Vec3(bx + dx, ground_y, bz + depth + 8))
    # машины
    car_colors = ["red", "blue", "yellow", "lime", "cyan", "light_gray"]
    for i, dx in enumerate(range(1, min(width - 3, 18), 4)):
        color = car_colors[i % len(car_colors)]
        parking_car(Vec3(bx + dx, ground_y + 1, bz + depth + 4), color)

    # фонари на парковке
    for dx in range(0, width, 8):
        lp = Vec3(bx + dx, ground_y, bz + depth + 2)
        for dy in range(1, 4):
            place(mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
        place(lantern_floor, lp + Vec3(0, 4, 0))


# ═══════════════════════  ГЛАВНАЯ СБОРКА  ═══════════════════════

mc.postToChat("Стройка Luxury Tower...")

# 1. Каркас этажей
for f in range(floors):
    build_floor_shell(f)
    mc.postToChat(f"  каркас этажа {f + 1}/{floors}")

# 2. Лобби
build_lobby(start)

# 3. Жилые этажи с мебелью
for f in range(1, floors):
    fp = start + Vec3(0, f * floor_height, 0)
    build_living_floor(fp, f)
    build_stairs(fp, f)

# 4. Балконы
for f in range(floors):
    build_balconies(f)

# 5. Крыша
build_roof()

# 6. Окружение
build_surroundings()

mc.postToChat("Отрисовка...")
mcw.draw()
mc.postToChat("Luxury Tower завершена!")
