from mcpq import Minecraft, Vec3


def fill_cube(mc: Minecraft, start: Vec3, vol: Vec3, block_name: str = 'stone'):
    for x in range(vol.x):
        for y in range(vol.y):
            for z in range(vol.z):
                block_pos = start + Vec3(x, y, z)
                mc.setBlock(block_name, block_pos)
                

                