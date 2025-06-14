from math import sin, cos, pi
from mcpq import Minecraft, Vec3

mc = Minecraft('192.168.1.77')
mc.postToChat("Генерация шара начинается!")

start_x = -544
start_y = 120
start_z = -500

radius = 25
step = pi / 200  # шаг по углам меньше — шар получится более плотный

phi = 0.0
while phi <= pi:
    theta = 0.0
    while theta <= 2 * pi:
        x = int(radius * sin(phi) * cos(theta * 4))
        y = int(radius * cos(phi))
        z = int(radius * sin(phi*3) * sin(theta / 2))

        pos = Vec3(start_x + x, start_y + y, start_z + z)
        mc.setBlock("stone", pos)

        theta += step
    phi += step