"""
Crystal Crown Tower — архитектурный небоскрёб с атриумом, офисами,
пентхаусом, бассейном на крыше, обсерваторией и детализированным лобби.
Объединяет интерьеры Luxury Tower и атриум my_skyscraper.
"""

import random

from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams


class CrystalCrownTower:
    def __init__(self, mc: Minecraft):
        self.mc = mc
        self.mcw = MinecraftWrap(mc)

        self.wall_block = mc.Block("smooth quartz")
        self.accent_wall = mc.Block("cyan terracotta")
        self.dark_accent = mc.Block("deepslate tiles")
        self.glass_block = mc.Block("light blue stained glass pane")
        self.dark_glass = mc.Block("gray stained glass pane")
        self.floor_block = mc.Block("polished deepslate")
        self.floor_marble = mc.Block("quartz block")
        self.ceiling_block = mc.Block("smooth stone")
        self.pillar_block = mc.Block("cut copper")
        self.pillar_gold = mc.Block("gold block")
        self.roof_block = mc.Block("black concrete")
        self.roof_slab = mc.Block("blackstone slab")
        self.antenna_block = mc.Block("lightning rod")
        self.railing_block = mc.Block("iron bars")
        self.railing_wood = mc.Block("dark oak fence")
        self.carpet_light = mc.Block("light blue carpet")
        self.carpet_dark = mc.Block("cyan carpet")
        self.carpet_gold = mc.Block("yellow carpet")
        self.lantern_hang = mc.Block("sea lantern")
        self.lantern_floor = mc.Block("sea lantern")
        self.soul_lantern = mc.Block("soul lantern").withData({"hanging": True})
        self.atrium_block = mc.Block("sea lantern")
        self.pool_block = mc.Block("prismarine bricks")
        self.water_block = mc.Block("water")
        self.leaf_block = mc.Block("azalea leaves").withData({"persistent": True})
        self.log_block = mc.Block("dark oak log")
        self.grass_block = mc.Block("grass block")
        self.plaza_block = mc.Block("polished diorite")
        self.path_block = mc.Block("smooth stone")
        self.hedge_block = mc.Block("spruce leaves").withData({"persistent": True})
        self.light_strip = mc.Block("glowstone")
        self.end_rod = mc.Block("end rod")

    def build(self, build_params: BuildParams):
        self.mc.postToChat("Стройка Crystal Crown Tower...")
        p = build_params

        for f in range(p.floors):
            self._build_floor_shell(f, p)
            self.mc.postToChat(f"  каркас этажа {f + 1}/{p.floors}")

        self._build_lobby(p.start, p)

        for f in range(1, p.floors):
            fp = p.start + Vec3(0, f * p.floor_height, 0)
            if f >= p.floors - 2:
                self._build_penthouse(fp, p)
            elif f % 5 == 0:
                self._build_gym_floor(fp, p)
            elif f % 2 == 0:
                self._build_office_floor(fp, f, p)
            else:
                self._build_living_floor(fp, f, p)
            self._build_stairs(fp, f, p)

        for f in range(p.floors):
            self._build_balconies(f, p)

        self._build_roof(p)
        self._build_surroundings(p)

        self.mc.postToChat("Отрисовка...")
        self.mcw.draw()
        self.mc.postToChat("Crystal Crown Tower завершена!")

    # ═══════════════════════  ВСПОМОГАТЕЛЬНЫЕ  ═══════════════════════

    def _fill(self, block, p1: Vec3, p2: Vec3):
        self.mcw.set_block_cube(block, p1, p2)

    def _place(self, block, pos: Vec3):
        self.mcw.set_block(block, pos)

    def _item_frame(self, pos: Vec3, facing: str = "south"):
        facings = {
            "north": Vec3().north(),
            "south": Vec3().south(),
            "east": Vec3().east(),
            "west": Vec3().west(),
        }
        frame = self.mc.spawnEntity("item_frame", pos)
        frame.teleport(facing=facings[facing])

    def _ceiling_y(self, pos: Vec3) -> Vec3:
        return pos + Vec3(0, self._current_floor_height - 1, 0)

    # ═══════════════════════  ДЕКОР / МЕБЕЛЬ  ═══════════════════════

    def _grand_chandelier(self, center: Vec3, size: int = 2):
        for dx in range(-size, size + 1):
            for dz in range(-size, size + 1):
                self._place(self.mc.Block("chain"), center + Vec3(dx, 0, dz))
                if abs(dx) + abs(dz) <= size:
                    self._place(self.lantern_hang, center + Vec3(dx, -1, dz))
                    if abs(dx) + abs(dz) <= size - 1:
                        self._place(self.lantern_hang, center + Vec3(dx, -2, dz))

    def _small_chandelier(self, center: Vec3):
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                self._place(self.mc.Block("chain"), center + Vec3(dx, 0, dz))
                if abs(dx) + abs(dz) <= 1:
                    self._place(self.lantern_hang, center + Vec3(dx, -1, dz))

    def _wall_lamp(self, pos: Vec3):
        self._place(self.mc.Block("dark oak fence"), pos)
        self._place(self.lantern_floor, pos + Vec3(0, 1, 0))

    def _floor_lamp(self, pos: Vec3):
        self._place(self.mc.Block("dark oak fence"), pos)
        self._place(self.mc.Block("dark oak fence"), pos + Vec3(0, 1, 0))
        self._place(self.lantern_floor, pos + Vec3(0, 2, 0))

    def _sofa(self, pos: Vec3, length: int, facing: str, wood: str = "dark_oak"):
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
        blocks = ["furnace", "smoker", "blast_furnace", "crafting_table", "smoker", "brewing_stand"]
        for i in range(length):
            b = blocks[i % len(blocks)]
            if b == "crafting_table":
                self._place(self.mc.Block("crafting table"), pos + Vec3(i, 0, 0))
            elif b == "brewing_stand":
                self._place(self.mc.Block("brewing stand"), pos + Vec3(i, 0, 0))
            else:
                self._place(self.mc.Block(b).withData({"facing": facing}), pos + Vec3(i, 0, 0))
        for i in range(length):
            self._place(self.mc.Block("barrel").withData({"facing": "down"}), pos + Vec3(i, 2, 0))

    def _bed_set(self, pos: Vec3, direction: str, color: str):
        self.mc.setBed(pos, direction, color)
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
                   "potted_oxeye_daisy", "potted_cornflower", "potted_lily_of_the_valley",
                   "potted_fern", "potted_bamboo"]
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

    def _fountain(self, center: Vec3, radius: int = 2):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if abs(dx) == radius or abs(dz) == radius:
                    self._place(self.pool_block, center + Vec3(dx, 0, dz))
                else:
                    self._place(self.pool_block, center + Vec3(dx, -1, dz))
                    self._place(self.water_block, center + Vec3(dx, 0, dz))
        for dy in range(1, 5):
            self._place(self.mc.Block("quartz pillar"), center + Vec3(0, dy, 0))
        self._place(self.water_block, center + Vec3(0, 5, 0))
        for dx, dz in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            self._place(self.lantern_floor, center + Vec3(dx, 1, dz))

    def _parking_car(self, pos: Vec3, color: str):
        self._fill(self.mc.Block(f"{color} concrete"), pos, pos + Vec3(1, 0, 3))
        for dz in (1, 2):
            self._place(self.mc.Block("glass"), pos + Vec3(0, 1, dz))
            self._place(self.mc.Block("glass"), pos + Vec3(1, 1, dz))
        self._fill(self.mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 0), pos + Vec3(1, 1, 0))
        self._fill(self.mc.Block(f"{color} concrete"), pos + Vec3(0, 1, 3), pos + Vec3(1, 1, 3))
        for wx, wz in [(-1, 0), (-1, 3), (2, 0), (2, 3)]:
            self._place(self.mc.Block("stone button").withData({"facing": "west" if wx < 0 else "east", "face": "floor"}),
                        pos + Vec3(wx, 0, wz))

    def _elevator_doors(self, pos: Vec3, facing: str = "south"):
        for dy in range(1, 4):
            self._place(self.mc.Block("iron_door").withData({"facing": facing, "half": "lower" if dy == 1 else "upper"}),
                        pos + Vec3(0, dy, 0))
            self._place(self.mc.Block("iron_door").withData({"facing": facing, "half": "lower" if dy == 1 else "upper"}),
                        pos + Vec3(1, dy, 0))
        self._place(self.mc.Block("stone button").withData({"facing": facing}), pos + Vec3(-1, 2, 0))

    def _office_desk(self, pos: Vec3, facing: str):
        self._place(self.mc.Block("spruce stairs").withData({"facing": facing}), pos)
        self._place(self.mc.Block("dark oak pressure plate"), pos + Vec3(0, 1, 0))
        self._place(self.mc.Block("flower pot"), pos + Vec3(1, 1, 0))

    def _gym_equipment(self, pos: Vec3):
        self._place(self.mc.Block("anvil"), pos)
        self._place(self.mc.Block("grindstone"), pos + Vec3(2, 0, 0))
        self._place(self.mc.Block("iron block"), pos + Vec3(4, 0, 0))
        self._place(self.mc.Block("iron block"), pos + Vec3(4, 1, 0))
        self._place(self.mc.Block("iron trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
                    pos + Vec3(4, 2, 0))

    def _atrium_lighting(self, center: Vec3, radius: int = 2):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                if abs(dx) + abs(dz) <= radius + 1:
                    self._place(self.atrium_block, center + Vec3(dx, 0, dz))

    def _facade_pillars(self, fp: Vec3, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        corners = [(0, 0), (width - 1, 0), (0, depth - 1), (width - 1, depth - 1)]
        for cx, cz in corners:
            for dy in range(1, floor_height):
                self._place(self.pillar_block, fp + Vec3(cx, dy, cz))
        for dx in (3, width // 2, width - 4):
            for dy in range(1, floor_height - 1):
                self._place(self.accent_wall, fp + Vec3(dx, dy, 0))
                self._place(self.accent_wall, fp + Vec3(dx, dy, depth - 1))

    def _wall_sconce(self, pos: Vec3):
        self._place(self.accent_wall, pos)
        self._place(self.end_rod, pos + Vec3(0, 1, 0))

    def _strip_lights(self, pos: Vec3, length: int, direction: str = "x"):
        for i in range(length):
            offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
            self._place(self.light_strip, pos + offset)

    def _recessed_ceiling(self, pos: Vec3):
        self._place(self.lantern_floor, pos)
        self._place(self.mc.Block("chain"), pos + Vec3(0, 1, 0))

    def _lighting_grid(self, pos: Vec3, params: BuildParams, step_x: int = 5, step_z: int = 4,
                       skip_atrium: bool = True, skip_stairs: bool = True):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        mid_x = width // 2
        mid_z = depth // 2
        stair_x = width - 5
        for dx in range(3, width - 3, step_x):
            for dz in range(3, depth - 3, step_z):
                if skip_atrium and abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                    continue
                if skip_stairs and dx >= stair_x - 1:
                    continue
                self._recessed_ceiling(self._ceiling_y(pos) + Vec3(dx, 0, dz))

    def _corridor_lights(self, pos: Vec3, path: list[tuple[int, int]]):
        for dx, dz in path:
            self._recessed_ceiling(self._ceiling_y(pos) + Vec3(dx, 0, dz))
            self._wall_sconce(pos + Vec3(dx, 2, dz))

    def _room_divider(self, pos: Vec3, length: int, params: BuildParams, direction: str = "x", door_at: int | None = None):
        floor_height = params.floor_height
        for i in range(length):
            if door_at is not None and i in (door_at, door_at + 1):
                continue
            offset = Vec3(i, 0, 0) if direction == "x" else Vec3(0, 0, i)
            for dy in range(1, floor_height - 1):
                self._place(self.accent_wall, pos + offset + Vec3(0, dy, 0))

    def _bathroom(self, pos: Vec3):
        self._fill(self.dark_accent, pos, pos + Vec3(3, 0, 3))
        self._place(self.mc.Block("cauldron"), pos + Vec3(1, 1, 1))
        self._place(self.mc.Block("cauldron"), pos + Vec3(2, 1, 1))
        self._fill(self.mc.Block("glass pane"), pos + Vec3(0, 2, 1), pos + Vec3(0, 3, 2))
        self._place(self.mc.Block("iron trapdoor").withData({"facing": "east", "half": "bottom", "open": True}),
                    pos + Vec3(3, 1, 2))
        self._place(self.lantern_floor, pos + Vec3(2, 3, 2))
        self._place(self.carpet_light, pos + Vec3(1, 1, 3))
        self._place(self.carpet_light, pos + Vec3(2, 1, 3))

    def _fireplace(self, pos: Vec3):
        for dx in (-1, 0, 1):
            for dy in range(1, 5):
                self._place(self.mc.Block("bricks"), pos + Vec3(dx, dy, 0))
        self._place(self.mc.Block("campfire").withData({"lit": True}), pos + Vec3(0, 1, 0))
        self._place(self.soul_lantern, pos + Vec3(0, 4, 0))

    def _tv_wall(self, pos: Vec3, w: int = 3, h: int = 2):
        self._fill(self.mc.Block("black concrete"), pos, pos + Vec3(w - 1, h - 1, 0))
        self._place(self.end_rod, pos + Vec3(w // 2, h, 0))
        self._place(self.mc.Block("oak trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
                    pos + Vec3(0, -1, 0))
        self._place(self.mc.Block("oak trapdoor").withData({"facing": "north", "half": "bottom", "open": True}),
                    pos + Vec3(w - 1, -1, 0))

    def _grand_piano(self, pos: Vec3):
        self._fill(self.mc.Block("black wool"), pos, pos + Vec3(2, 0, 1))
        self._fill(self.mc.Block("white wool"), pos + Vec3(0, 1, 0), pos + Vec3(2, 1, 0))
        self._place(self.mc.Block("note block"), pos + Vec3(1, 1, 1))
        self._place(self.lantern_floor, pos + Vec3(1, 2, 0))

    def _jacuzzi(self, pos: Vec3):
        self._fill(self.pool_block, pos, pos + Vec3(3, 0, 3))
        self._fill(self.water_block, pos + Vec3(1, 1, 1), pos + Vec3(2, 1, 2))
        for dx, dz in ((0, 0), (3, 0), (0, 3), (3, 3)):
            self._place(self.lantern_floor, pos + Vec3(dx, 1, dz))
        self._place(self.end_rod, pos + Vec3(1, 3, 1))

    def _meeting_table(self, pos: Vec3, length: int):
        self._fill(self.floor_marble, pos, pos + Vec3(length - 1, 0, 2))
        for i in range(length):
            self._place(self.mc.Block("dark oak fence"), pos + Vec3(i, 1, -1))
            self._place(self.mc.Block("dark oak fence"), pos + Vec3(i, 1, 3))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "north"}), pos + Vec3(i, 1, 0))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "south"}), pos + Vec3(i, 1, 2))
        self._grand_chandelier(self._ceiling_y(pos) + Vec3(length // 2, 0, 1), 1)

    def _cubicle(self, pos: Vec3, w: int, d: int):
        for dx in range(w):
            self._place(self.railing_wood, pos + Vec3(dx, 1, 0))
            self._place(self.railing_wood, pos + Vec3(dx, 1, d - 1))
        for dz in range(1, d - 1):
            self._place(self.railing_wood, pos + Vec3(0, 1, dz))
        self._office_desk(pos + Vec3(1, 1, 1), "south")
        self._recessed_ceiling(self._ceiling_y(pos) + Vec3(w // 2, 0, d // 2))

    def _aquarium(self, pos: Vec3, w: int, h: int):
        for dx in range(w):
            for dy in range(h):
                self._place(self.glass_block, pos + Vec3(dx, dy, 0))
                self._place(self.glass_block, pos + Vec3(dx, dy, 2))
        for dy in range(1, h):
            self._place(self.glass_block, pos + Vec3(0, dy, 1))
            self._place(self.glass_block, pos + Vec3(w - 1, dy, 1))
        self._fill(self.water_block, pos + Vec3(1, 1, 1), pos + Vec3(w - 2, h - 2, 1))
        self._place(self.mc.Block("brain coral"), pos + Vec3(1, 1, 1))
        self._place(self.mc.Block("tube coral"), pos + Vec3(w - 2, 1, 1))
        self._place(self.lantern_floor, pos + Vec3(w // 2, h, 1))

    # ═══════════════════════  ЛОББИ  ═══════════════════════

    def _build_lobby(self, pos: Vec3, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        self._current_floor_height = floor_height
        mid_x = width // 2
        mid_z = depth // 2

        for dx in range(1, width - 1):
            for dz in range(1, depth - 1):
                b = self.floor_marble if (dx + dz) % 2 == 0 else self.floor_block
                self._place(b, pos + Vec3(dx, 1, dz))

        for dz in range(1, depth - 1):
            self._place(self.carpet_gold, pos + Vec3(mid_x, 1, dz))
            self._place(self.carpet_gold, pos + Vec3(mid_x - 1, 1, dz))

        for dx in range(mid_x - 3, mid_x + 4):
            self._place(self.mc.Block("polished andesite"), pos + Vec3(dx, 1, mid_z))
            self._place(self.mc.Block("dark oak pressure plate"), pos + Vec3(dx, 2, mid_z))
        for dx in range(mid_x - 2, mid_x + 3, 2):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "south"}),
                        pos + Vec3(dx, 1, mid_z + 1))

        self._elevator_doors(pos + Vec3(2, 1, mid_z - 1), "east")
        self._elevator_doors(pos + Vec3(width - 4, 1, mid_z - 1), "west")

        self._sofa(pos + Vec3(3, 1, 3), 4, "east", "spruce")
        self._sofa(pos + Vec3(width - 5, 1, 3), 4, "west", "spruce")
        self._dining_table(pos + Vec3(3, 1, depth - 5), 3, "x")
        self._dining_table(pos + Vec3(width - 6, 1, depth - 5), 3, "x")

        art_colors = ["white", "orange", "magenta", "light_blue", "yellow", "lime"]
        for i, dx in enumerate(range(5, width - 5, 3)):
            color = art_colors[i % len(art_colors)]
            self._place(self.mc.Block(f"{color} wool"), pos + Vec3(dx, 2, 1))
            self._item_frame(pos + Vec3(dx, 2, 0), "south")

        self._flower_row(pos + Vec3(2, 1, 2), 4, "x")
        self._flower_row(pos + Vec3(width - 6, 1, 2), 4, "x")
        self._flower_row(pos + Vec3(2, 1, depth - 3), 4, "x")
        self._flower_row(pos + Vec3(width - 6, 1, depth - 3), 4, "x")

        self._grand_chandelier(pos + Vec3(mid_x, floor_height - 1, mid_z // 2), 2)
        self._grand_chandelier(pos + Vec3(mid_x, floor_height - 1, mid_z + mid_z // 2), 2)
        self._floor_lamp(pos + Vec3(1, 1, 1))
        self._floor_lamp(pos + Vec3(width - 2, 1, 1))
        self._floor_lamp(pos + Vec3(1, 1, depth - 2))
        self._floor_lamp(pos + Vec3(width - 2, 1, depth - 2))

        self._atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)

        self._aquarium(pos + Vec3(1, 2, depth - 5), 4, 3)
        self._aquarium(pos + Vec3(width - 5, 2, depth - 5), 4, 3)

        self._place(self.mc.Block("bell"), pos + Vec3(mid_x, 2, mid_z))
        self._place(self.mc.Block("flower pot"), pos + Vec3(mid_x - 3, 2, mid_z))
        self._place(self.mc.Block("flower pot"), pos + Vec3(mid_x + 3, 2, mid_z))

    # ═══════════════════════  ЖИЛОЙ ЭТАЖ  ═══════════════════════

    def _build_living_floor(self, pos: Vec3, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        self._current_floor_height = floor_height
        mid_x = width // 2
        mid_z = depth // 2
        stair_x = width - 6

        for dx in range(2, stair_x):
            for dz in range(2, depth - 2):
                if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                    continue
                c = self.carpet_dark if (dx + dz + floor_num) % 4 == 0 else self.carpet_light
                self._place(c, pos + Vec3(dx, 1, dz))

        bed_colors = ["red", "blue", "cyan", "lime", "pink", "purple", "orange", "magenta", "light_blue"]
        color = random.choice(bed_colors)
        self._bed_set(pos + Vec3(3, 1, 3), "north", color)
        self._place(self.mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, 1, 2))
        self._place(self.mc.Block("chest").withData({"facing": "south"}), pos + Vec3(2, 1, 3))
        self._place(self.mc.Block("flower pot"), pos + Vec3(5, 1, 3))
        self._floor_lamp(pos + Vec3(2, 1, 5))
        self._small_chandelier(self._ceiling_y(pos) + Vec3(4, 0, 4))

        self._kitchen_counter(pos + Vec3(mid_x + 1, 1, 2), 5, "north")
        self._dining_table(pos + Vec3(mid_x + 2, 1, mid_z - 2), 4, "x")
        for i in range(4):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "north"}),
                        pos + Vec3(mid_x + 2 + i, 1, mid_z - 1))
            self._place(self.mc.Block("spruce stairs").withData({"facing": "south"}),
                        pos + Vec3(mid_x + 2 + i, 1, mid_z - 3))
        self._place(self.mc.Block("cauldron"), pos + Vec3(mid_x + 1, 1, 3))
        self._small_chandelier(self._ceiling_y(pos) + Vec3(mid_x + 3, 0, mid_z - 2))

        self._sofa(pos + Vec3(3, 1, mid_z + 2), 4, "east", "dark_oak")
        self._dining_table(pos + Vec3(6, 1, mid_z + 4), 2, "x")
        self._fireplace(pos + Vec3(3, 1, depth - 4))
        self._tv_wall(pos + Vec3(mid_x + 1, 2, mid_z + 3), 3, 2)
        self._sofa(pos + Vec3(mid_x + 4, 1, mid_z + 4), 2, "west", "spruce")
        self._flower_row(pos + Vec3(11, 1, depth - 2), 4, "x")
        self._grand_chandelier(self._ceiling_y(pos) + Vec3(6, 0, mid_z + 4), 1)

        for dx in range(3, stair_x, 5):
            self._place(self.mc.Block("potted_fern"), pos + Vec3(dx, 1, 1))
            self._place(self.mc.Block("potted_bamboo"), pos + Vec3(dx, 1, depth - 2))

        self._atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 1)
        self._lighting_grid(pos, params, step_x=6, step_z=5)

    # ═══════════════════════  ОФИСНЫЙ ЭТАЖ  ═══════════════════════

    def _build_office_floor(self, pos: Vec3, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        self._current_floor_height = floor_height
        mid_x = width // 2
        mid_z = depth // 2
        stair_x = width - 6

        for dx in range(2, stair_x):
            for dz in range(2, depth - 2):
                if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                    continue
                self._place(self.carpet_light if (dx + dz) % 3 == 0 else self.carpet_dark, pos + Vec3(dx, 1, dz))

        for row in range(2):
            for col in range(3):
                self._office_desk(pos + Vec3(3 + col * 4, 1, 3 + row * 3), "north")

        self._meeting_table(pos + Vec3(3, 1, depth - 6), 5)
        self._place(self.mc.Block("lectern"), pos + Vec3(2, 1, depth - 5))

        self._dining_table(pos + Vec3(mid_x + 2, 1, mid_z - 2), 3, "x")
        self._place(self.mc.Block("brewing stand"), pos + Vec3(mid_x + 1, 1, mid_z - 2))
        self._place(self.mc.Block("cake"), pos + Vec3(mid_x + 1, 1, mid_z - 3))

        self._flower_row(pos + Vec3(2, 1, 2), 4, "x")

        self._atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 1)
        self._lighting_grid(pos, params, step_x=5, step_z=4)
        for dx in (3, stair_x - 2):
            self._floor_lamp(pos + Vec3(dx, 1, mid_z + 1))
        self._grand_chandelier(self._ceiling_y(pos) + Vec3(mid_x - 3, 0, depth - 5), 1)

    # ═══════════════════════  СПОРТИВНЫЙ ЭТАЖ  ═══════════════════════

    def _build_gym_floor(self, pos: Vec3, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        self._current_floor_height = floor_height
        mid_x = width // 2
        mid_z = depth // 2
        stair_x = width - 6

        self._fill(self.floor_block, pos + Vec3(2, 1, 2), pos + Vec3(stair_x - 1, 1, depth - 3))

        self._gym_equipment(pos + Vec3(3, 1, 3))
        self._gym_equipment(pos + Vec3(3, 1, depth - 5))
        self._gym_equipment(pos + Vec3(8, 1, 3))

        for dx in range(4, stair_x - 2, 2):
            self._place(self.carpet_dark, pos + Vec3(dx, 1, depth - 4))
            self._place(self.carpet_dark, pos + Vec3(dx, 1, depth - 3))

        for dx in range(mid_x - 1, mid_x + 3):
            for dz in range(mid_z - 1, mid_z + 3):
                if abs(dx - mid_x) <= 2 and abs(dz - mid_z) <= 2:
                    continue
                self._place(self.carpet_light, pos + Vec3(dx, 1, dz))
        self._place(self.mc.Block("flower pot"), pos + Vec3(mid_x + 2, 1, mid_z + 2))

        self._fill(self.pool_block, pos + Vec3(stair_x - 6, 0, 2), pos + Vec3(stair_x - 1, 0, 7))
        self._fill(self.water_block, pos + Vec3(stair_x - 5, 0, 3), pos + Vec3(stair_x - 2, 0, 6))
        for dx in range(stair_x - 5, stair_x - 1):
            self._place(self.lantern_floor, pos + Vec3(dx, 1, 2))

        self._sofa(pos + Vec3(2, 1, depth - 5), 3, "east", "spruce")
        self._atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)
        self._grand_chandelier(self._ceiling_y(pos) + Vec3(mid_x - 4, 0, 4), 1)
        self._lighting_grid(pos, params, step_x=6, step_z=5)

    # ═══════════════════════  ПЕНТХАУС  ═══════════════════════

    def _build_penthouse(self, pos: Vec3, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        self._current_floor_height = floor_height
        mid_x = width // 2
        mid_z = depth // 2
        stair_x = width - 6

        for dx in range(1, width - 1):
            for dz in range(1, depth - 1):
                if dx >= stair_x:
                    self._place(self.floor_marble, pos + Vec3(dx, 1, dz))
                else:
                    self._place(self.floor_marble if (dx + dz) % 2 == 0 else self.carpet_gold, pos + Vec3(dx, 1, dz))

        self._bed_set(pos + Vec3(3, 1, 3), "north", "purple")
        self._bed_set(pos + Vec3(6, 1, 3), "north", "purple")
        self._jacuzzi(pos + Vec3(3, 1, 8))
        self._place(self.mc.Block("ender chest").withData({"facing": "south"}), pos + Vec3(2, 1, 2))
        self._place(self.mc.Block("ender chest").withData({"facing": "south"}), pos + Vec3(2, 1, 3))

        self._sofa(pos + Vec3(3, 1, mid_z + 2), 4, "east", "dark_oak")
        self._sofa(pos + Vec3(8, 1, mid_z + 2), 4, "east", "dark_oak")
        self._grand_piano(pos + Vec3(mid_x - 1, 1, mid_z + 5))
        self._fireplace(pos + Vec3(8, 1, depth - 3))
        self._tv_wall(pos + Vec3(mid_x + 1, 2, mid_z + 3), 4, 2)
        self._dining_table(pos + Vec3(mid_x - 2, 1, mid_z), 6, "x")

        self._kitchen_counter(pos + Vec3(stair_x - 6, 1, 2), 5, "north")
        self._fill(self.mc.Block("gold block"), pos + Vec3(2, 1, depth - 5), pos + Vec3(4, 1, depth - 4))
        self._place(self.mc.Block("brewing stand"), pos + Vec3(3, 2, depth - 5))

        self._flower_row(pos + Vec3(2, 1, mid_z - 1), 6, "x")
        self._aquarium(pos + Vec3(stair_x - 4, 2, depth - 5), 3, 3)

        self._grand_chandelier(self._ceiling_y(pos) + Vec3(mid_x - 2, 0, mid_z), 2)
        self._grand_chandelier(self._ceiling_y(pos) + Vec3(5, 0, 5), 1)
        self._atrium_lighting(pos + Vec3(mid_x, 1, mid_z), 2)
        self._lighting_grid(pos, params, step_x=6, step_z=6)

    # ═══════════════════════  ЛЕСТНИЦА  ═══════════════════════

    def _build_stairs(self, pos: Vec3, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        sx = width - 4
        if floor_num % 2 == 0:
            dy = 1
            for dz in range(3, 3 + floor_height):
                self._place(self.mc.Block("quartz stairs").withData({"facing": "south"}),
                            pos + Vec3(sx, dy, dz))
                self._place(self.mc.Block("quartz stairs").withData({"facing": "south"}),
                            pos + Vec3(sx - 1, dy, dz))
                self._place(self.railing_wood, pos + Vec3(sx + 1, dy, dz))
                self._place(self.railing_wood, pos + Vec3(sx - 2, dy + 1, dz))
                self._place(self.end_rod, pos + Vec3(sx - 2, dy + 2, dz))
                self._place(self.lantern_floor, pos + Vec3(sx + 1, dy + 2, dz))
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
                self._place(self.railing_wood, pos + Vec3(sx + 1, dy, dz))
                self._place(self.railing_wood, pos + Vec3(sx - 2, dy + 1, dz))
                self._place(self.end_rod, pos + Vec3(sx - 2, dy + 2, dz))
                self._place(self.lantern_floor, pos + Vec3(sx + 1, dy + 2, dz))
                dy += 1
            self._fill(self.mc.Block("quartz block"), pos + Vec3(sx - 1, floor_height, depth - 4 - floor_height - 2),
                       pos + Vec3(sx, floor_height, depth - 4 - floor_height))

    # ═══════════════════════  КАРКАС ЭТАЖА  ═══════════════════════

    def _build_floor_shell(self, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        floors = params.floors
        start = params.start
        self._current_floor_height = floor_height

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
                        self._place(self.floor_block, p)

                    if is_edge:
                        if is_corner:
                            self._place(self.pillar_gold if is_penthouse else self.pillar_block, p)
                        elif y == 0 or y == floor_height - 1:
                            self._place(self.dark_accent, p)
                        elif 1 <= y <= floor_height - 2:
                            if floor_num == 0:
                                if (dx in (0, width - 1) and dz % 2 == 0) or \
                                   (dz in (0, depth - 1) and dx % 2 == 0):
                                    self._place(self.glass_block, p)
                                else:
                                    self._place(self.wall_block, p)
                            elif is_penthouse:
                                if 2 <= dx <= width - 3 and dz in (0, depth - 1):
                                    self._place(self.dark_glass, p)
                                elif 2 <= dz <= depth - 3 and dx in (0, width - 1):
                                    self._place(self.dark_glass, p)
                                else:
                                    self._place(self.accent_wall, p)
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
            self._place(self.pillar_gold, fp + Vec3(door_x - 2, 1, 0))
            self._place(self.pillar_gold, fp + Vec3(door_x + 2, 1, 0))

        self._facade_pillars(fp, params)

    # ═══════════════════════  БАЛКОНЫ  ═══════════════════════

    def _build_balconies(self, floor_num: int, params: BuildParams):
        width = params.width
        depth = params.depth
        floor_height = params.floor_height
        start = params.start

        if floor_num < 2 or floor_num % 3 != 0:
            return
        fp = start + Vec3(0, floor_num * floor_height, 0)

        for side_z, dz_range in ((-1, range(-2, 0)), (depth, range(depth, depth + 2))):
            for dx in range(4, width - 4):
                for dz in dz_range:
                    self._place(self.mc.Block("smooth quartz slab"), fp + Vec3(dx, 0, dz))
                self._place(self.railing_block, fp + Vec3(dx, 1, dz_range[-1]))
            for dz in dz_range:
                self._place(self.railing_block, fp + Vec3(3, 1, dz))
                self._place(self.railing_block, fp + Vec3(width - 4, 1, dz))
            self._flower_row(fp + Vec3(5, 1, side_z if side_z < 0 else depth), min(6, width - 10), "x")
            self._place(self.end_rod, fp + Vec3(4, 1, side_z if side_z < 0 else depth))
            self._place(self.end_rod, fp + Vec3(width - 5, 1, side_z if side_z < 0 else depth))

    # ═══════════════════════  КРЫША  ═══════════════════════

    def _build_roof(self, params: BuildParams):
        width = params.width
        depth = params.depth
        floors = params.floors
        floor_height = params.floor_height
        start = params.start
        self._current_floor_height = floor_height

        ry = floors * floor_height
        rp = start + Vec3(0, ry, 0)
        mid_x = width // 2
        mid_z = depth // 2

        self._fill(self.roof_block, rp + Vec3(-2, 0, -2), rp + Vec3(width + 1, 0, depth + 1))

        for tier, shrink in enumerate([0, 2, 4]):
            y = tier
            self._fill(self.accent_wall, rp + Vec3(shrink, y, shrink),
                       rp + Vec3(width - 1 - shrink, y, depth - 1 - shrink))

        px, pz = 2, 2
        self._fill(self.pool_block, rp + Vec3(px, 1, pz), rp + Vec3(px + 8, 1, pz + 5))
        self._fill(self.mc.Block("air"), rp + Vec3(px + 1, 1, pz + 1), rp + Vec3(px + 7, 1, pz + 4))
        self._fill(self.pool_block, rp + Vec3(px + 1, 0, pz + 1), rp + Vec3(px + 7, 0, pz + 4))
        self._fill(self.water_block, rp + Vec3(px + 1, 1, pz + 1), rp + Vec3(px + 7, 1, pz + 4))
        for i in range(4):
            self._place(self.mc.Block("spruce stairs").withData({"facing": "north", "half": "bottom"}),
                        rp + Vec3(px + 1 + i * 2, 2, pz + 6))

        for dx in range(12, width - 2):
            for dz in range(2, 7):
                self._place(self.grass_block, rp + Vec3(dx, 1, dz))
        self._tree(rp + Vec3(16, 2, 4), 4)
        self._flower_row(rp + Vec3(12, 2, 2), 6, "x")

        self._kitchen_counter(rp + Vec3(2, 2, depth - 6), 5, "north")
        self._sofa(rp + Vec3(2, 2, depth - 4), 3, "east", "spruce")
        self._dining_table(rp + Vec3(2, 2, depth - 8), 3, "x")
        self._grand_chandelier(rp + Vec3(5, 4, depth - 5), 1)
        self._floor_lamp(rp + Vec3(2, 2, depth - 3))
        self._floor_lamp(rp + Vec3(8, 2, depth - 3))
        self._strip_lights(rp + Vec3(2, 4, depth - 7), 6, "x")

        for dx in range(px, px + 9):
            self._place(self.lantern_floor, rp + Vec3(dx, 1, pz - 1))
            self._place(self.lantern_floor, rp + Vec3(dx, 1, pz + 6))
        for dz in range(pz, pz + 6):
            self._place(self.end_rod, rp + Vec3(px - 1, 2, dz))
            self._place(self.end_rod, rp + Vec3(px + 9, 2, dz))

        for dx in range(mid_x - 2, mid_x + 3):
            for dz in range(mid_z - 2, mid_z + 3):
                self._place(self.glass_block, rp + Vec3(dx, 2, dz))
                self._place(self.glass_block, rp + Vec3(dx, 3, dz))
        self._place(self.light_strip, rp + Vec3(mid_x, 1, mid_z))
        self._grand_chandelier(rp + Vec3(mid_x, 4, mid_z), 1)
        for dx in range(mid_x - 2, mid_x + 3):
            self._place(self.end_rod, rp + Vec3(dx, 1, mid_z - 3))
            self._place(self.end_rod, rp + Vec3(dx, 1, mid_z + 3))
        for dz in range(mid_z - 2, mid_z + 3):
            self._place(self.end_rod, rp + Vec3(mid_x - 3, 1, dz))
            self._place(self.end_rod, rp + Vec3(mid_x + 3, 1, dz))
        for dx in range(mid_x - 2, mid_x + 3):
            self._place(self.railing_block, rp + Vec3(dx, 2, mid_z - 3))
            self._place(self.railing_block, rp + Vec3(dx, 2, mid_z + 3))
        for dz in range(mid_z - 2, mid_z + 3):
            self._place(self.railing_block, rp + Vec3(mid_x - 3, 2, dz))
            self._place(self.railing_block, rp + Vec3(mid_x + 3, 2, dz))

        for dx in range(-2, width + 2):
            self._place(self.railing_block, rp + Vec3(dx, 2, -2))
            self._place(self.railing_block, rp + Vec3(dx, 2, depth + 1))
        for dz in range(-2, depth + 2):
            self._place(self.railing_block, rp + Vec3(-2, 2, dz))
            self._place(self.railing_block, rp + Vec3(width + 1, 2, dz))

        for i, dx in enumerate([3, mid_x, width - 4]):
            h = 8 + i * 3
            for a in range(h):
                self._place(self.antenna_block, rp + Vec3(dx, 3 + a, mid_z))
        self._place(self.mc.Block("beacon"), rp + Vec3(mid_x, 3 + 12, mid_z))

        self._fill(self.mc.Block("yellow concrete"), rp + Vec3(mid_x - 4, 2, mid_z - 4),
                   rp + Vec3(mid_x + 4, 2, mid_z + 4))
        self._fill(self.roof_block, rp + Vec3(mid_x - 3, 2, mid_z - 3),
                   rp + Vec3(mid_x + 3, 2, mid_z + 3))
        for dx, dz in [
            (mid_x - 2, mid_z - 1), (mid_x - 2, mid_z), (mid_x - 2, mid_z + 1),
            (mid_x - 1, mid_z), (mid_x + 1, mid_z),
            (mid_x + 2, mid_z - 1), (mid_x + 2, mid_z), (mid_x + 2, mid_z + 1),
        ]:
            self._place(self.mc.Block("white concrete"), rp + Vec3(dx, 2, dz))

    # ═══════════════════════  ОКРУЖЕНИЕ  ═══════════════════════

    def _build_surroundings(self, params: BuildParams):
        width = params.width
        depth = params.depth
        start = params.start

        ground_y = start.y
        bx = start.x
        bz = start.z

        self._fill(self.plaza_block, Vec3(bx - 5, ground_y, bz - 14), Vec3(bx + width + 4, ground_y, bz - 1))
        self._fill(self.path_block, Vec3(bx + width // 2 - 1, ground_y, bz - 14),
                   Vec3(bx + width // 2 + 1, ground_y, bz - 1))

        self._fountain(Vec3(bx + width // 2, ground_y + 1, bz - 8), radius=3)

        self._tree(Vec3(bx - 2, ground_y + 1, bz - 12), 6)
        self._tree(Vec3(bx + width + 1, ground_y + 1, bz - 12), 6)
        self._tree(Vec3(bx - 2, ground_y + 1, bz - 4), 5)
        self._tree(Vec3(bx + width + 1, ground_y + 1, bz - 4), 5)

        for dx in range(-5, width + 5):
            self._place(self.hedge_block, Vec3(bx + dx, ground_y + 1, bz - 14))
            self._place(self.hedge_block, Vec3(bx + dx, ground_y + 2, bz - 14))
        for dz in range(-14, 0):
            self._place(self.hedge_block, Vec3(bx - 5, ground_y + 1, bz + dz))
            self._place(self.hedge_block, Vec3(bx + width + 4, ground_y + 1, bz + dz))

        for z_off in (-5, -10):
            for side_x, facing in ((2, "east"), (width - 3, "west")):
                self._place(self.mc.Block("spruce stairs").withData({"facing": facing}),
                            Vec3(bx + side_x, ground_y + 1, bz + z_off))
                self._place(self.mc.Block("spruce stairs").withData({"facing": facing}),
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
                self._place(self.mc.Block("dark oak fence"), lp + Vec3(0, dy, 0))
            self._place(self.lantern_hang, lp + Vec3(0, 4, 0))
            self._place(self.end_rod, lp + Vec3(1, 3, 0))
            self._place(self.end_rod, lp + Vec3(-1, 3, 0))

        self._fill(self.mc.Block("spruce planks"), Vec3(bx - 4, ground_y, bz - 3),
                   Vec3(bx - 1, ground_y, bz + 3))
        for dx in range(-4, 0):
            for dz in range(-3, 4, 3):
                self._dining_table(Vec3(bx + dx, ground_y + 1, bz + dz), 2, "x")
        self._tree(Vec3(bx - 3, ground_y + 1, bz), 3)

        self._fill(self.mc.Block("gray concrete"), Vec3(bx, ground_y, bz + depth + 1),
                   Vec3(bx + width - 1, ground_y, bz + depth + 12))
        for dx in range(0, width, 4):
            self._fill(self.mc.Block("white concrete"), Vec3(bx + dx, ground_y, bz + depth + 4),
                       Vec3(bx + dx, ground_y, bz + depth + 9))
        car_colors = ["red", "blue", "yellow", "lime", "cyan", "light_gray", "orange", "purple"]
        for i, dx in enumerate(range(1, min(width - 3, 20), 4)):
            self._parking_car(Vec3(bx + dx, ground_y + 1, bz + depth + 5), car_colors[i % len(car_colors)])
