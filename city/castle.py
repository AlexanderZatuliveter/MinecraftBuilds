import random
from typing import Literal
from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap
from city.build_params import BuildParams


class MassiveCastle:
    def __init__(self, mc: Minecraft):
        self.mc = mc
        self.mcw = MinecraftWrap(mc)

        # Ancient architecture materials
        self.wall_base = mc.Block("stone_bricks")
        self.wall_mossy = mc.Block("mossy_stone_bricks")
        self.pillar = mc.Block("chiseled_stone_bricks")
        self.floor_block = mc.Block("cobblestone")
        self.window_pane = mc.Block("glass_pane")

        # Colors for varied rooms
        self.colors = [
            "white", "orange", "magenta", "light_blue",
            "yellow", "lime", "pink", "gray", "cyan",
            "purple", "blue", "green", "red", "black"
        ]

    def build(self, params: BuildParams):
        self.mc.postToChat("Building massive 10x10 chunk castle...")

        for f in range(params.floors):
            self._build_floor(f, params)

        self._build_roof(params)
        self._build_towers(params)
        self.mcw.draw()
        self.mc.postToChat("Castle construction completed!")

    def _build_floor(self, floor_idx: int, params: BuildParams):
        # Calculate Y offset for current floor
        y_shift = floor_idx * params.floor_height
        f_start = params.start + Vec3(0, y_shift, 0)

        # Build outer structure, columns, and interior
        self._outer_walls(f_start, params)
        self._inner_columns(f_start, params)
        self._generate_rooms(f_start, params)

    def _outer_walls(self, start: Vec3, params: BuildParams):
        # Generate massive outer walls with ancient texture variation, pillars, and arches
        for y in range(params.floor_height):
            for dx in range(params.width):
                for dz in range(params.depth):
                    pos = start + Vec3(dx, y, dz)

                    is_edge = (dx == 0 or dx == params.width - 1 or
                               dz == 0 or dz == params.depth - 1)

                    if is_edge:
                        # Add grand external columns every 4 blocks for majestic depth
                        is_pillar_spot = (dx % 4 == 0 and dz % 4 == 0)

                        # Create architectural arches between columns
                        # Arch top is at height - 2, sides are at height - 3 and height - 4
                        is_arch_top = (y == params.floor_height - 2 and
                                       (dx % 4 == 2 or dz % 4 == 2))
                        is_arch_side = (y in (params.floor_height - 3, params.floor_height - 4)
                                        and (dx % 4 in (1, 3) or dz % 4 in (1, 3)))
                        is_window = (y in (2, 3) and (dx % 4 == 2 or dz % 4 == 2))

                        if is_pillar_spot:
                            # External decorative pillars select from chiseled bricks
                            self.mcw.set_block(self.pillar, pos)
                        elif is_arch_top or is_arch_side:
                            # Highlight arches with select materials
                            self.mcw.set_block(self.pillar, pos)
                        elif is_window:
                            # Open select windows inside arches for grand look
                            self.mcw.set_block(self.window_pane, pos)
                        else:
                            # Randomize blocks for ancient look inside the main wall
                            is_mossy = random.random() < 0.3
                            block = self.wall_mossy if is_mossy else self.wall_base
                            self.mcw.set_block(block, pos)
                    elif y == 0:
                        # Base floor layer
                        self.mcw.set_block(self.floor_block, pos)

    def _inner_columns(self, start: Vec3, params: BuildParams):
        # Place ancient columns every 16 blocks (1 chunk)
        spacing = 16
        for dx in range(spacing, params.width - spacing, spacing):
            for dz in range(spacing, params.depth - spacing, spacing):
                for y in range(1, params.floor_height):
                    pos = start + Vec3(dx, y, dz)
                    self.mcw.set_block(self.pillar, pos)

                    # Add glowstone lighting at the top of pillars
                    if y == params.floor_height - 1:
                        glow = self.mc.Block("glowstone")
                        self.mcw.set_block(glow, pos)

    def _generate_rooms(self, start: Vec3, params: BuildParams):
        # Divide space into large colorful rooms
        room_size = 16

        # Iterate over the grid to create rooms
        for dx in range(1, params.width - room_size, room_size):
            for dz in range(1, params.depth - room_size, room_size):
                color = random.choice(self.colors)
                wall_block = self.mc.Block(f"{color}_concrete")

                # Build room walls
                for rx in range(room_size):
                    for rz in range(room_size):
                        for ry in range(1, params.floor_height):
                            is_r_edge = (rx == 0 or rx == room_size - 1 or
                                         rz == 0 or rz == room_size - 1)

                            # Leave space for doors
                            is_door = (is_r_edge and ry in (1, 2) and
                                       (rx == 8 or rz == 8))

                            if is_r_edge and not is_door:
                                r_pos = start + Vec3(dx + rx, ry, dz + rz)
                                self.mcw.set_block(wall_block, r_pos)

    def _build_roof(self, params: BuildParams):
        # Build a carved roof with high decorative spires and towers
        roof_y = params.floors * params.floor_height

        for dx in range(params.width):
            for dz in range(params.depth):
                is_edge = (dx == 0 or dx == params.width - 1 or
                           dz == 0 or dz == params.depth - 1)
                if is_edge:
                    # Carved pattern: alternating peaks on edges
                    if (dx + dz) % 2 == 0:
                        pos = params.start + Vec3(dx, roof_y, dz)
                        self.mcw.set_block(self.pillar, pos)
                        wall_blk = self.mc.Block("stone_brick_wall")
                        self.mcw.set_block(wall_blk, pos + Vec3(0, 1, 0))
                else:
                    # Standard roof ceiling layer
                    pos = params.start + Vec3(dx, roof_y - 1, dz)
                    self.mcw.set_block(self.floor_block, pos)

        # Center coordinates for the main gothic spire tower
        cx = params.width // 2
        cz = params.depth // 2

        # Build a grand central roof tower
        for y in range(8):
            for dx in range(-3, 4):
                for dz in range(-3, 4):
                    if abs(dx) == 3 or abs(dz) == 3:
                        pos = params.start + Vec3(cx + dx, roof_y + y, cz + dz)
                        self.mcw.set_block(self.wall_base, pos)

        # Add a tall tapered spire on top of the central tower
        spire_y = roof_y + 8
        for y in range(12):
            size = 3 - (y // 4)
            size = max(0, size)
            for dx in range(-size, size + 1):
                for dz in range(-size, size + 1):
                    pos = params.start + Vec3(cx + dx, spire_y + y, cz + dz)
                    blk = (self.pillar if size > 0
                           else self.mc.Block("stone_brick_wall"))
                    self.mcw.set_block(blk, pos)

        # Add extra decorative spires across the roof landscape
        spacing = 16
        for dx in range(spacing, params.width - spacing, spacing):
            for dz in range(spacing, params.depth - spacing, spacing):
                if abs(dx - cx) > 5 or abs(dz - cz) > 5:
                    self._build_small_spire(
                        params.start + Vec3(dx, roof_y, dz)
                    )

    def _build_small_spire(self, base_pos: Vec3):
        # Build a sharp 5-block tall spire
        for y in range(4):
            self.mcw.set_block(self.pillar, base_pos + Vec3(0, y, 0))
        top_blk = self.mc.Block("stone_brick_wall")
        self.mcw.set_block(top_blk, base_pos + Vec3(0, 4, 0))

    def _build_towers(self, params: BuildParams):
        # Add high watchtowers at the 4 corners of the castle
        tower_h = params.floor_height * 2
        roof_y = params.floors * params.floor_height

        corners = [
            Vec3(0, roof_y, 0),
            Vec3(params.width - 1, roof_y, 0),
            Vec3(0, roof_y, params.depth - 1),
            Vec3(params.width - 1, roof_y, params.depth - 1)
        ]

        for corner in corners:
            # Build up the tower structure
            for y in range(tower_h):
                for dx in [-1, 0, 1]:
                    for dz in [-1, 0, 1]:
                        pos = params.start + corner + Vec3(dx, y, dz)
                        self.mcw.set_block(self.wall_base, pos)

                # Top of the tower beacon
                if y == tower_h - 1:
                    fire_pos = params.start + corner + Vec3(0, tower_h, 0)
                    self.mcw.set_block(self.mc.Block("campfire"), fire_pos)
