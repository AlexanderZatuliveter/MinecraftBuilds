"""
Luxury Tower — современная башня с террасами, бассейном на крыше,
лобби, кухнями, спальнями, библиотеками, садом и фонтаном у входа.
"""

import random

from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams


class LuxuryTower:
    def __init__(self, mc: Minecraft):
        self.mc = mc
        self.mcw = MinecraftWrap(mc)

        self.wall_block = mc.Block("white concrete")
        self.accent_wall = mc.Block("light gray concrete")
        self.glass_block = mc.Block("light blue stained glass pane")
        self.dark_glass = mc.Block("gray stained glass pane")
        self.floor_block = mc.Block("polished andesite")
        self.ceiling_block = mc.Block("smooth stone")
        self.pillar_block = mc.Block("quartz pillar")
        self.roof_block = mc.Block("black concrete")
        self.roof_slab = mc.Block("blackstone slab")
        self.antenna_block = mc.Block("iron bars")
        self.railing_block = mc.Block("dark oak fence")
        self.carpet_light = mc.Block("light gray carpet")
        self.carpet_dark = mc.Block("gray carpet")
        self.carpet_red = mc.Block("red carpet")
        self.lantern_hang = mc.Block("lantern").withData({"hanging": True})
        self.lantern_floor = mc.Block("lantern")
        self.soul_lantern = mc.Block("soul lantern").withData({"hanging": True})
        self.pool_block = mc.Block("prismarine bricks")
        self.water_block = mc.Block("water")
        self.leaf_block = mc.Block("oak leaves").withData({"persistent": True})
        self.log_block = mc.Block("oak log")
        self.grass_block = mc.Block("grass block")
        self.flower_pot_block = mc.Block("potted poppy")
        self.path_block = mc.Block("smooth stone")
        self.hedge_block = mc.Block("spruce leaves").withData({"persistent": True})
        self.plaza_block = mc.Block("polished diorite")
        self.bench_block = mc.Block("spruce stairs")

    def build(self, build_params: BuildParams):
        self.mc.postToChat("Стройка Luxury Tower...")
        p = build_params

        for f in range(p.floors):
            self._build_floor_shell(f, p)
            self.mc.postToChat(f"  каркас этажа {f + 1}/{p.floors}")

        self._build_lobby(p.start, p)

        for f in range(1, p.floors):
            fp = p.start + Vec3(0, f * p.floor_height, 0)
            self._build_living_floor(fp, f, p)
            if f < p.floors - 1:
                self._build_stairs(fp, f, p)

        for f in range(p.floors):
            self._build_balconies(f, p)

        self._build_roof(p)
        self._build_surroundings(p)

        self.mc.postToChat("Отрисовка...")
        self.mcw.draw()
        self.mc.postToChat("Luxury Tower завершена!")

    # ═══════════════════════  ВСПОМОГАТЕЛЬНЫЕ  ═══════════════════════

    def _fill(self, block, p1: Vec3, p2: Vec3):
        self.mcw.set_block_cube(block, p1, p2)

    def _place(self, block, pos: Vec3):
        self.mcw.set_block(block, pos)

    # ═══════════════════════  ДЕКОР / МЕБЕЛЬ  ═══════════════════════

    def _chandelier(self, center: Vec3):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                self._place(self.mc.Block("chain"), center + Vec3(dx, 0, dz))
                if abs(dx) + abs(dz) <= 1:
                    self._place(self.lantern_hang, center + Vec3(dx, -1, dz))

    def _wall_lamp(self, pos: Vec3, facing: str):
        self._place(self.mc.Block("dark oak fence"), pos)
        self._place(self.lantern_floor, pos + Vec3(0, 1, 0))

    def _floor_lamp(self, pos: Vec3):
        self._place(self.mc.Block("dark oak fence"), pos)
        self._place(self.mc.Block("dark oak fence"), pos + Vec3(0, 1, 0))
        self._place(self.lantern_floor, pos + Vec3(0, 2, 0))

    def _sofa(self, pos: Vec3, length: int, facing: str, wood: str = "spruce"):
        dx_dir = 1 if facing in ("north", "south") else 0
        dz_dir = 0 if facing in ("north", "south") else 1
        self._place(self.mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_left"}), pos)
        end = pos + Vec3(dx_dir * (length + 1), 0, dz_dir * (length + 1))
        self._place(self.mc.Block(f"{wood} stairs").withData({"facing": facing, "shape": "outer_right"}), end)
        for i in range(1, length + 1):
            self._place(self.mc.Block(f"{wood} stairs").withData({"facing": facing}),
                        pos + Vec3(dx_dir * i, 0, dz_dir * i))

    def _dining_table(self, pos: Vec3, length: int, direction: str = "x"):
        for i in range(length):
            offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
            self._place(self.mc.Block("dark oak fence"), pos + offset)
            self._place(self.mc.Block("dark oak pressure plate"), pos + offset + Vec3(0, 1, 0))

    def _kitchen_counter(self, pos: Vec3, length: int, facing: str):
        blocks = ["furnace", "smoker", "blast_furnace", "crafting_table", "smoker"]
        for i in range(length):
            b = blocks[i % len(blocks)]
            if b == "crafting_table":
                self._place(self.mc.Block("crafting table"), pos + Vec3(i, 0, 0))
            else:
                self._place(self.mc.Block(b).withData({"facing": facing}), pos + Vec3(i, 0, 0))
        for i in range(length):
            self._place(self.mc.Block("barrel").withData({"facing": "down"}), pos + Vec3(i, 2, 0))

    def _bed_set(self, pos: Vec3, direction: str, color: str):
        self.mc.setBed(pos, direction, color)
        if direction == "north":
            self._place(self.mc.Block("oak trapdoor").withData({"facing": "west", "half": "bottom", "open": True}),
                        pos + Vec3(1, 0, 0))
            self._place(self.mc.Block("oak trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
                        pos + Vec3(-1, 0, 0))
            self._place(self.lantern_floor, pos + Vec3(1, 1, 0))
            self._place(self.lantern_floor, pos + Vec3(-1, 1, 0))
        elif direction == "south":
            self._place(self.mc.Block("oak trapdoor").withData({"facing": "west", "half": "bottom", "open": True}),
                        pos + Vec3(1, 0, 0))
            self._place(self.mc.Block("oak trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
                        pos + Vec3(-1, 0, 0))
            self._place(self.lantern_floor, pos + Vec3(1, 1, 0))
            self._place(self.lantern_floor, pos + Vec3(-1, 1, 0))

    def _bookshelf_wall(self, pos: Vec3, w: int, h: int):
        for dx in range(w):
            for dy in range(h):
                self._place(self.mc.Block("bookshelf"), pos + Vec3(dx, dy, 0))
        self._place(self.lantern_floor, pos + Vec3(0, h, 0))
        self._place(self.lantern_floor, pos + Vec3(w - 1, h, 0))

    def _flower_row(self, pos: Vec3, length: int, direction: str = "x"):
        flowers = ["potted_poppy", "potted_dandelion", "potted_blue_orchid",
                   "potted_allium", "potted_azure_bluet", "potted_red_tulip",
                   "potted_oxeye_daisy", "potted_cornflower", "potted_lily_of_the_valley"]
        for i in range(length):
            f = random.choice(flowers)
            offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
            self._place(self.mc.Block(f), pos + offset)

    def _tree(self, pos: Vec3, trunk_h: int = 5):
        for dy in range(trunk_h):
            self._place(self.log_block, pos + Vec3(0, dy, 0))
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in range(trunk_h, trunk_h + 3):
                    if abs(dx) + abs(dz) <= 3 - (dy - trunk_h):
                        self._place(self.leaf_block, pos + Vec3(dx, dy, dz))

    def _fountain(self, center: Vec3):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) == 2 or abs(dz) == 2:
                    self._place(self.pool_block, center + Vec3(dx, 0, dz))
                else:
                    self._place(self.pool_block, center + Vec3(dx, -1, dz))
                    self._place(self.water_block, center + Vec3(dx, 0, dz))
        for dy in range(1, 4):
            self._place(self.mc.Block("quartz pillar"), center + Vec3(0, dy, 0))
        self._place(self.water_block, center + Vec3(0, 4, 0))

    def _parking_car(self, pos: Vec3, color: str):
        self._fill(self.mc.Block(f"{color} concrete"), pos, pos + Vec3(1, 0, 3))
        self._place(self.mc.Block("glass"), pos + Vec3(0, 1, 1))
        self._place(self.mc.Block("glass"), pos + Vec3(1, 1, 1))
        self._place(self.mc.Block("glass"), pos + Vec3(0, 1, 2))
        self._place(self.mc.Block("glass"), pos + Vec3(1, 1, 2))
        self._fill(self.mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 0), pos + Vec3(1, 1, 0))
        self._fill(self.mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 3), pos + Vec3(1, 1, 3))
        self._place(self.mc.Block("stone button").withData({"facing": "west", "face": "floor"}), pos + Vec3(-1, 0, 0))
        self._place(self.mc.Block("stone button").withData({"facing": "west", "face": "floor"}), pos + Vec3(-1, 0, 3))
        self._place(self.mc.Block("stone button").withData({"facing": "east", "face": "floor"}), pos + Vec3(2, 0, 0))
        self._place(self.mc.Block("stone button").withData({"facing": "east", "face": "floor"}), pos + Vec3(2, 0, 3))

    # ═══════════════════════  ЛОББИ  ═══════════════════════

    def _build_lobby(self, pos: Vec3, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height

        for dx in range(4, 10):
            self._place(self.mc.Block("polished andesite"), pos + Vec3(dx, 1, depth // 2))
            self._place(self.mc.Block("dark oak pressure plate"), pos + Vec3(dx, 2, depth // 2))
        for dx in range(4, 10, 2):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "south"}),
                        pos + Vec3(dx, 1, depth // 2 + 1))

        self._sofa(pos + Vec3(2, 1, 3), 3, "east", "dark_oak")
        self._dining_table(pos + Vec3(2, 1, 7), 2, "z")
        self._sofa(pos + Vec3(12, 1, 3), 3, "west", "dark_oak")
        self._dining_table(pos + Vec3(12, 1, 7), 2, "z")

        self._flower_row(pos + Vec3(2, 1, 2), 3, "x")
        self._flower_row(pos + Vec3(11, 1, 2), 3, "x")
        self._flower_row(pos + Vec3(2, 1, depth - 3), 3, "x")
        self._flower_row(pos + Vec3(11, 1, depth - 3), 3, "x")

        for dz in range(1, depth - 1):
            self._place(self.carpet_red, pos + Vec3(width // 2, 1, dz))
            self._place(self.carpet_red, pos + Vec3(width // 2 - 1, 1, dz))

        self._chandelier(pos + Vec3(width // 4, floor_height - 1, depth // 3))
        self._chandelier(pos + Vec3(3 * width // 4, floor_height - 1, depth // 3))
        self._chandelier(pos + Vec3(width // 2, floor_height - 1, 2 * depth // 3))

        self._floor_lamp(pos + Vec3(1, 1, 1))
        self._floor_lamp(pos + Vec3(14, 1, 1))
        self._floor_lamp(pos + Vec3(1, 1, depth - 2))
        self._floor_lamp(pos + Vec3(14, 1, depth - 2))

    # ═══════════════════════  ЖИЛОЙ ЭТАЖ  ═══════════════════════

    def _build_living_floor(self, pos: Vec3, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        stair_x_min = width - 6

        for dx in range(2, stair_x_min):
            for dz in range(2, depth - 2):
                c = self.carpet_dark if (dx + dz) % 5 == 0 else self.carpet_light
                self._place(c, pos + Vec3(dx, 1, dz))

        mid_x = width // 2
        mid_z = depth // 2

        bed_colors = ["red", "blue", "cyan", "lime", "pink", "purple", "orange", "magenta"]
        color = random.choice(bed_colors)
        self._bed_set(pos + Vec3(4, 1, 3), "north", color)
        for dy in range(1, 4):
            self._place(self.mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, dy, 2))
            self._place(self.mc.Block("chest").withData({"facing": "south"}), pos + Vec3(3, dy, 2))
        self._place(self.mc.Block("glass pane"), pos + Vec3(6, 2, 2))
        self._place(self.mc.Block("glass pane"), pos + Vec3(6, 3, 2))
        self._floor_lamp(pos + Vec3(2, 1, 5))
        self._place(self.lantern_hang, pos + Vec3(4, floor_height - 1, 3))

        self._kitchen_counter(pos + Vec3(mid_x + 1, 1, 2), 3, "north")
        self._place(self.mc.Block("iron block"), pos + Vec3(stair_x_min - 1, 1, 2))
        self._place(self.mc.Block("iron block"), pos + Vec3(stair_x_min - 1, 2, 2))
        self._place(self.mc.Block("iron_door").withData({"facing": "south", "half": "lower"}),
                    pos + Vec3(stair_x_min - 1, 1, 3))
        self._place(self.mc.Block("cauldron"), pos + Vec3(mid_x + 1, 1, 3))
        self._dining_table(pos + Vec3(mid_x + 1, 1, mid_z - 3), 3, "x")
        for i in range(3):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "north"}),
                        pos + Vec3(mid_x + 1 + i, 1, mid_z - 2))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "south"}),
                        pos + Vec3(mid_x + 1 + i, 1, mid_z - 4))
        self._chandelier(pos + Vec3(mid_x + 2, floor_height - 1, mid_z // 2))

        self._sofa(pos + Vec3(3, 1, mid_z + 3), 4, "east", "dark_oak")
        self._sofa(pos + Vec3(3, 1, mid_z + 6), 4, "east", "dark_oak")
        self._dining_table(pos + Vec3(5, 1, mid_z + 5), 2, "x")
        self._place(self.mc.Block("campfire").withData({"lit": True}), pos + Vec3(3, 1, depth - 3))
        self._place(self.mc.Block("bricks"), pos + Vec3(2, 1, depth - 3))
        self._place(self.mc.Block("bricks"), pos + Vec3(4, 1, depth - 3))
        for dy in range(2, 4):
            self._place(self.mc.Block("bricks"), pos + Vec3(2, dy, depth - 3))
            self._place(self.mc.Block("bricks"), pos + Vec3(4, dy, depth - 3))
            self._place(self.mc.Block("bricks"), pos + Vec3(3, dy, depth - 3))
        self._place(self.mc.Block("bricks"), pos + Vec3(2, 4, depth - 3))
        self._place(self.mc.Block("bricks"), pos + Vec3(3, 4, depth - 3))
        self._place(self.mc.Block("bricks"), pos + Vec3(4, 4, depth - 3))
        self._fill(self.mc.Block("black concrete"), pos + Vec3(mid_x + 1, 2, mid_z + 3),
                   pos + Vec3(mid_x + 1, 3, mid_z + 5))
        self._sofa(pos + Vec3(mid_x + 3, 1, mid_z + 3), 2, "west", "spruce")
        self._flower_row(pos + Vec3(2, 1, depth - 4), 3, "z")
        self._bookshelf_wall(pos + Vec3(mid_x + 1, 1, depth - 2), 3, 3)
        self._chandelier(pos + Vec3(width // 4, floor_height - 1, mid_z + depth // 4))
        self._chandelier(pos + Vec3(mid_x + 2, floor_height - 1, mid_z + depth // 4))
        self._floor_lamp(pos + Vec3(2, 1, mid_z + 2))
        self._floor_lamp(pos + Vec3(stair_x_min - 1, 1, mid_z + 2))

        for dx in range(3, stair_x_min, 4):
            self._place(self.mc.Block("potted_fern"), pos + Vec3(dx, 1, 1))
            self._place(self.mc.Block("potted_fern"), pos + Vec3(dx, 1, depth - 2))

    # ═══════════════════════  ЛЕСТНИЦА  ═══════════════════════

    def _build_stairs(self, pos: Vec3, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        sx = width - 3
        if floor_num % 2 == 0:
            dy = 1
            for dz in range(3, 3 + floor_height):
                self._place(self.mc.Block("quartz stairs").withData({"facing": "south"}),
                            pos + Vec3(sx, dy, dz))
                self._place(self.mc.Block("quartz stairs").withData({"facing": "south"}),
                            pos + Vec3(sx - 1, dy, dz))
                self._place(self.railing_block, pos + Vec3(sx + 1, dy, dz))
                self._place(self.railing_block, pos + Vec3(sx - 2, dy + 1, dz))
                dy += 1
            self._fill(self.mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, 3 + floor_height),
                       pos + Vec3(sx, floor_height, 3 + floor_height + 2))
        else:
            dy = 1
            for dz in range(depth - 4, depth - 4 - floor_height, -1):
                self._place(self.mc.Block("quartz stairs").withData({"facing": "north"}),
                            pos + Vec3(sx, dy, dz))
                self._place(self.mc.Block("quartz stairs").withData({"facing": "north"}),
                            pos + Vec3(sx - 1, dy, dz))
                self._place(self.railing_block, pos + Vec3(sx + 1, dy, dz))
                self._place(self.railing_block, pos + Vec3(sx - 2, dy + 1, dz))
                dy += 1
            self._fill(self.mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, depth - 4 - floor_height - 2),
                       pos + Vec3(sx, floor_height, depth - 4 - floor_height))

    # ═══════════════════════  ЭТАЖ (каркас)  ═══════════════════════

    def _build_floor_shell(self, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        start = params.start

        floor_shift = Vec3(0, floor_num * floor_height, 0)
        fp = start + floor_shift

        stair_opening = set()
        if floor_num > 0:
            sx = width - 3
            prev = floor_num - 1
            if prev % 2 == 0:
                for dx in range(sx - 1, sx + 1):
                    for dz in range(3, 3 + floor_height + 3):
                        stair_opening.add((dx, dz))
            else:
                for dx in range(sx - 1, sx + 1):
                    for dz in range(depth - 4 - floor_height - 2, depth - 3):
                        stair_opening.add((dx, dz))

        for y in range(floor_height):
            for dx in range(width):
                for dz in range(depth):
                    p = fp + Vec3(dx, y, dz)
                    is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                    is_corner = dx in (0, width - 1) and dz in (0, depth - 1)

                    if y == 0 and not is_edge:
                        if (dx, dz) in stair_opening:
                            continue
                        self._place(self.floor_block, p)

                    if is_edge:
                        if is_corner:
                            self._place(self.pillar_block, p)
                        elif y == 0 or y == floor_height - 1:
                            self._place(self.accent_wall, p)
                        elif 1 <= y <= floor_height - 2:
                            if floor_num == 0:
                                if (dx in (0, width - 1) and dz % 2 == 0) or \
                                   (dz in (0, depth - 1) and dx % 2 == 0):
                                    self._place(self.glass_block, p)
                                else:
                                    self._place(self.wall_block, p)
                            else:
                                if (dx in (0, width - 1) and 2 <= dz <= depth - 3) or \
                                   (dz in (0, depth - 1) and 2 <= dx <= width - 3):
                                    self._place(self.glass_block, p)
                                else:
                                    self._place(self.wall_block, p)

        if floor_num == 0:
            door_x = width // 2
            for dy in range(1, 4):
                self._place(self.mc.Block("air"), fp + Vec3(door_x, dy, 0))
                self._place(self.mc.Block("air"), fp + Vec3(door_x - 1, dy, 0))
                self._place(self.mc.Block("air"), fp + Vec3(door_x + 1, dy, 0))
            self._place(self.mc.Block("stone brick stairs").withData({"facing": "east", "half": "top"}),
                        fp + Vec3(door_x - 1, 3, 0))
            self._place(self.mc.Block("stone brick stairs").withData({"facing": "west", "half": "top"}),
                        fp + Vec3(door_x + 1, 3, 0))

    # ═══════════════════════  БАЛКОНЫ  ═══════════════════════

    def _build_balconies(self, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        start = params.start

        if floor_num < 2 or floor_num % 2 != 0:
            return
        fp = start + Vec3(0, floor_num * floor_height, 0)

        for dx in range(3, width - 3):
            self._place(self.mc.Block("smooth stone slab"), fp + Vec3(dx, 0, -1))
            self._place(self.mc.Block("smooth stone slab"), fp + Vec3(dx, 0, -2))
            self._place(self.railing_block, fp + Vec3(dx, 1, -2))
        for dz in (-1, -2):
            self._place(self.railing_block, fp + Vec3(2, 1, dz))
            self._place(self.railing_block, fp + Vec3(width - 3, 1, dz))
        self._flower_row(fp + Vec3(4, 1, -1), min(5, width - 8), "x")

        for dx in range(3, width - 3):
            self._place(self.mc.Block("smooth stone slab"), fp + Vec3(dx, 0, depth))
            self._place(self.mc.Block("smooth stone slab"), fp + Vec3(dx, 0, depth + 1))
            self._place(self.railing_block, fp + Vec3(dx, 1, depth + 1))
        for dz in (depth, depth + 1):
            self._place(self.railing_block, fp + Vec3(2, 1, dz))
            self._place(self.railing_block, fp + Vec3(width - 3, 1, dz))

    # ═══════════════════════  КРЫША  ═══════════════════════

    def _build_roof(self, params: BuildParams):
        width = params.width
        depth = params.depth
        floors = params.floors
        floor_height = params.floor_height
        start = params.start

        ry = floors * floor_height
        rp = start + Vec3(0, ry, 0)

        self._fill(self.roof_block, rp + Vec3(-1, 0, -1), rp + Vec3(width, 0, depth))

        px, pz = 2, 2
        self._fill(self.pool_block, rp + Vec3(px, 0, pz), rp + Vec3(px + 6, 0, pz + 4))
        self._fill(self.mc.Block("air"), rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 5, 0, pz + 3))
        self._fill(self.pool_block, rp + Vec3(px + 1, -1, pz + 1), rp + Vec3(px + 5, -1, pz + 3))
        self._fill(self.water_block, rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 5, 0, pz + 3))

        for i in range(3):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "north", "half": "bottom"}),
                        rp + Vec3(px + 1 + i * 2, 1, pz + 5))

        for dx in range(12, width - 2):
            for dz in range(2, 5):
                self._place(self.grass_block, rp + Vec3(dx, 0, dz))
        self._tree(rp + Vec3(15, 1, 3), 4)
        self._flower_row(rp + Vec3(12, 1, 2), 5, "x")
        self._flower_row(rp + Vec3(12, 1, 4), 5, "x")

        self._sofa(rp + Vec3(3, 1, depth - 5), 3, "east", "spruce")
        self._dining_table(rp + Vec3(3, 1, depth - 7), 3, "x")
        self._floor_lamp(rp + Vec3(2, 1, depth - 4))
        self._floor_lamp(rp + Vec3(7, 1, depth - 4))

        for dx in range(-1, width + 1):
            self._place(self.railing_block, rp + Vec3(dx, 1, -1))
            self._place(self.railing_block, rp + Vec3(dx, 1, depth))
        for dz in range(-1, depth + 1):
            self._place(self.railing_block, rp + Vec3(-1, 1, dz))
            self._place(self.railing_block, rp + Vec3(width, 1, dz))

        for i, dx in enumerate([0, width - 1]):
            h = 7 + i * 2
            for a in range(h):
                self._place(self.antenna_block, rp + Vec3(dx, 1 + a, depth // 2))

        self._place(self.mc.Block("redstone torch"), rp + Vec3(width - 1, 1 + 9, depth // 2))

        heli_x, heli_z = 14, 12
        self._fill(self.mc.Block("yellow concrete"), rp + Vec3(heli_x - 3, 1, heli_z - 3),
                   rp + Vec3(heli_x + 3, 1, heli_z + 3))
        self._fill(self.roof_block, rp + Vec3(heli_x - 2, 1, heli_z - 2),
                   rp + Vec3(heli_x + 2, 1, heli_z + 2))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x - 1, 1, heli_z - 1))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x - 1, 1, heli_z))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x - 1, 1, heli_z + 1))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x, 1, heli_z))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x + 1, 1, heli_z - 1))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x + 1, 1, heli_z))
        self._place(self.mc.Block("white concrete"), rp + Vec3(heli_x + 1, 1, heli_z + 1))

    # ═══════════════════════  ОКРУЖЕНИЕ  ═══════════════════════

    def _build_surroundings(self, params: BuildParams):
        width = params.width
        depth = params.depth
        start = params.start

        ground_y = start.y
        bx = start.x
        bz = start.z

        self._fill(self.plaza_block, Vec3(bx - 3, ground_y, bz - 12), Vec3(bx + width + 2, ground_y, bz - 1))
        self._fill(self.path_block, Vec3(bx + width // 2 - 1, ground_y, bz - 12),
                   Vec3(bx + width // 2 + 1, ground_y, bz - 1))

        self._fountain(Vec3(bx + width // 2, ground_y + 1, bz - 7))

        self._tree(Vec3(bx - 1, ground_y + 1, bz - 10), 5)
        self._tree(Vec3(bx + width, ground_y + 1, bz - 10), 5)
        self._tree(Vec3(bx - 1, ground_y + 1, bz - 4), 4)
        self._tree(Vec3(bx + width, ground_y + 1, bz - 4), 4)

        for dx in range(-3, width + 3):
            self._place(self.hedge_block, Vec3(bx + dx, ground_y + 1, bz - 12))
            self._place(self.hedge_block, Vec3(bx + dx, ground_y + 2, bz - 12))
        for dz in range(-12, 0):
            self._place(self.hedge_block, Vec3(bx - 3, ground_y + 1, bz + dz))
            self._place(self.hedge_block, Vec3(bx + width + 2, ground_y + 1, bz + dz))

        for z_off in (-4, -9):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "east"}),
                        Vec3(bx + 2, ground_y + 1, bz + z_off))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "east"}),
                        Vec3(bx + 2, ground_y + 1, bz + z_off + 1))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "west"}),
                        Vec3(bx + width - 3, ground_y + 1, bz + z_off))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "west"}),
                        Vec3(bx + width - 3, ground_y + 1, bz + z_off + 1))

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
                self._place(self.mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
            self._place(self.lantern_hang, lp + Vec3(0, 4, 0))
            self._place(self.mc.Block("dark oak fence"), lp + Vec3(1, 4, 0))
            self._place(self.lantern_hang, lp + Vec3(1, 3, 0))
            self._place(self.mc.Block("dark oak fence"), lp + Vec3(-1, 4, 0))
            self._place(self.lantern_hang, lp + Vec3(-1, 3, 0))

        self._fill(self.mc.Block("gray concrete"), Vec3(bx, ground_y, bz + depth + 1),
                   Vec3(bx + width - 1, ground_y, bz + depth + 10))
        for dx in range(0, width, 4):
            self._fill(self.mc.Block("white concrete"), Vec3(bx + dx, ground_y, bz + depth + 3),
                       Vec3(bx + dx, ground_y, bz + depth + 8))
        car_colors = ["red", "blue", "yellow", "lime", "cyan", "light_gray"]
        for i, dx in enumerate(range(1, min(width - 3, 18), 4)):
            color = car_colors[i % len(car_colors)]
            self._parking_car(Vec3(bx + dx, ground_y + 1, bz + depth + 4), color)

        for dx in range(0, width, 8):
            lp = Vec3(bx + dx, ground_y, bz + depth + 2)
            for dy in range(1, 4):
                self._place(self.mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
            self._place(self.lantern_floor, lp + Vec3(0, 4, 0))
