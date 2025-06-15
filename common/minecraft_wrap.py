

from mcpq import Block, Minecraft, Vec3


class MinecraftWrap:
    def __init__(self, mc: Minecraft) -> None:
        self.__mc = mc
        self.__blocks: dict[str, tuple[Block, list[Vec3]]] = {}
        self.__cubes: dict[str, tuple[Block, list[tuple[Vec3, Vec3]]]] = {}

    def set_block(self, block: Block, pos: Vec3) -> None:
        # print(block, hash(block))
        block_str = str(block)
        if block_str not in self.__blocks:
            self.__blocks[block_str] = (block, [])
        self.__blocks[block_str][1].append(pos)

    def set_block_cube(self, block: Block, pos1: Vec3, pos2: Vec3) -> None:
        block_str = str(block)
        if block not in self.__cubes:
            self.__cubes[block_str] = (block, [])
        self.__cubes[block_str][1].append((pos1, pos2))

    def draw(self):
        for block_str, data in self.__cubes.items():
            for vec1, vec2 in data[1]:
                self.__mc.setBlockCube(data[0], vec1, vec2)

        for block_str, data in self.__blocks.items():
            self.__mc.setBlockList(data[0], data[1])
