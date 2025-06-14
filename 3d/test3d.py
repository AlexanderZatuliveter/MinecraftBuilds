from mcpq import Minecraft, Vec3
import trimesh
from common.files import get_resource_path

file = get_resource_path("3d\\models\\glad3Dprintable-animal-octopus.STL")
mesh = trimesh.load(file)
print('loaded')

mesh.apply_scale(0.025)

voxelized = mesh.voxelized(pitch=1.0)
print('voxelized')

voxels = voxelized.points.astype(int)
print(f'voxels count: {len(voxels)}')

mc = Minecraft('192.168.1.77')  # connect to server on localhost

mc.postToChat("Printing!")

start = Vec3(1567, 50, -791)  # origin of world, coordinates x, y and z = 0

blocks = [start + Vec3(voxel[0], voxel[2], voxel[1]) for voxel in voxels]

mc.setBlockList("stone", blocks)
