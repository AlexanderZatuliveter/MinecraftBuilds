

from mcpq import Minecraft, Vec3


class MinecraftWrap:

    def __init__(self, mc: Minecraft) -> None:
        self.__mc = mc
        self.__blocks: dict[str, list[Vec3]] = {}
        self.__cubes: dict[str, list[tuple[Vec3, Vec3]]] = {}

    def set_block(self, block_type: str, pos: Vec3) -> None:
        self.__blocks[block_type].append(pos)

    def set_block_cube(self, block_type: str, pos1: Vec3, pos2: Vec3) -> None:
        self.__cubes[block_type].append((pos1, pos2))

    def draw(self):

        for block_type, vecs in self.__cubes.items():
            for vec1, vec2 in vecs:
                self.__mc.setBlockCube(block_type, vec1, vec2)

        for block_type, vecs in self.__blocks.items():
            self.__mc.setBlockList(block_type, vecs)
