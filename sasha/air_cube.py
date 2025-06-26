from mcpq import Block, Minecraft, Vec3

from common.minecraft_wrap import MinecraftWrap

mc = Minecraft('localhost')
mcw = MinecraftWrap(mc)

start = Vec3(275, 63, 75)
end = Vec3(85, 100, 330)

mc.setBlockCube("air", start, end)
