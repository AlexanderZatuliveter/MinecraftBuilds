from mcpq import Minecraft, Vec3
import trimesh
from common.files import get_resource_path

file_name = "Trex.stl"
file = get_resource_path(f"3d\\models\\{file_name}")
mesh = trimesh.load(file)
print('loaded')

mesh.apply_scale(3.5)

voxelized = mesh.voxelized(pitch=1.0)
print('voxelized')

voxels = voxelized.points.astype(int)
print(f'voxels count: {len(voxels)}')

mc = Minecraft('192.168.1.77')  # connect to server on localhost

mc.postToChat("Printing!")

start = Vec3(550, 30, 1400)  # origin of world, coordinates x, y and z = 0

blocks = [start + Vec3(voxel[0], voxel[2], voxel[1]) for voxel in voxels]

mc.setBlockList("stone", blocks)
