import random
from typing import Literal

from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap
from sasha.skyscrapers.build_params import BuildParams


class GeminiSkyscraper:
    def __init__(self, mc: Minecraft):
        self.mc = mc
        self.mcw = MinecraftWrap(mc)

        self.wall_block = mc.Block("cyan_terracotta")
        self.glass_block = mc.Block("black_stained_glass_pane")
        self.floor_block = mc.Block("smooth_stone")
        self.pillar_block = mc.Block("stripped_dark_oak_log")
        self.roof_block = mc.Block("stone_bricks")
        self.antenna_block = mc.Block("iron_bars")
        self.atrium_block = mc.Block("sea_lantern")
        self.railing_block = mc.Block("dark_oak_fence")
        self.accent_block = mc.Block("quartz_block")

    def build(self, build_params: BuildParams):
        self.mc.postToChat("Building advanced skyscraper...")
        p = build_params

        for f in range(p.floors):
            self._build_floor(f, p)

        self._roof_with_helipad(p)
        self._modern_spire(p)

        self.mcw.draw()
        self.mc.postToChat("Skyscraper construction completed successfully!")

    # ═══════════════════════  КРЫША  ═══════════════════════

    def _roof_with_helipad(self, params: BuildParams):
        pos = params.start
        roof_shift = params.floors * params.floor_height

        for dx in range(-1, params.width + 2):
            for dz in range(-1, params.depth + 2):
                self.mcw.set_block(self.roof_block, pos + Vec3(dx, roof_shift, dz))

        helipad_y = roof_shift + 1
        cx = params.width // 2
        cz = params.depth // 2

        for dx in range(-4, 5):
            for dz in range(-4, 5):
                self.mcw.set_block(self.mc.Block("gray_concrete"), pos + Vec3(cx + dx, helipad_y, cz + dz))

        for dz in range(-2, 3):
            self.mcw.set_block(self.accent_block, pos + Vec3(cx - 2, helipad_y, cz + dz))
            self.mcw.set_block(self.accent_block, pos + Vec3(cx + 2, helipad_y, cz + dz))
        for dx in range(-1, 2):
            self.mcw.set_block(self.accent_block, pos + Vec3(cx + dx, helipad_y, cz))

    def _modern_spire(self, params: BuildParams):
        pos = params.start
        roof_shift = params.floors * params.floor_height + 1
        cx = params.width // 2 - 6
        cz = params.depth // 2

        for dy in range(12):
            self.mcw.set_block(self.mc.Block("iron_block"), pos + Vec3(cx, roof_shift + dy, cz))

        self.mcw.set_block(self.mc.Block("redstone_block"), pos + Vec3(cx, roof_shift + 12, cz))
        self.mcw.set_block(
            self.mc.Block("lightning_rod").withData({"facing": "up"}),
            pos + Vec3(cx, roof_shift + 13, cz)
        )

    # ═══════════════════════  ДЕКОР / МЕБЕЛЬ  ═══════════════════════

    def _table_with_lanterns(self, pos: Vec3):
        self.mcw.set_block(self.mc.Block("crafting table"), pos + Vec3(0, 0, 0))
        self.mcw.set_block(self.mc.Block("crafting table"), pos + Vec3(-1, 0, 0))
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(0, 1, 0))
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(-1, 1, 0))

    def _storage(self, pos: Vec3, wood_type: str):
        log_positions = [Vec3(0, 1, 0), Vec3(0, 2, 0), Vec3(0, 3, 0)]
        for log_pos in log_positions:
            self.mcw.set_block(self.mc.Block(f"{wood_type} log"), log_pos + pos)
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(0, 4, 0))

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
            self.mcw.set_block(self.mc.Block("chest").withData({"facing": direction}), p + pos)

    def _atrium_and_pillars(self, pos: Vec3, light_block: Block, pillar_block: Block, floor_h: int):
        lighting_positions = []
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                lighting_positions.append(Vec3(dx, 0, dz))

        for p in lighting_positions:
            self.mcw.set_block(light_block, p + pos)

        pillar_positions = []
        for y in range(1, floor_h):
            pillar_positions.extend([
                Vec3(-3, y, -3), Vec3(3, y, 3),
                Vec3(3, y, -3), Vec3(-3, y, 3)
            ])

        for p in pillar_positions:
            self.mcw.set_block(pillar_block, p + pos)

    def _sofa_with_table(self, wood_type: str, pos: Vec3):
        self.mcw.set_block(self.mc.Block(f"{wood_type} fence"), pos)
        self.mcw.set_block(self.mc.Block(f"{wood_type} pressure plate"), pos + Vec3(0, 1, 0))
        self.mcw.set_block(self.mc.Block(f"{wood_type} log"), pos + Vec3(2, 0, 2))
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(2, 1, 2))

        stairs_properties = [
            (Vec3(0, 0, 2), "south"), (Vec3(1, 0, 2), "south"),
            (Vec3(2, 0, 1), "east"), (Vec3(2, 0, 0), "east")
        ]
        for p, direction in stairs_properties:
            self.mcw.set_block(
                self.mc.Block(f"{wood_type} stairs").withData({"facing": direction}),
                p + pos
            )

    def _bookshelves_and_lanterns(self, pos: Vec3):
        bookshelves_positions = []
        for y in range(0, 3):
            bookshelves_positions.extend([
                Vec3(0, y, 0), Vec3(-1, y, 0), Vec3(-2, y, 0),
                Vec3(0, y, 1), Vec3(0, y, 2)
            ])

        for p in bookshelves_positions:
            self.mcw.set_block(self.mc.Block("bookshelf"), p + pos)

        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(0, 3, 0))
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(-2, 3, 0))
        self.mcw.set_block(self.mc.Block("lantern"), pos + Vec3(0, 3, 2))

    def _street_lamp(self, pos: Vec3, fence_material: str, facing: str):
        for dy in range(2, 5):
            self.mcw.set_block(f"{fence_material} fence", pos + Vec3(0, dy, 0))
        if facing == "south":
            self.mcw.set_block(f"{fence_material} fence", pos + Vec3(0, 4, 1))
            self.mcw.set_block(f"{fence_material} fence", pos + Vec3(-1, 4, 0))
            self.mcw.set_block(self.mc.Block("lantern").withData({"hanging": True}), pos + Vec3(0, 3, 1))
            self.mcw.set_block(self.mc.Block("lantern").withData({"hanging": True}), pos + Vec3(-1, 3, 0))
        elif facing == "north":
            self.mcw.set_block(f"{fence_material} fence", pos + Vec3(0, 4, -1))
            self.mcw.set_block(f"{fence_material} fence", pos + Vec3(-1, 4, 0))
            self.mcw.set_block(self.mc.Block("lantern").withData({"hanging": True}), pos + Vec3(0, 3, -1))
            self.mcw.set_block(self.mc.Block("lantern").withData({"hanging": True}), pos + Vec3(-1, 3, 0))

    # ═══════════════════════  ЛЕСТНИЦА  ═══════════════════════

    def _ladder(self, pos: Vec3, floor: int, floor_height: int, max_floor: int):
        def even_floor():
            self.mcw.set_block_cube("quartz block", pos + Vec3(1, 0, -1), pos + Vec3(3, 0, -4))
            for dx in range(1, 5):
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(dx, 0, 0)
                )

            stairs_y = 1
            for dz in range(5, 10):
                self.mcw.set_block("quartz stairs", pos + Vec3(1, stairs_y, -dz))
                self.mcw.set_block("quartz stairs", pos + Vec3(2, stairs_y, -dz))
                self.mcw.set_block(self.mc.Block(self.railing_block), pos + Vec3(3, stairs_y, -dz + 1))
                self.mcw.set_block(
                    self.mc.Block("quartz stairs").withData({"facing": "south", "half": "top"}),
                    pos + Vec3(3, stairs_y, -dz)
                )
                stairs_y += 1

            self.mcw.set_block_cube(
                "quartz block",
                pos + Vec3(1, floor_height, -10),
                pos + Vec3(3, floor_height, -13)
            )
            for dx in range(1, 4):
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(dx, floor_height, -14)
                )

        def odd_floor():
            self.mcw.set_block_cube("quartz block", pos + Vec3(6, 0, -10), pos + Vec3(4, 0, -13))

            for dx in range(1, 7):
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(dx, 0, -14)
                )
                self.mcw.set_block(self.mc.Block(self.railing_block), pos + Vec3(dx, 1, -14))
            for dz in range(10, 14):
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(6, 0, -dz)
                )
                self.mcw.set_block(self.mc.Block(self.railing_block), pos + Vec3(6, 1, -dz))

            self._street_lamp(pos + Vec3(6, 0, -14), fence_material="pale oak", facing="south")

            stairs_y = 5
            for dz in range(5, 10):
                self.mcw.set_block(
                    self.mc.Block("quartz stairs").withData({"facing": "south"}),
                    pos + Vec3(4, stairs_y, -dz)
                )
                self.mcw.set_block(
                    self.mc.Block("quartz stairs").withData({"facing": "south"}),
                    pos + Vec3(5, stairs_y, -dz)
                )
                self.mcw.set_block(
                    self.mc.Block("quartz stairs").withData({"facing": "north", "half": "top"}),
                    pos + Vec3(6, stairs_y, -dz)
                )
                self.mcw.set_block(
                    self.mc.Block("quartz stairs").withData({"facing": "north", "half": "top"}),
                    pos + Vec3(3, stairs_y, -dz)
                )
                self.mcw.set_block(self.railing_block, pos + Vec3(6, stairs_y + 1, -dz))
                self.mcw.set_block(self.railing_block, pos + Vec3(3, stairs_y, -dz - 1))
                stairs_y -= 1

            self.mcw.set_block_cube(
                "quartz block",
                pos + Vec3(4, floor_height, -1),
                pos + Vec3(5, floor_height, -4)
            )

            for dx in range(1, 7):
                if dx >= 5:
                    self.mcw.set_block(
                        self.mc.Block("quartz slab").withData({"type": "top"}),
                        pos + Vec3(dx, floor_height, 0)
                    )
                self.mcw.set_block(self.mc.Block(self.railing_block), pos + Vec3(dx, floor_height + 1, 0))
            for dz in range(1, 5):
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(6, floor_height, -dz)
                )
                self.mcw.set_block(self.mc.Block(self.railing_block), pos + Vec3(6, floor_height + 1, -dz))

            self._street_lamp(pos + Vec3(6, floor_height, 0), fence_material="pale oak", facing="north")

        if floor == 0:
            self.mcw.set_block_cube("quartz block", pos + Vec3(4, 0, 0), pos + Vec3(6, 0, -4))
            for dx in range(4, 7):
                self.mcw.set_block(self.railing_block, pos + Vec3(dx, 1, -4))
            for dz in range(0, 4):
                self.mcw.set_block(self.railing_block, pos + Vec3(6, 1, -dz))

            self._street_lamp(pos + Vec3(6, 0, 0), fence_material="pale oak", facing="north")

        elif floor == max_floor:
            if max_floor % 2 == 0:
                self.mcw.set_block(self.railing_block, pos + Vec3(3, floor_height + 1, -9))
                self.mcw.set_block(self.railing_block, pos + Vec3(4, floor_height + 1, -9))
                self.mcw.set_block(
                    self.mc.Block("quartz slab").withData({"type": "top"}),
                    pos + Vec3(4, floor_height, -9)
                )
                for dz in range(10, 15):
                    self.mcw.set_block(
                        self.mc.Block("quartz slab").withData({"type": "top"}),
                        pos + Vec3(4, floor_height, -dz)
                    )
                    self.mcw.set_block(self.railing_block, pos + Vec3(4, floor_height + 1, -dz))
                for dx in range(1, 4):
                    self.mcw.set_block(self.railing_block, pos + Vec3(dx, floor_height + 1, -14))
                self._street_lamp(
                    pos + Vec3(4, floor_height, -14),
                    fence_material="pale oak",
                    facing="south"
                )
            else:
                self.mcw.set_block_cube(
                    "quartz block",
                    pos + Vec3(1, floor_height, -1),
                    pos + Vec3(3, floor_height, -5)
                )
                for dx in range(1, 4):
                    self.mcw.set_block(
                        self.mc.Block("quartz slab").withData({"type": "top"}),
                        pos + Vec3(dx, floor_height, 0)
                    )
                    self.mcw.set_block(self.railing_block, pos + Vec3(dx, floor_height + 1, 0))
                    self.mcw.set_block(self.railing_block, pos + Vec3(dx, floor_height + 1, -5))

        if floor % 2 != 0:
            odd_floor()
        else:
            even_floor()

    # ═══════════════════════  ЭТАЖ  ═══════════════════════

    def _build_floor(self, f_idx: int, params: BuildParams):
        floor_shift = Vec3(0, f_idx * params.floor_height, 0)
        floor_start = params.start + floor_shift
        width = params.width
        depth = params.depth
        floor_height = params.floor_height

        for y in range(floor_height):
            for dx in range(width):
                for dz in range(depth):
                    current_pos = floor_start + Vec3(dx, y, dz)
                    is_edge = dx in (0, width - 1) or dz in (0, depth - 1)
                    is_corner = dx in (0, width - 1) and dz in (0, depth - 1)

                    if is_edge:
                        if is_corner:
                            self.mcw.set_block(self.accent_block, current_pos)
                        elif 1 <= y <= 3:
                            self.mcw.set_block(self.glass_block, current_pos)
                        else:
                            self.mcw.set_block(self.wall_block, current_pos)
                    else:
                        self.mcw.set_block(self.floor_block, floor_start + Vec3(dx, 0, dz))

        if f_idx != params.floors - 1:
            self._ladder(floor_start + Vec3(width - 1, 0, depth - 1), f_idx, floor_height, params.floors - 2)

        self._atrium_and_pillars(
            floor_start + Vec3(width // 2, 0, depth // 2), self.atrium_block, self.pillar_block, floor_height
        )

        bed_colors: list[Literal[
            "red", "orange", "yellow", "lime", "green", "cyan",
            "light_blue", "blue", "purple", "magenta", "pink"
        ]] = [
            "red", "orange", "yellow", "lime", "green", "cyan",
            "light_blue", "blue", "purple", "magenta", "pink"
        ]
        rand_color = random.choice(bed_colors)

        self.mc.setBed(floor_start + Vec3(4, 1, 3), "north", rand_color)
        self.mc.setBed(floor_start + Vec3(3, 1, 3), "north", rand_color)
        self.mcw.set_block(self.mc.Block("crafting table"), floor_start + Vec3(2, 1, 2))
        self.mcw.set_block(self.mc.Block("lantern"), floor_start + Vec3(2, 2, 2))

        self._storage(floor_start + Vec3(2, 0, depth - 3), "oak")

        if f_idx % 2 == 0:
            self._bookshelves_and_lanterns(floor_start + Vec3(width - 3, 1, 2))
            self._table_with_lanterns(floor_start + Vec3(width - 4, 1, depth - 2))
            self.mcw.set_block(self.mc.Block("air"), floor_start + Vec3(width - 1, 1, depth - 3))
            self.mcw.set_block(self.mc.Block("air"), floor_start + Vec3(width - 1, 2, depth - 3))
        else:
            self._sofa_with_table("oak", floor_start + Vec3(width - 5, 1, depth - 5))
            self._table_with_lanterns(floor_start + Vec3(width - 4, 1, 1))
            self.mcw.set_block(self.mc.Block("air"), floor_start + Vec3(width - 1, 1, 2))
            self.mcw.set_block(self.mc.Block("air"), floor_start + Vec3(width - 1, 2, 2))
