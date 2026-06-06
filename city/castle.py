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
        # Generate massive outer walls with ancient texture variation
        for y in range(params.floor_height):
            for dx in range(params.width):
                for dz in range(params.depth):
                    pos = start + Vec3(dx, y, dz)

                    is_edge = (dx == 0 or dx == params.width - 1 or
                               dz == 0 or dz == params.depth - 1)

                    if is_edge:
                        # Randomize blocks for ancient look
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
                        self.mcw.set_block(self.mc.Block("glowstone"), pos)

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
                            is_door = is_r_edge and ry in (1, 2) and (rx == 8 or rz == 8)

                            if is_r_edge and not is_door:
                                r_pos = start + Vec3(dx + rx, ry, dz + rz)
                                self.mcw.set_block(wall_block, r_pos)

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
